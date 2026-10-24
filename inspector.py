import sys
import asyncio
from ui import HOT_PINK, BRIGHT_MAGENTA, GREEN, YELLOW, RED, CYAN, WHITE, GRAY, RESET

async def inspect_guild(client, config):
    tokens = config.get("tokens", {})
    token = tokens.get("sniper_token") or tokens.get("swapper_token_b")
    guild_id = config.get("guilds", {}).get("target_guild_id")

    if not token or "TOKEN" in token:
        print(f"{RED}Please configure sniper_token first! (Option [5]){RESET}")
        return
    if not guild_id or "TARGET" in guild_id:
        print(f"{RED}Please configure target_guild_id first! (Option [5]){RESET}")
        return

    print(f"\n{YELLOW}[*] Querying Guild Details for {guild_id}...{RESET}")
    res = await client.get_guild(token, guild_id)

    if res.get("status") == 200:
        g = res.get("data", {})
        features = g.get("features", [])
        has_vanity = "VANITY_URL" in features

        print(f"\n{HOT_PINK}═══ GUILD INSPECTION REPORT ═══{RESET}")
        print(f"Guild Name        : {WHITE}{g.get('name')}{RESET}")
        print(f"Guild ID          : {CYAN}{g.get('id')}{RESET}")
        print(f"Current Vanity    : {GREEN}{'discord.gg/' + g['vanity_url_code'] if g.get('vanity_url_code') else 'None'}{RESET}")
        print(f"Boost Tier / Level: {YELLOW}Tier {g.get('premium_tier', 0)}{RESET} ({g.get('premium_subscription_count', 0)} boosts)")
        print(f"Vanity Capability : {GREEN + 'ENABLED (Ready to snipe/swap) ✅' if has_vanity else RED + 'DISABLED (Requires Tier 3 / 14 boosts) ❌'}{RESET}")
        print(f"Approx Members    : {WHITE}{g.get('approximate_member_count', 'N/A')}{RESET}")
        print(f"{HOT_PINK}═══════════════════════════════{RESET}\n")
    else:
        print(f"{RED}Failed to inspect guild (HTTP {res.get('status')}): {res.get('data') or res.get('error')}{RESET}")

async def check_vanity_interactive(client):
    code = input(f"\n{CYAN}Enter Vanity Code to check (e.g. aqxilorcore): {RESET}").strip()
    clean_code = code.replace("https://discord.gg/", "").replace("discord.gg/", "").strip()
    if not clean_code:
        return

    sys.stdout.write(f"{YELLOW}[*] Querying Discord invite API... {RESET}")
    sys.stdout.flush()
    result = await client.check_vanity(clean_code)

    print(f"\n{HOT_PINK}═══ VANITY STATUS: discord.gg/{clean_code} ═══{RESET}")
    if result.get("available"):
        print(f"Status     : {GREEN}AVAILABLE TO CLAIM! 🎉{RESET}")
        print(f"HTTP Code  : {GREEN}404 (Unclaimed){RESET}")
    else:
        guild_name = result.get("guild", {}).get("name") if result.get("guild") else "Private Server"
        print(f"Status     : {RED}TAKEN / OCCUPIED ❌{RESET}")
        print(f"Server Name: {WHITE}{guild_name}{RESET}")
    print(f"Reaction   : {YELLOW}{result.get('latency_ms', 0)} ms{RESET}")
    print(f"{HOT_PINK}═════════════════════════════════════════════{RESET}\n")

async def run_jitter_benchmark(client):
    print(f"\n{YELLOW}[*] Benchmarking network ping to Discord API (10 Samples)...{RESET}\n")
    samples = []

    for i in range(1, 11):
        ping = await client.ping_discord()
        if ping is not None:
            samples.append(ping)
            print(f"  Sample #{i:2d}: {GREEN}{ping:6.2f} ms{RESET}")
        else:
            print(f"  Sample #{i:2d}: {RED}Failed / Timeout{RESET}")
        await asyncio.sleep(0.3)

    if samples:
        avg = round(sum(samples) / len(samples), 2)
        min_p = min(samples)
        max_p = max(samples)
        jitter = round(max_p - min_p, 2)

        print(f"\n{HOT_PINK}═══ SPEED BENCHMARK RESULTS ═══{RESET}")
        print(f"Min Latency  : {GREEN}{min_p} ms{RESET}")
        print(f"Avg Latency  : {YELLOW}{avg} ms{RESET}")
        print(f"Max Latency  : {RED}{max_p} ms{RESET}")
        print(f"Packet Jitter: {CYAN}{jitter} ms{RESET}")
        print(f"{HOT_PINK}═══════════════════════════════{RESET}\n")
