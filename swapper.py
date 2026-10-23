import sys
from ui import HOT_PINK, BRIGHT_MAGENTA, GREEN, YELLOW, RED, CYAN, WHITE, GRAY, RESET

class VanitySwapper:
    def __init__(self, client, webhook, config):
        self.client = client
        self.webhook = webhook
        self.config = config

    async def start(self):
        tokens = self.config.get("tokens", {})
        token_a = tokens.get("swapper_token_a") or tokens.get("sniper_token")
        token_b = tokens.get("swapper_token_b") or tokens.get("sniper_token")
        guild_a = self.config.get("guilds", {}).get("source_guild_id")
        guild_b = self.config.get("guilds", {}).get("destination_guild_id")
        target_vanity = self.config.get("vanity", {}).get("target_vanity")
        dummy_vanity = self.config.get("vanity", {}).get("dummy_vanity", "temp_swap_9821")

        if not token_a or "TOKEN" in token_a:
            print(f"\n{RED}[ERROR] Valid swapper_token_a required in config! Use Option [5].{RESET}")
            return
        if not token_b or "TOKEN" in token_b:
            print(f"\n{RED}[ERROR] Valid swapper_token_b required in config! Use Option [5].{RESET}")
            return
        if not guild_a or "SOURCE" in guild_a:
            print(f"\n{RED}[ERROR] Valid source_guild_id required in config! Use Option [5].{RESET}")
            return
        if not guild_b or "DESTINATION" in guild_b:
            print(f"\n{RED}[ERROR] Valid destination_guild_id required in config! Use Option [5].{RESET}")
            return
        if not target_vanity:
            print(f"\n{RED}[ERROR] Valid target_vanity required in config!{RESET}")
            return

        print(f"\n{HOT_PINK}════════════════════════════════════════════════════════════════════{RESET}")
        print(f"{BRIGHT_MAGENTA}🔁 STARTING ATOMIC ZERO-GAP PYTHON VANITY SWAPPER 🔁{RESET}")
        print(f"{WHITE}Transferring  : {GREEN}discord.gg/{target_vanity}{RESET}")
        print(f"{WHITE}Source Guild  : {CYAN}{guild_a}{RESET}")
        print(f"{WHITE}Dest Guild    : {CYAN}{guild_b}{RESET}")
        print(f"{WHITE}Dummy Vanity  : {YELLOW}{dummy_vanity}{RESET}")
        print(f"{HOT_PINK}════════════════════════════════════════════════════════════════════{RESET}\n")

        # 1. Pre-warm TCP & TLS 1.3 socket
        sys.stdout.write(f"{YELLOW}[*] Pre-warming TLS 1.3 keep-alive sockets... {RESET}")
        sys.stdout.flush()
        warm = await self.client.pre_warm()
        if warm.get("success"):
            print(f"{GREEN}WARMED ({warm['latency_ms']} ms){RESET}")
        else:
            print(f"{RED}FAILED ({warm.get('error')}){RESET}")

        # 2. Check destination guild vanity feature
        sys.stdout.write(f"{YELLOW}[*] Verifying Destination Guild boost & vanity capability... {RESET}")
        sys.stdout.flush()
        dest_check = await self.client.get_guild(token_b, guild_b)
        if dest_check.get("status") == 200:
            g = dest_check.get("data", {})
            features = g.get("features", [])
            if "VANITY_URL" in features:
                print(f"{GREEN}VERIFIED (VANITY_URL enabled ✅){RESET}")
            else:
                print(f"\n{RED}[⚠️ WARNING] Destination guild lacks VANITY_URL feature! (Needs Level 3 / 14 boosts){RESET}")
        else:
            print(f"{YELLOW}Could not verify boost status (HTTP {dest_check.get('status')}), proceeding...{RESET}")

        # 3. Fire Atomic Pipelined Swap
        print(f"\n{BRIGHT_MAGENTA}⚡ FIRING ATOMIC ZERO-GAP SWAP NOW...{RESET}")
        result = await self.client.execute_atomic_swap(
            token_a, guild_a, dummy_vanity,
            token_b, guild_b, target_vanity
        )

        print(f"\n{HOT_PINK}════════════════════════════════════════════════════════════════════{RESET}")
        if result.get("success"):
            lat = result.get("total_latency_ms", 0)
            print(f"{GREEN}🎉 🎉 🎉 [SUCCESS] VANITY SWAPPED IN {lat} MS! 🎉 🎉 🎉{RESET}")
            print(f"{WHITE}Vanity URL   : {GREEN}discord.gg/{target_vanity}{RESET}")
            print(f"{WHITE}Transferred  : {CYAN}{guild_a} ➔ {guild_b}{RESET}")
            print(f"{WHITE}Reaction Gap : {YELLOW}{lat} ms{RESET}")
            print(f"{WHITE}Server A Drop: {GREEN}HTTP {result['drop_status']}{RESET}")
            print(f"{WHITE}Server B Get : {GREEN}HTTP {result['claim_status']}{RESET}")

            if self.webhook:
                await self.webhook.send_swap_success(target_vanity, guild_a, guild_b, lat)
        else:
            lat = result.get("total_latency_ms", 0)
            print(f"{RED}[✗] Swap Incomplete or Failed!{RESET}")
            print(f"{WHITE}Server A Drop Status : {result['drop_status']} ({result['drop_response']}){RESET}")
            print(f"{WHITE}Server B Claim Status: {result['claim_status']} ({result['claim_response']}){RESET}")
            print(f"{WHITE}Latency Elapsed      : {lat} ms{RESET}")

            if self.webhook:
                await self.webhook.send_alert("Swap Failed", f"Drop: {result['drop_status']}\nClaim: {result['claim_status']}", is_error=True)
        print(f"{HOT_PINK}════════════════════════════════════════════════════════════════════{RESET}\n")
