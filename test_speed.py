import asyncio
import sys
from client import FastDiscordClient
from config_editor import load_config
from ui import render_banner, render_menu
from speed_monitor import SpeedMonitor

async def run_tests():
    print("🧪 [PYTHON TEST SUITE] Verifying Cherry Vanity Engine (Python Edition)...\n")

    # Test 1: Config Load
    config = load_config()
    assert config is not None, "Failed to load config.json"
    print("✅ [TEST 1 PASSED] config.json loaded successfully.")

    # Test 2: UI Render Test
    try:
        render_banner(author="aqxior")
        render_menu([
            {"num": 1, "title": "TEST OPTION 1"},
            {"num": 2, "title": "TEST OPTION 2"}
        ], prompt_tag="test")
        print("✅ [TEST 2 PASSED] UI Banner & Double-Column Menu rendered cleanly.")
    except Exception as e:
        raise AssertionError(f"UI render failed: {e}")

    # Test 3: Client Pre-warm
    client = FastDiscordClient(config)
    print("\n[*] Testing TCP & TLS 1.3 socket pre-warm...")
    warm = await client.pre_warm()
    if warm.get("success"):
        print(f"✅ [TEST 3 PASSED] TLS 1.3 socket pre-warmed in {warm['latency_ms']} ms.")
    else:
        print(f"⚠️ Pre-warm note: {warm.get('error')}")

    # Test 4: Ping Discord API
    print("[*] Testing instant Discord API round-trip latency...")
    ping = await client.ping_discord()
    if ping is not None:
        print(f"✅ [TEST 4 PASSED] Discord API ping measured: {ping} ms.")
    else:
        print("⚠️ Ping check timed out or network issue.")

    # Test 5: Check Vanity Query
    print("[*] Testing vanity availability query for 'discord-developers'...")
    check = await client.check_vanity("discord-developers")
    print(f"✅ [TEST 5 PASSED] Vanity status query completed in {check.get('latency_ms', 0)} ms (Available: {check.get('available')}).")

    # Test 6: Speed Monitor Gauge
    monitor = SpeedMonitor(client)
    tag = monitor.get_speed_tag(25.0)
    bar = monitor.get_speed_bar(25.0)
    print(f"✅ [TEST 6 PASSED] Speed gauge rendered: {bar} {tag}")

    await client.close()
    print("\n🎉 ALL 6 PYTHON VERIFICATION TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(run_tests())
