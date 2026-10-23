import json
import asyncio
import sys
import aiohttp
from ui import HOT_PINK, BRIGHT_MAGENTA, GREEN, YELLOW, RED, CYAN, WHITE, GRAY, RESET

class VanitySniper:
    def __init__(self, client, webhook, config):
        self.client = client
        self.webhook = webhook
        self.config = config
        self.is_running = False
        self.checks_count = 0
        self.last_speed_ms = 0.0

    async def start(self):
        token = self.config.get("tokens", {}).get("sniper_token")
        target_guild = self.config.get("guilds", {}).get("target_guild_id")
        target_vanity = self.config.get("vanity", {}).get("target_vanity")

        if not token or "YOUR_DISCORD_TOKEN" in token:
            print(f"\n{RED}[ERROR] Valid sniper_token required in config! Use Option [5] to set it.{RESET}")
            return
        if not target_guild or "YOUR_TARGET" in target_guild:
            print(f"\n{RED}[ERROR] Valid target_guild_id required in config! Use Option [5] to set it.{RESET}")
            return
        if not target_vanity:
            print(f"\n{RED}[ERROR] Valid target_vanity required in config!{RESET}")
            return

        print(f"\n{HOT_PINK}════════════════════════════════════════════════════════════════════{RESET}")
        print(f"{BRIGHT_MAGENTA}⚡ STARTING ULTRA-FAST PYTHON DISCORD VANITY SNIPER ⚡{RESET}")
        print(f"{WHITE}Target Vanity : {GREEN}discord.gg/{target_vanity}{RESET}")
        print(f"{WHITE}Target Guild  : {CYAN}{target_guild}{RESET}")
        print(f"{HOT_PINK}════════════════════════════════════════════════════════════════════{RESET}\n")

        # 1. Pre-warm TCP & TLS 1.3 socket
        sys.stdout.write(f"{YELLOW}[*] Pre-warming TLS 1.3 keep-alive socket to discord.com... {RESET}")
        sys.stdout.flush()
        warm = await self.client.pre_warm()
        if warm.get("success"):
            self.last_speed_ms = warm["latency_ms"]
            print(f"{GREEN}WARMED ({warm['latency_ms']} ms){RESET}")
        else:
            print(f"{RED}FAILED ({warm.get('error')}){RESET}")

        # 2. Check initial vanity status
        sys.stdout.write(f"{YELLOW}[*] Checking current vanity status... {RESET}")
        sys.stdout.flush()
        initial = await self.client.check_vanity(target_vanity)
        if initial.get("available"):
            print(f"{GREEN}VANITY IS ALREADY AVAILABLE! CLAIMING IMMEDIATELY...{RESET}")
            await self.execute_claim()
            return
        else:
            guild_name = initial.get("guild", {}).get("name", "Unknown Server") if initial.get("guild") else "Occupied"
            print(f"{GRAY}Occupied by [{guild_name}] ({initial.get('latency_ms', 0)} ms){RESET}")

        self.is_running = True
        print(f"\n{YELLOW}[*] Connecting to Discord Gateway v10 WebSocket...{RESET}")
        print(f"{GRAY}Press CTRL+C anytime to stop sniper.{RESET}\n")

        # Run Gateway listener & Watchdog concurrently
        try:
            await asyncio.gather(
                self.gateway_loop(token, target_vanity),
                self.watchdog_loop(target_vanity)
            )
        except (KeyboardInterrupt, asyncio.CancelledError):
            self.is_running = False
            print(f"\n{YELLOW}[!] Sniper stopped by user.{RESET}")

    async def gateway_loop(self, token, target_vanity):
        """Maintains persistent WebSocket connection to Discord Gateway for 0ms GUILD_UPDATE dispatch"""
        session = await self.client.get_session()
        gateway_url = "wss://gateway.discord.gg/?v=10&encoding=json"

        while self.is_running:
            try:
                async with session.ws_connect(gateway_url) as ws:
                    # Identify
                    identify_payload = {
                        "op": 2,
                        "d": {
                            "token": token,
                            "intents": 1, # GUILDS
                            "properties": {
                                "os": sys.platform,
                                "browser": "Chrome",
                                "device": ""
                            }
                        }
                    }

                    heartbeat_task = None
                    async for msg in ws:
                        if not self.is_running:
                            break
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            data = json.loads(msg.data)
                            op = data.get("op")
                            t = data.get("t")
                            d = data.get("d")

                            if op == 10: # Hello
                                hb_interval = d["heartbeat_interval"] / 1000.0
                                heartbeat_task = asyncio.create_task(self.heartbeat_loop(ws, hb_interval))
                                await ws.send_json(identify_payload)

                            elif t == "READY":
                                user = d.get("user", {})
                                username = user.get("username", "Sniper")
                                print(f"{GREEN}[✓] Gateway Authenticated as: {WHITE}{username}{RESET}")
                                print(f"{BRIGHT_MAGENTA}[⚡] Gateway Active - Monitoring real-time GUILD_UPDATE packets...{RESET}")

                            elif t == "GUILD_UPDATE":
                                # Instant trigger!
                                if d.get("vanity_url_code") != target_vanity:
                                    print(f"\n{YELLOW}[🔔 GATEWAY PACKET DETECTED] Guild {d.get('id')} dropped/changed vanity!{RESET}")
                                    await self.execute_claim()
                                    return

                        elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                            break

                    if heartbeat_task:
                        heartbeat_task.cancel()

            except Exception as e:
                if self.is_running:
                    await asyncio.sleep(2)

    async def heartbeat_loop(self, ws, interval):
        while self.is_running and not ws.closed:
            await asyncio.sleep(interval)
            try:
                await ws.send_json({"op": 1, "d": None})
            except Exception:
                break

    async def watchdog_loop(self, target_vanity):
        """Watchdog checking target vanity availability with live terminal speed readout"""
        while self.is_running:
            await asyncio.sleep(2.0)
            self.checks_count += 1
            check = await self.client.check_vanity(target_vanity)
            self.last_speed_ms = check.get("latency_ms", 0)

            if check.get("available"):
                print(f"\n{GREEN}[🎯 WATCHDOG TRIGGER] Vanity {target_vanity} is now FREE!{RESET}")
                await self.execute_claim()
                return
            else:
                status_bar = (
                    f"\r{HOT_PINK}[SNIPING]{RESET} Target: {WHITE}{target_vanity}{RESET} | "
                    f"Checks: {YELLOW}{self.checks_count}{RESET} | "
                    f"Speed: {GREEN}{self.last_speed_ms} ms{RESET} | "
                    f"Socket: {BRIGHT_MAGENTA}HOT-PREWARMED{RESET} "
                )
                sys.stdout.write(status_bar)
                sys.stdout.flush()

    async def execute_claim(self):
        token = self.config.get("tokens", {}).get("sniper_token")
        target_guild = self.config.get("guilds", {}).get("target_guild_id")
        target_vanity = self.config.get("vanity", {}).get("target_vanity")

        print(f"\n{BRIGHT_MAGENTA}⚡ DISPATCHING INSTANT CLAIM: PATCH /api/v9/guilds/{target_guild}/vanity-url ...{RESET}")
        res = await self.client.claim_vanity(token, target_guild, target_vanity)

        if res.get("success"):
            lat = res.get("latency_ms", 0)
            print(f"\n{GREEN}🎉 🎉 🎉 [SUCCESS] VANITY SNIPED IN {lat} MS! 🎉 🎉 🎉{RESET}")
            print(f"{WHITE}Vanity URL : {GREEN}discord.gg/{target_vanity}{RESET}")
            print(f"{WHITE}Guild ID   : {CYAN}{target_guild}{RESET}")
            print(f"{WHITE}Speed      : {YELLOW}{lat} ms{RESET}\n")

            if self.webhook:
                await self.webhook.send_snipe_success(target_vanity, target_guild, lat)
            self.is_running = False
        else:
            status = res.get("status")
            lat = res.get("latency_ms", 0)
            print(f"\n{RED}[✗] Claim Failed (HTTP {status}, {lat} ms): {res.get('data') or res.get('error')}{RESET}")
            if status == 429:
                print(f"{YELLOW}[!] Rate limited! Backing off...{RESET}")
