import os
import sys

# Ensure script directory is ALWAYS in sys.path and working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
try:
    os.chdir(BASE_DIR)
except Exception:
    pass

import asyncio
from ui import render_banner, render_menu, HOT_PINK, BRIGHT_MAGENTA, GREEN, YELLOW, RED, CYAN, WHITE, GRAY, RESET
from client import FastDiscordClient
from webhook import WebhookNotifier
from sniper import VanitySniper
from swapper import VanitySwapper
from speed_monitor import SpeedMonitor
from config_editor import load_config, run_config_editor, print_config_summary
from inspector import inspect_guild, check_vanity_interactive, run_jitter_benchmark

MENU_ITEMS = [
    {"num": 1, "title": "FAST VANITY SNIPER"},
    {"num": 2, "title": "INSTANT VANITY SWAPPER"},
    {"num": 3, "title": "GUILD BOOST INSPECTOR"},
    {"num": 4, "title": "LIVE SPEED MONITOR"},
    {"num": 5, "title": "EDIT CONFIGURATION"},
    {"num": 6, "title": "SEND TEST WEBHOOK"},
    {"num": 7, "title": "CHECK VANITY STATUS"},
    {"num": 8, "title": "SPEED BENCHMARK & JITTER"},
    {"num": 9, "title": "VIEW TOKENS & CONFIG"},
    {"num": 10, "title": "EXIT PROGRAM"}
]

async def main():
    config = load_config()
    if not config:
        print(f"{RED}Fatal: Failed to load config.json!{RESET}")
        return

    client = FastDiscordClient(config)
    webhook = WebhookNotifier(config.get("webhook", {}).get("url"), config.get("webhook", {}).get("enabled", True))
    monitor = SpeedMonitor(client)

    # Pre-warm socket on launch in background
    asyncio.create_task(client.pre_warm())

    try:
        while True:
            render_banner(author="aqxior")
            prompt_str = render_menu(MENU_ITEMS, prompt_tag="@/aqxilorcore")

            choice = input(prompt_str).strip()

            if choice == "1":
                sniper = VanitySniper(client, webhook, config)
                await sniper.start()
                input(f"\n{GRAY}Press Enter to return to menu...{RESET}")

            elif choice == "2":
                swapper = VanitySwapper(client, webhook, config)
                await swapper.start()
                input(f"\n{GRAY}Press Enter to return to menu...{RESET}")

            elif choice == "3":
                await inspect_guild(client, config)
                input(f"\n{GRAY}Press Enter to return to menu...{RESET}")

            elif choice == "4":
                # Live Speed Monitor
                await monitor.run_live_monitor()
                input(f"\n{GRAY}Press Enter to return to menu...{RESET}")

            elif choice == "5":
                updated = run_config_editor()
                if updated:
                    config = updated
                    webhook = WebhookNotifier(config.get("webhook", {}).get("url"), config.get("webhook", {}).get("enabled", True))

            elif choice == "6":
                url = config.get("webhook", {}).get("url")
                if not url:
                    print(f"\n{RED}[!] No webhook URL set! Configure it via Option [5].{RESET}")
                else:
                    sys.stdout.write(f"\n{YELLOW}[*] Sending test webhook embed... {RESET}")
                    sys.stdout.flush()
                    await webhook.send_alert("Webhook Speed Test", "aqxilorcore verified! Live ms latency reporting active.")
                    print(f"{GREEN}SENT ✅ Check your Discord channel!{RESET}")
                input(f"\n{GRAY}Press Enter to return to menu...{RESET}")

            elif choice == "7":
                await check_vanity_interactive(client)
                input(f"\n{GRAY}Press Enter to return to menu...{RESET}")

            elif choice == "8":
                await run_jitter_benchmark(client)
                input(f"\n{GRAY}Press Enter to return to menu...{RESET}")

            elif choice == "9":
                print_config_summary(config)
                input(f"\n{GRAY}Press Enter to return to menu...{RESET}")

            elif choice == "10":
                print(f"\n{BRIGHT_MAGENTA}Exiting aqxilorcore. Fast claims ahead! ⚡{RESET}\n")
                await client.close()
                sys.exit(0)

            else:
                print(f"\n{RED}[!] Invalid option '{choice}'. Choose 1-10.{RESET}")
                await asyncio.sleep(0.8)

    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Interrupted. Closing session...{RESET}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
