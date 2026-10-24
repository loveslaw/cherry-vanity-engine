#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ aqxilorcore (Single-File Standalone Edition)
All-in-One Discord Vanity Sniper & Atomic Swapper with Live Speed Monitor & Auto-MFA Resolver
Zero internal imports - 100% immune to ModuleNotFoundError!
"""

import os
import sys
import time
import json
import shutil
import asyncio

# Setup Base Directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
try:
    os.chdir(BASE_DIR)
except Exception:
    pass

# Auto-install or handle external packages
try:
    import aiohttp
except ImportError:
    print("[*] Installing aiohttp...")
    os.system(f"{sys.executable} -m pip install aiohttp")
    import aiohttp

try:
    from colorama import init, Style
    init(autoreset=True)
except ImportError:
    try:
        os.system(f"{sys.executable} -m pip install colorama")
        from colorama import init, Style
        init(autoreset=True)
    except Exception:
        class Style:
            RESET_ALL = "\033[0m"
            BRIGHT = "\033[1m"

# UI Colors (Matching Screenshot Magenta Theme)
HOT_PINK = "\033[38;2;255;0;160m"
BRIGHT_MAGENTA = "\033[38;2;255;30;200m"
MAGENTA = "\033[38;2;255;0;255m"
CYAN = "\033[38;2;0;220;255m"
GREEN = "\033[38;2;40;220;120m"
YELLOW = "\033[38;2;255;200;50m"
RED = "\033[38;2;255;50;50m"
WHITE = "\033[38;2;245;245;245m"
GRAY = "\033[38;2;120;120;120m"
RESET = Style.RESET_ALL

CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

DEFAULT_CONFIG = {
    "tokens": {
        "sniper_token": "YOUR_DISCORD_TOKEN_HERE",
        "account_password": "",
        "swapper_token_a": "SOURCE_SERVER_TOKEN_HERE",
        "swapper_token_b": "DESTINATION_SERVER_TOKEN_HERE"
    },
    "guilds": {
        "target_guild_id": "YOUR_TARGET_SERVER_ID",
        "source_guild_id": "SOURCE_SERVER_ID",
        "destination_guild_id": "DESTINATION_SERVER_ID"
    },
    "vanity": {
        "target_vanity": "aqxilorcore",
        "dummy_vanity": "temp_swap_9821"
    },
    "webhook": {
        "url": "",
        "enabled": True
    },
    "settings": {
        "pre_warm_connections": True,
        "keep_alive_timeout": 60,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
}

def load_config():
    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_CONFIG

def save_config(cfg):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
        return True
    except Exception:
        return False

def mask_token(token):
    if not token or len(token) < 10:
        return token or "Not Set"
    return token[:6] + "••••••••••••••••••••" + token[-4:]

def mask_password(pwd):
    if not pwd:
        return "Not Set (Required if Discord asks 2FA)"
    return "••••••••••••"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def render_banner(author="aqxior"):
    clear_screen()
    ascii_art = f"""
{HOT_PINK} /__  \\|  \\  \\ \\ / /  _   | |   _   \\
/ /\\  \\| | \\  \\ V /  | | | | | |_)  /
|  _   | |  \\   /   | | | | |  _  < 
| | |  | \\  / / \\ \\ | |_| | | | \\  \\
\\_| |_/\\__// /   \\_\\ \\___/|_|_|  \\_\\{RESET}
"""
    print(ascii_art)
    term_width = shutil.get_terminal_size((80, 24)).columns
    max_w = min(term_width, 78)
    print(f"{HOT_PINK}{'─' * max_w}{RESET}")
    subtext = f"MADE BY - {author}"
    pad = max(0, (max_w - len(subtext)) // 2)
    print(" " * pad + f"{Style.BRIGHT}{WHITE}{subtext}{RESET}\n")

def _format_col(item, col_width=36):
    if not item:
        return " " * col_width
    num = item.get("num", 0)
    title = item.get("title", "")
    prefix_len = 7  # 2 spaces + 4 chars "[ X]" + 1 space
    avail = col_width - prefix_len
    padded = title[:avail].ljust(avail)
    return f"  {HOT_PINK}[{BRIGHT_MAGENTA}{num:>2}{HOT_PINK}]{RESET} {WHITE}{padded}{RESET}"

def render_menu(items, prompt_tag="aqxilorcore"):
    mid = (len(items) + 1) // 2
    left_col = items[:mid]
    right_col = items[mid:]
    col_width = 36
    inner_width = col_width * 2 + 1  # 73 visible characters

    print(f"{HOT_PINK}╭{'─' * inner_width}╮{RESET}")
    max_rows = max(len(left_col), len(right_col))
    for i in range(max_rows):
        l_item = left_col[i] if i < len(left_col) else None
        r_item = right_col[i] if i < len(right_col) else None

        l_str = _format_col(l_item, col_width)
        r_str = _format_col(r_item, col_width)

        print(f"{HOT_PINK}│{RESET}{l_str}{HOT_PINK}│{RESET}{r_str}{HOT_PINK}│{RESET}")

    print(f"{HOT_PINK}╰{'─' * inner_width}╯{RESET}\n")
    return f"{RED}({prompt_tag}){RESET} {WHITE}Option:{RESET} "

class FastDiscordClient:
    def __init__(self, config):
        self.config = config
        self.user_agent = config.get("settings", {}).get("user_agent", "Mozilla/5.0 Chrome/131.0.0.0")
        self.session = None

    async def get_session(self):
        if self.session is None or self.session.closed:
            connector = aiohttp.TCPConnector(limit=0, ttl_dns_cache=300, keepalive_timeout=60, ssl=False)
            self.session = aiohttp.ClientSession(connector=connector, headers={"User-Agent": self.user_agent})
        return self.session

    async def pre_warm(self):
        t0 = time.perf_counter_ns()
        session = await self.get_session()
        try:
            async with session.get("https://discord.com/api/v9/gateway") as r:
                await r.read()
                return {"success": True, "latency_ms": round((time.perf_counter_ns() - t0) / 1_000_000, 2)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def ping_discord(self):
        t0 = time.perf_counter_ns()
        session = await self.get_session()
        try:
            async with session.get("https://discord.com/api/v9/experiments") as r:
                await r.read()
                return round((time.perf_counter_ns() - t0) / 1_000_000, 2)
        except Exception:
            return None

    async def solve_mfa_ticket(self, token, ticket, methods):
        totp_secret = self.config.get("tokens", {}).get("two_factor_secret")
        password = self.config.get("tokens", {}).get("account_password")
        
        session = await self.get_session()
        mfa_url = "https://discord.com/api/v9/mfa/finish"
        headers = {"Authorization": token, "Content-Type": "application/json", "User-Agent": self.user_agent}

        method_types = [m.get("type") if isinstance(m, dict) else m for m in (methods or [])]
        if "totp" in method_types or totp_secret:
            if totp_secret:
                try:
                    import pyotp
                    code = pyotp.TOTP(totp_secret.replace(" ", "")).now()
                    payload = {"mfa_type": "totp", "data": code, "ticket": ticket}
                    async with session.post(mfa_url, headers=headers, json=payload) as resp:
                        resp_data = await resp.json()
                        if resp.status == 200:
                            print(f"{GREEN}[✓] 2FA TOTP Verified instantly via pyotp (Code: {code})!{RESET}")
                            return resp_data.get("token") or ticket
                        else:
                            print(f"{RED}[!] TOTP Challenge Failed: {resp_data.get('message')}{RESET}")
                except Exception as e:
                    print(f"{RED}[!] pyotp error: {e}{RESET}")

        if password:
            payload = {"mfa_type": "password", "data": password, "ticket": ticket}
            try:
                async with session.post(mfa_url, headers=headers, json=payload) as resp:
                    resp_data = await resp.json()
                    if resp.status == 200:
                        print(f"{GREEN}[✓] Password Verified! MFA Token received.{RESET}")
                        return resp_data.get("token") or ticket
                    else:
                        code = resp_data.get("code")
                        print(f"{RED}[!] Discord Password Check Failed: {resp_data.get('message')} (Code: {code}){RESET}")
            except Exception as e:
                print(f"{RED}[!] Error connecting to MFA endpoint: {e}{RESET}")

        print(f"\n{YELLOW}[🔐 DISCORD 2FA / SECURITY CHALLENGE DETECTED]{RESET}")
        print(f"{WHITE}Discord requires MFA elevation to authorize vanity URL changes.{RESET}")
        print(f"{GRAY}Allowed methods: {method_types}{RESET}")
        try:
            val = input(f"{CYAN}Enter 2FA Secret Key, 6-digit Code, or Account Password: {RESET}").strip()
            if not val:
                return None
            
            clean = val.replace(" ", "")
            if clean.isdigit() and len(clean) == 6:
                payload = {"mfa_type": "totp", "data": clean, "ticket": ticket}
            elif "totp" in method_types and len(clean) in (16, 26, 32):
                import pyotp
                self.config["tokens"]["two_factor_secret"] = clean
                code = pyotp.TOTP(clean).now()
                payload = {"mfa_type": "totp", "data": code, "ticket": ticket}
            else:
                self.config["tokens"]["account_password"] = val
                payload = {"mfa_type": "password", "data": val, "ticket": ticket}

            try:
                save_config(self.config)
            except Exception:
                pass

            async with session.post(mfa_url, headers=headers, json=payload) as resp:
                resp_data = await resp.json()
                if resp.status == 200:
                    print(f"{GREEN}[✓] Challenge solved! Vanity claiming now...{RESET}")
                    return resp_data.get("token") or ticket
                else:
                    print(f"{RED}[!] Challenge failed: {resp_data}{RESET}")
        except Exception as e:
            print(f"{RED}[!] Prompt error: {e}{RESET}")

        return None

    async def claim_vanity(self, token, guild_id, vanity_code, mfa_token=None):
        session = await self.get_session()
        url = f"https://discord.com/api/v9/guilds/{guild_id}/vanity-url"
        raw_body = b'{"code":"' + vanity_code.encode("utf-8") + b'"}'
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "Content-Length": str(len(raw_body)),
            "User-Agent": self.user_agent,
            "Connection": "keep-alive"
        }
        if mfa_token:
            headers["X-Discord-MFA"] = mfa_token
            headers["X-Discord-MFA-Ticket"] = mfa_token
            headers["Cookie"] = f"__Secure-recent_mfa={mfa_token}"

        t0 = time.perf_counter_ns()
        try:
            async with session.patch(url, data=raw_body, headers=headers) as r:
                text = await r.text()
                lat = round((time.perf_counter_ns() - t0) / 1_000_000, 2)
                try: data = json.loads(text)
                except Exception: data = {"raw": text}

                # Auto-solve 60003 Two-Factor challenge
                if r.status == 401 and data.get("code") == 60003 and data.get("mfa") and not mfa_token:
                    mfa_data = data["mfa"]
                    ticket = mfa_data.get("ticket")
                    methods = mfa_data.get("methods", [])
                    print(f"\n{YELLOW}[*] Two-factor elevation required by Discord. Solving MFA ticket...{RESET}")
                    solved_mfa = await self.solve_mfa_ticket(token, ticket, methods)
                    if solved_mfa:
                        print(f"{GREEN}[✓] MFA ticket solved! Resubmitting claim...{RESET}")
                        return await self.claim_vanity(token, guild_id, vanity_code, mfa_token=solved_mfa)
                    else:
                        print(f"{RED}[!] Unable to solve MFA ticket. Please check your password.{RESET}")

                return {"status": r.status, "success": 200 <= r.status < 300, "latency_ms": lat, "data": data}
        except Exception as e:
            return {"status": 500, "success": False, "latency_ms": round((time.perf_counter_ns() - t0) / 1_000_000, 2), "error": str(e)}

    async def execute_atomic_swap(self, token_a, guild_a, dummy_code, token_b, guild_b, target_code):
        session = await self.get_session()
        url_drop = f"https://discord.com/api/v9/guilds/{guild_a}/vanity-url"
        url_claim = f"https://discord.com/api/v9/guilds/{guild_b}/vanity-url"
        body_drop = b'{"code":"' + dummy_code.encode("utf-8") + b'"}'
        body_claim = b'{"code":"' + target_code.encode("utf-8") + b'"}'
        headers_a = {"Authorization": token_a, "Content-Type": "application/json", "Connection": "keep-alive"}
        headers_b = {"Authorization": token_b, "Content-Type": "application/json", "Connection": "keep-alive"}

        t0 = time.perf_counter_ns()
        async def do_drop():
            async with session.patch(url_drop, data=body_drop, headers=headers_a) as r:
                return r.status, await r.text()
        async def do_claim():
            async with session.patch(url_claim, data=body_claim, headers=headers_b) as r:
                return r.status, await r.text()

        (s_drop, t_drop), (s_claim, t_claim) = await asyncio.gather(do_drop(), do_claim())
        total_lat = round((time.perf_counter_ns() - t0) / 1_000_000, 2)
        return {
            "drop_status": s_drop,
            "claim_status": s_claim,
            "success": 200 <= s_claim < 300,
            "total_latency_ms": total_lat,
            "drop_response": t_drop,
            "claim_response": t_claim
        }

    async def check_vanity(self, vanity_code):
        session = await self.get_session()
        url = f"https://discord.com/api/v9/invites/{vanity_code}"
        t0 = time.perf_counter_ns()
        try:
            async with session.get(url) as r:
                text = await r.text()
                lat = round((time.perf_counter_ns() - t0) / 1_000_000, 2)
                try: data = json.loads(text)
                except Exception: data = {}
                return {"status": r.status, "available": r.status == 404, "latency_ms": lat, "guild": data.get("guild")}
        except Exception as e:
            return {"available": False, "error": str(e), "latency_ms": 0}

    async def get_guild(self, token, guild_id):
        session = await self.get_session()
        url = f"https://discord.com/api/v9/guilds/{guild_id}?with_counts=true"
        try:
            async with session.get(url, headers={"Authorization": token, "User-Agent": self.user_agent}) as r:
                return {"status": r.status, "data": await r.json()}
        except Exception as e:
            return {"status": 500, "error": str(e)}

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()

class WebhookNotifier:
    def __init__(self, url, enabled=True):
        self.url = url
        self.enabled = enabled and bool(url)

    async def send(self, embed):
        if not self.enabled or not self.url:
            return
        payload = {"username": "aqxilorcore", "embeds": [embed]}
        try:
            async with aiohttp.ClientSession() as s:
                await s.post(self.url, json=payload)
        except Exception:
            pass

class SpeedMonitor:
    def __init__(self, client):
        self.client = client
        self.history = []

    async def run_live_monitor(self):
        print(f"\n{HOT_PINK}════════════════════════════════════════════════════════════════════{RESET}")
        print(f"{BRIGHT_MAGENTA}⚡ LIVE DISCORD SPEED MONITOR (Press CTRL+C to stop) ⚡{RESET}")
        print(f"{HOT_PINK}════════════════════════════════════════════════════════════════════{RESET}\n")
        self.history.clear()
        try:
            while True:
                p = await self.client.ping_discord()
                if p is not None:
                    self.history.append(p)
                    if len(self.history) > 30: self.history.pop(0)
                    avg_p = round(sum(self.history)/len(self.history), 2)
                    tag = f"{GREEN}⚡ [INSANE]{RESET}" if p < 40 else (f"{CYAN}🚀 [FAST]{RESET}" if p < 90 else f"{YELLOW}🏎️  [OK]{RESET}")
                    sys.stdout.write(f"\r{HOT_PINK}[SPEED]{RESET} Current: {WHITE}{str(p).rjust(6)} ms{RESET} | Avg: {CYAN}{str(avg_p).rjust(6)} ms{RESET} | Min: {GREEN}{str(min(self.history)).rjust(6)} ms{RESET} | {tag} ")
                    sys.stdout.flush()
                await asyncio.sleep(0.4)
        except (KeyboardInterrupt, asyncio.CancelledError):
            print(f"\n{HOT_PINK}════════════════════════════════════════════════════════════════════{RESET}\n")

async def run_sniper(client, webhook, config):
    token = config.get("tokens", {}).get("sniper_token")
    guild = config.get("guilds", {}).get("target_guild_id")
    vanity = config.get("vanity", {}).get("target_vanity")
    if not token or "TOKEN" in token or not guild or "TARGET" in guild or not vanity:
        print(f"\n{RED}[ERROR] Please configure tokens and IDs first via Option [5]!{RESET}")
        return

    print(f"\n{HOT_PINK}════════════════════════════════════════════════════════════════════{RESET}")
    print(f"{BRIGHT_MAGENTA}⚡ STARTING FAST DISCORD VANITY SNIPER ⚡{RESET}")
    print(f"{WHITE}Target: {GREEN}discord.gg/{vanity}{RESET} | Guild: {CYAN}{guild}{RESET}")
    print(f"{HOT_PINK}════════════════════════════════════════════════════════════════════{RESET}\n")

    sys.stdout.write(f"{YELLOW}[*] Pre-warming TLS keep-alive socket... {RESET}")
    sys.stdout.flush()
    w = await client.pre_warm()
    print(f"{GREEN}WARMED ({w.get('latency_ms', 0)} ms){RESET}" if w.get("success") else f"{RED}FAILED{RESET}")

    init_check = await client.check_vanity(vanity)
    if init_check.get("available"):
        print(f"\n{GREEN}[!] Vanity is already available! Claiming immediately...{RESET}")
        res = await client.claim_vanity(token, guild, vanity)
        print(f"{GREEN}SUCCESS in {res['latency_ms']} ms!{RESET}" if res['success'] else f"{RED}FAILED: {res}{RESET}")
        return

    print(f"{YELLOW}[*] Watchdog loop active. Press CTRL+C to stop.{RESET}")
    checks = 0
    try:
        while True:
            await asyncio.sleep(2.0)
            checks += 1
            c = await client.check_vanity(vanity)
            if c.get("available"):
                print(f"\n{GREEN}[🎯 TRIGGER] Vanity {vanity} is now free!{RESET}")
                res = await client.claim_vanity(token, guild, vanity)
                print(f"{GREEN}🎉 VANITY SNIPED IN {res['latency_ms']} MS!{RESET}" if res['success'] else f"{RED}Claim failed: {res}{RESET}")
                break
            else:
                sys.stdout.write(f"\r{HOT_PINK}[SNIPING]{RESET} Target: {WHITE}{vanity}{RESET} | Checks: {YELLOW}{checks}{RESET} | Speed: {GREEN}{c.get('latency_ms', 0)} ms{RESET} ")
                sys.stdout.flush()
    except (KeyboardInterrupt, asyncio.CancelledError):
        print(f"\n{YELLOW}[!] Sniper stopped.{RESET}")

async def run_swapper(client, webhook, config):
    tokens = config.get("tokens", {})
    t_a = tokens.get("swapper_token_a") or tokens.get("sniper_token")
    t_b = tokens.get("swapper_token_b") or tokens.get("sniper_token")
    g_a = config.get("guilds", {}).get("source_guild_id")
    g_b = config.get("guilds", {}).get("destination_guild_id")
    vanity = config.get("vanity", {}).get("target_vanity")
    dummy = config.get("vanity", {}).get("dummy_vanity", "swap_temp_9821")

    if not t_a or "TOKEN" in t_a or not g_a or "SOURCE" in g_a or not g_b or "DESTINATION" in g_b:
        print(f"\n{RED}[ERROR] Please configure swapper tokens and guilds via Option [5]!{RESET}")
        return

    print(f"\n{HOT_PINK}════════════════════════════════════════════════════════════════════{RESET}")
    print(f"{BRIGHT_MAGENTA}🔁 ATOMIC ZERO-GAP VANITY SWAPPER 🔁{RESET}")
    print(f"{WHITE}Transferring: {GREEN}discord.gg/{vanity}{RESET} ({CYAN}{g_a} ➔ {g_b}{RESET})")
    print(f"{HOT_PINK}════════════════════════════════════════════════════════════════════{RESET}\n")

    sys.stdout.write(f"{YELLOW}[*] Pre-warming sockets... {RESET}")
    sys.stdout.flush()
    await client.pre_warm()
    print(f"{GREEN}READY!{RESET}")

    print(f"{BRIGHT_MAGENTA}⚡ Executing concurrent pipelined swap...{RESET}")
    res = await client.execute_atomic_swap(t_a, g_a, dummy, t_b, g_b, vanity)
    if res['success']:
        print(f"\n{GREEN}🎉 🎉 🎉 [SUCCESS] SWAPPED IN {res['total_latency_ms']} MS! 🎉 🎉 🎉{RESET}")
    else:
        print(f"\n{RED}[✗] Swap failed! Drop: {res['drop_status']}, Claim: {res['claim_status']} ({res['total_latency_ms']} ms){RESET}")

def run_config_editor(cfg):
    while True:
        tokens = cfg.get("tokens", {})
        guilds = cfg.get("guilds", {})
        vanity = cfg.get("vanity", {})
        print(f"\n{HOT_PINK}╭─────────────────────────────────────────────────────────────────────────────╮{RESET}")
        print(f"{HOT_PINK}│{RESET}  {BRIGHT_MAGENTA}⚙️  CONFIG EDITOR (Saves to config.json){RESET}{' ' * 33}{HOT_PINK}│{RESET}")
        print(f"{HOT_PINK}├─────────────────────────────────────────────────────────────────────────────┤{RESET}")
        print(f"{HOT_PINK}│{RESET}  [ 1] Sniper Token        : {GRAY}{mask_token(tokens.get('sniper_token'))}{RESET}")
        print(f"{HOT_PINK}│{RESET}  [ 2] Account Password    : {YELLOW}{mask_password(tokens.get('account_password'))}{RESET}")
        print(f"{HOT_PINK}│{RESET}  [ 3] Swapper Token A     : {GRAY}{mask_token(tokens.get('swapper_token_a'))}{RESET}")
        print(f"{HOT_PINK}│{RESET}  [ 4] Swapper Token B     : {GRAY}{mask_token(tokens.get('swapper_token_b'))}{RESET}")
        print(f"{HOT_PINK}│{RESET}  [ 5] Target Guild ID     : {CYAN}{guilds.get('target_guild_id')}{RESET}")
        print(f"{HOT_PINK}│{RESET}  [ 6] Source Guild ID     : {CYAN}{guilds.get('source_guild_id')}{RESET}")
        print(f"{HOT_PINK}│{RESET}  [ 7] Destination Guild ID: {CYAN}{guilds.get('destination_guild_id')}{RESET}")
        print(f"{HOT_PINK}│{RESET}  [ 8] Target Vanity Code  : {GREEN}discord.gg/{vanity.get('target_vanity')}{RESET}")
        print(f"{HOT_PINK}│{RESET}  [ 0] Back to Main Menu")
        print(f"{HOT_PINK}╰─────────────────────────────────────────────────────────────────────────────╯{RESET}\n")

        opt = input(f"{RED}(config){RESET} {WHITE}Select item (0-8): {RESET}").strip()
        if opt == "0": break
        elif opt == "1":
            v = input(f"{CYAN}Enter Sniper Token: {RESET}").strip()
            if v: tokens["sniper_token"] = v; save_config(cfg)
        elif opt == "2":
            v = input(f"{CYAN}Enter Account Password (for 2FA bypass): {RESET}").strip()
            tokens["account_password"] = v; save_config(cfg)
            print(f"{GREEN}✓ Password saved! Auto-MFA is now active.{RESET}")
        elif opt == "3":
            v = input(f"{CYAN}Enter Token A: {RESET}").strip()
            if v: tokens["swapper_token_a"] = v; save_config(cfg)
        elif opt == "4":
            v = input(f"{CYAN}Enter Token B: {RESET}").strip()
            if v: tokens["swapper_token_b"] = v; save_config(cfg)
        elif opt == "5":
            v = input(f"{CYAN}Enter Target Guild ID: {RESET}").strip()
            if v: guilds["target_guild_id"] = v; save_config(cfg)
        elif opt == "6":
            v = input(f"{CYAN}Enter Source Guild ID: {RESET}").strip()
            if v: guilds["source_guild_id"] = v; save_config(cfg)
        elif opt == "7":
            v = input(f"{CYAN}Enter Destination Guild ID: {RESET}").strip()
            if v: guilds["destination_guild_id"] = v; save_config(cfg)
        elif opt == "8":
            v = input(f"{CYAN}Enter Vanity Code: {RESET}").strip()
            if v: vanity["target_vanity"] = v.replace("https://discord.gg/", "").replace("discord.gg/", ""); save_config(cfg)

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
    cfg = load_config()
    client = FastDiscordClient(cfg)
    webhook = WebhookNotifier(cfg.get("webhook", {}).get("url"), cfg.get("webhook", {}).get("enabled", True))
    monitor = SpeedMonitor(client)
    asyncio.create_task(client.pre_warm())

    try:
        while True:
            render_banner("aqxior")
            prompt = render_menu(MENU_ITEMS, prompt_tag="aqxilorcore")
            choice = input(prompt).strip()

            if choice == "1":
                await run_sniper(client, webhook, cfg)
                input(f"\n{GRAY}Press Enter...{RESET}")
            elif choice == "2":
                await run_swapper(client, webhook, cfg)
                input(f"\n{GRAY}Press Enter...{RESET}")
            elif choice == "3":
                token = cfg.get("tokens", {}).get("sniper_token")
                guild = cfg.get("guilds", {}).get("target_guild_id")
                res = await client.get_guild(token, guild)
                print(f"\n{res}\n")
                input(f"\n{GRAY}Press Enter...{RESET}")
            elif choice == "4":
                await monitor.run_live_monitor()
                input(f"\n{GRAY}Press Enter...{RESET}")
            elif choice == "5":
                run_config_editor(cfg)
            elif choice == "6":
                print(f"{YELLOW}Testing webhook...{RESET}")
                await webhook.send({"title": "aqxilorcore Alert", "description": "Connection verified!"})
                input(f"\n{GRAY}Press Enter...{RESET}")
            elif choice == "7":
                code = input(f"{CYAN}Enter vanity: {RESET}").strip()
                res = await client.check_vanity(code)
                print(f"Status: {res}")
                input(f"\n{GRAY}Press Enter...{RESET}")
            elif choice == "8":
                print(f"{YELLOW}Testing 5 ping samples...{RESET}")
                for i in range(5):
                    print(f"  #{i+1}: {await client.ping_discord()} ms")
                    await asyncio.sleep(0.3)
                input(f"\n{GRAY}Press Enter...{RESET}")
            elif choice == "9":
                print(json.dumps(cfg, indent=2))
                input(f"\n{GRAY}Press Enter...{RESET}")
            elif choice == "10":
                await client.close()
                sys.exit(0)
    except KeyboardInterrupt:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
