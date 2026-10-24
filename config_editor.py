import os
import json
from ui import HOT_PINK, BRIGHT_MAGENTA, GREEN, YELLOW, RED, CYAN, WHITE, GRAY, RESET

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return None
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def save_config(config):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        return True
    except Exception:
        return False

def mask_token(token):
    if not token or len(token) < 10:
        return token or "Not Set"
    return token[:6] + "••••••••••••••••••••" + token[-4:]

def mask_password(pwd, totp=None):
    if totp:
        return f"2FA Active (pyotp TOTP ✅)"
    if not pwd:
        return "Not Set (2FA or Password)"
    return "••••••••••••"

def run_config_editor():
    config = load_config()
    if not config:
        print(f"{RED}Error: Unable to load config.json!{RESET}")
        return None

    while True:
        tokens = config.get("tokens", {})
        guilds = config.get("guilds", {})
        vanity = config.get("vanity", {})
        webhook = config.get("webhook", {})

        print(f"\n{HOT_PINK}╭─────────────────────────────────────────────────────────────────────────────╮{RESET}")
        print(f"{HOT_PINK}│{RESET}  {BRIGHT_MAGENTA}⚙️  CONFIG EDITOR (Live Updates to config.json){RESET}{' ' * 29}{HOT_PINK}│{RESET}")
        print(f"{HOT_PINK}├─────────────────────────────────────────────────────────────────────────────┤{RESET}")
        print(f"{HOT_PINK}│{RESET}  [ 1] Sniper Token        : {GRAY}{mask_token(tokens.get('sniper_token'))}{RESET}")
        print(f"{HOT_PINK}│{RESET}  [ 2] 2FA Secret / Password: {YELLOW}{mask_password(tokens.get('account_password'), tokens.get('two_factor_secret'))}{RESET}")
        print(f"{HOT_PINK}│{RESET}  [ 3] Swapper Token A     : {GRAY}{mask_token(tokens.get('swapper_token_a'))}{RESET}")
        print(f"{HOT_PINK}│{RESET}  [ 4] Swapper Token B     : {GRAY}{mask_token(tokens.get('swapper_token_b'))}{RESET}")
        print(f"{HOT_PINK}│{RESET}  [ 5] Target Guild ID     : {CYAN}{guilds.get('target_guild_id', 'Not Set')}{RESET}")
        print(f"{HOT_PINK}│{RESET}  [ 6] Source Guild ID     : {CYAN}{guilds.get('source_guild_id', 'Not Set')}{RESET}")
        print(f"{HOT_PINK}│{RESET}  [ 7] Destination Guild ID: {CYAN}{guilds.get('destination_guild_id', 'Not Set')}{RESET}")
        print(f"{HOT_PINK}│{RESET}  [ 8] Target Vanity Code  : {GREEN}discord.gg/{vanity.get('target_vanity', 'Not Set')}{RESET}")
        print(f"{HOT_PINK}│{RESET}  [ 9] Webhook URL         : {YELLOW}{'Configured ✅' if webhook.get('url') else 'Disabled / Not Set'}{RESET}")
        print(f"{HOT_PINK}│{RESET}  [ 0] Back to Main Menu")
        print(f"{HOT_PINK}╰─────────────────────────────────────────────────────────────────────────────╯{RESET}\n")

        opt = input(f"{RED}(config){RESET} {WHITE}Select item to edit (0-9): {RESET}").strip()

        if opt == "0":
            break
        elif opt == "1":
            val = input(f"{CYAN}Enter New Sniper Token: {RESET}").strip()
            if val:
                tokens["sniper_token"] = val
                save_config(config)
                print(f"{GREEN}✓ Saved!{RESET}")
        elif opt == "2":
            print(f"\n{CYAN}Choose MFA method to configure:{RESET}")
            print(f"  [1] 2FA Secret Key (Google Authenticator TOTP - Recommended ⚡)")
            print(f"  [2] Account Password")
            m_opt = input(f"{WHITE}Select (1/2): {RESET}").strip()
            if m_opt == "1":
                val = input(f"{CYAN}Enter 2FA Secret Key (from Discord Settings): {RESET}").strip()
                tokens["two_factor_secret"] = val.replace(" ", "").upper()
                save_config(config)
                print(f"{GREEN}✓ 2FA Secret Key Saved! (pyotp Auto-MFA is now active ⚡){RESET}")
            else:
                val = input(f"{CYAN}Enter Discord Account Password: {RESET}").strip()
                tokens["account_password"] = val
                save_config(config)
                print(f"{GREEN}✓ Password Saved! (Auto-MFA is now active){RESET}")
        elif opt == "3":
            val = input(f"{CYAN}Enter New Swapper Token A (Source): {RESET}").strip()
            if val:
                tokens["swapper_token_a"] = val
                save_config(config)
                print(f"{GREEN}✓ Saved!{RESET}")
        elif opt == "4":
            val = input(f"{CYAN}Enter New Swapper Token B (Destination): {RESET}").strip()
            if val:
                tokens["swapper_token_b"] = val
                save_config(config)
                print(f"{GREEN}✓ Saved!{RESET}")
        elif opt == "5":
            val = input(f"{CYAN}Enter Target Guild ID: {RESET}").strip()
            if val:
                guilds["target_guild_id"] = val
                save_config(config)
                print(f"{GREEN}✓ Saved!{RESET}")
        elif opt == "6":
            val = input(f"{CYAN}Enter Source Guild ID (Server A): {RESET}").strip()
            if val:
                guilds["source_guild_id"] = val
                save_config(config)
                print(f"{GREEN}✓ Saved!{RESET}")
        elif opt == "7":
            val = input(f"{CYAN}Enter Destination Guild ID (Server B): {RESET}").strip()
            if val:
                guilds["destination_guild_id"] = val
                save_config(config)
                print(f"{GREEN}✓ Saved!{RESET}")
        elif opt == "8":
            val = input(f"{CYAN}Enter Target Vanity (e.g. aqxilorcore): {RESET}").strip()
            if val:
                vanity["target_vanity"] = val.replace("https://discord.gg/", "").replace("discord.gg/", "")
                save_config(config)
                print(f"{GREEN}✓ Saved!{RESET}")
        elif opt == "9":
            val = input(f"{CYAN}Enter Discord Webhook URL: {RESET}").strip()
            webhook["url"] = val
            webhook["enabled"] = bool(val)
            save_config(config)
            print(f"{GREEN}✓ Saved!{RESET}")

    return config

def print_config_summary(config):
    tokens = config.get("tokens", {})
    guilds = config.get("guilds", {})
    vanity = config.get("vanity", {})
    webhook = config.get("webhook", {})

    print(f"\n{HOT_PINK}═══ CURRENT CONFIGURATION SUMMARY ═══{RESET}")
    print(f"Sniper Token        : {GRAY}{mask_token(tokens.get('sniper_token'))}{RESET}")
    print(f"Account Password    : {YELLOW}{mask_password(tokens.get('account_password'))}{RESET}")
    print(f"Swapper Token A     : {GRAY}{mask_token(tokens.get('swapper_token_a'))}{RESET}")
    print(f"Swapper Token B     : {GRAY}{mask_token(tokens.get('swapper_token_b'))}{RESET}")
    print(f"Target Guild ID     : {CYAN}{guilds.get('target_guild_id', 'Not Set')}{RESET}")
    print(f"Source Guild ID     : {CYAN}{guilds.get('source_guild_id', 'Not Set')}{RESET}")
    print(f"Dest Guild ID       : {CYAN}{guilds.get('destination_guild_id', 'Not Set')}{RESET}")
    print(f"Target Vanity       : {GREEN}discord.gg/{vanity.get('target_vanity', 'Not Set')}{RESET}")
    print(f"Webhook Configured  : {YELLOW}{'Yes' if webhook.get('url') else 'No'}{RESET}")
    print(f"{HOT_PINK}═════════════════════════════════════{RESET}\n")
