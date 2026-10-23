import time
import asyncio
import sys
from ui import HOT_PINK, BRIGHT_MAGENTA, GREEN, YELLOW, RED, CYAN, WHITE, GRAY, RESET

class SpeedMonitor:
    def __init__(self, client):
        self.client = client
        self.history = []

    def get_speed_tag(self, ms):
        if ms < 40:
            return f"{GREEN}⚡ [INSANE SPEED]{RESET}"
        elif ms < 90:
            return f"{CYAN}🚀 [VERY FAST]{RESET}"
        elif ms < 160:
            return f"{YELLOW}🏎️  [FAST]{RESET}"
        else:
            return f"{RED}⚠️  [HIGH LATENCY]{RESET}"

    def get_speed_bar(self, ms, max_val=200):
        length = 20
        filled = int(min(max(ms / max_val, 0), 1.0) * length)
        empty = length - filled
        bar = f"{GREEN}{'█' * (length - filled)}{YELLOW}{'░' * filled}{RESET}"
        return f"[{bar}]"

    async def run_live_monitor(self, duration_sec=None):
        """Runs an interactive live latency & socket monitor in the terminal"""
        print(f"\n{HOT_PINK}════════════════════════════════════════════════════════════════════{RESET}")
        print(f"{BRIGHT_MAGENTA}⚡ LIVE DISCORD API & GATEWAY SPEED MONITOR ⚡{RESET}")
        print(f"{WHITE}Measuring round-trip socket latency in real-time... Press CTRL+C to stop.{RESET}")
        print(f"{HOT_PINK}════════════════════════════════════════════════════════════════════{RESET}\n")

        self.history.clear()
        start_time = time.time()

        try:
            while True:
                if duration_sec and (time.time() - start_time) > duration_sec:
                    break

                t0 = time.perf_counter_ns()
                ping_ms = await self.client.ping_discord()
                t1 = time.perf_counter_ns()

                if ping_ms is not None:
                    self.history.append(ping_ms)
                    if len(self.history) > 50:
                        self.history.pop(0)

                    min_p = min(self.history)
                    max_p = max(self.history)
                    avg_p = round(sum(self.history) / len(self.history), 2)
                    jitter = round(abs(ping_ms - avg_p), 2)
                    tag = self.get_speed_tag(ping_ms)

                    status_line = (
                        f"\r{HOT_PINK}[SPEED]{RESET} Current: {WHITE}{str(ping_ms).rjust(6)} ms{RESET} | "
                        f"Avg: {CYAN}{str(avg_p).rjust(6)} ms{RESET} | "
                        f"Min: {GREEN}{str(min_p).rjust(6)} ms{RESET} | "
                        f"Jitter: {YELLOW}{str(jitter).rjust(5)} ms{RESET} | "
                        f"{tag} "
                    )
                    sys.stdout.write(status_line)
                    sys.stdout.flush()
                else:
                    sys.stdout.write(f"\r{RED}[SPEED] Connection Dropped / Packet Timeout...{RESET}")
                    sys.stdout.flush()

                await asyncio.sleep(0.4)

        except (KeyboardInterrupt, asyncio.CancelledError):
            pass

        print(f"\n\n{HOT_PINK}═══ SPEED BENCHMARK SUMMARY ═══{RESET}")
        if self.history:
            print(f"Total Samples Recorded : {WHITE}{len(self.history)}{RESET}")
            print(f"Fastest Reaction Ping  : {GREEN}{min(self.history)} ms{RESET}")
            print(f"Average Network Latency: {YELLOW}{round(sum(self.history) / len(self.history), 2)} ms{RESET}")
            print(f"Max Latency Spike      : {RED}{max(self.history)} ms{RESET}")
        print(f"{HOT_PINK}════════════════════════════════{RESET}\n")
