import time
import json
import asyncio
import aiohttp

class FastDiscordClient:
    def __init__(self, config=None):
        self.config = config or {}
        self.user_agent = self.config.get("settings", {}).get(
            "user_agent",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
        self.session = None
        self.is_warmed = False

    async def get_session(self):
        if self.session is None or self.session.closed:
            connector = aiohttp.TCPConnector(
                limit=0,
                ttl_dns_cache=300,
                keepalive_timeout=60,
                ssl=False
            )
            self.session = aiohttp.ClientSession(
                connector=connector,
                headers={"User-Agent": self.user_agent}
            )
        return self.session

    async def pre_warm(self):
        t0 = time.perf_counter_ns()
        session = await self.get_session()
        try:
            async with session.get("https://discord.com/api/v9/gateway") as resp:
                await resp.read()
                t1 = time.perf_counter_ns()
                latency_ms = (t1 - t0) / 1_000_000
                self.is_warmed = True
                return {"success": True, "latency_ms": round(latency_ms, 2)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def ping_discord(self):
        t0 = time.perf_counter_ns()
        session = await self.get_session()
        try:
            async with session.get("https://discord.com/api/v9/experiments") as resp:
                await resp.read()
                t1 = time.perf_counter_ns()
                return round((t1 - t0) / 1_000_000, 2)
        except Exception:
            return None

    async def solve_mfa_ticket(self, token, ticket, methods):
        """Automatically resolves Discord 2FA / Password challenge tickets on the fly"""
        password = self.config.get("tokens", {}).get("account_password")
        if not password:
            return None

        session = await self.get_session()
        mfa_url = "https://discord.com/api/v9/mfa/finish"
        payload = {
            "mfa_type": "password",
            "data": password,
            "ticket": ticket
        }
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": self.user_agent
        }

        try:
            async with session.post(mfa_url, headers=headers, json=payload) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("token")
        except Exception:
            pass
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

        t0 = time.perf_counter_ns()
        try:
            async with session.patch(url, data=raw_body, headers=headers) as resp:
                raw_text = await resp.text()
                t1 = time.perf_counter_ns()
                latency_ms = round((t1 - t0) / 1_000_000, 2)
                
                try:
                    data = json.loads(raw_text)
                except Exception:
                    data = {"raw": raw_text}

                # Auto-solve 60003 Two-Factor challenge if password configured
                if resp.status == 401 and data.get("code") == 60003 and data.get("mfa") and not mfa_token:
                    mfa_data = data["mfa"]
                    ticket = mfa_data.get("ticket")
                    methods = mfa_data.get("methods", [])
                    solved_mfa = await self.solve_mfa_ticket(token, ticket, methods)
                    if solved_mfa:
                        return await self.claim_vanity(token, guild_id, vanity_code, mfa_token=solved_mfa)

                return {
                    "status": resp.status,
                    "success": 200 <= resp.status < 300,
                    "latency_ms": latency_ms,
                    "data": data
                }
        except Exception as e:
            t1 = time.perf_counter_ns()
            return {
                "status": 500,
                "success": False,
                "latency_ms": round((t1 - t0) / 1_000_000, 2),
                "error": str(e)
            }

    async def execute_atomic_swap(self, token_a, guild_a, dummy_code, token_b, guild_b, target_code, mfa_token=None):
        session = await self.get_session()
        url_drop = f"https://discord.com/api/v9/guilds/{guild_a}/vanity-url"
        url_claim = f"https://discord.com/api/v9/guilds/{guild_b}/vanity-url"

        body_drop = b'{"code":"' + dummy_code.encode("utf-8") + b'"}'
        body_claim = b'{"code":"' + target_code.encode("utf-8") + b'"}'

        headers_a = {
            "Authorization": token_a,
            "Content-Type": "application/json",
            "Content-Length": str(len(body_drop)),
            "User-Agent": self.user_agent,
            "Connection": "keep-alive"
        }
        headers_b = {
            "Authorization": token_b,
            "Content-Type": "application/json",
            "Content-Length": str(len(body_claim)),
            "User-Agent": self.user_agent,
            "Connection": "keep-alive"
        }
        if mfa_token:
            headers_b["X-Discord-MFA"] = mfa_token
            headers_b["X-Discord-MFA-Ticket"] = mfa_token

        t0 = time.perf_counter_ns()

        async def do_drop():
            async with session.patch(url_drop, data=body_drop, headers=headers_a) as r:
                return r.status, await r.text()

        async def do_claim():
            async with session.patch(url_claim, data=body_claim, headers=headers_b) as r:
                return r.status, await r.text()

        (status_drop, text_drop), (status_claim, text_claim) = await asyncio.gather(
            do_drop(), do_claim()
        )
        t1 = time.perf_counter_ns()
        total_latency_ms = round((t1 - t0) / 1_000_000, 2)

        return {
            "drop_status": status_drop,
            "claim_status": status_claim,
            "success": 200 <= status_claim < 300,
            "total_latency_ms": total_latency_ms,
            "drop_response": text_drop,
            "claim_response": text_claim
        }

    async def check_vanity(self, vanity_code):
        session = await self.get_session()
        url = f"https://discord.com/api/v9/invites/{vanity_code}"
        
        t0 = time.perf_counter_ns()
        try:
            async with session.get(url) as resp:
                raw_text = await resp.text()
                t1 = time.perf_counter_ns()
                latency_ms = round((t1 - t0) / 1_000_000, 2)

                try:
                    data = json.loads(raw_text)
                except Exception:
                    data = {}

                return {
                    "status": resp.status,
                    "available": resp.status == 404,
                    "latency_ms": latency_ms,
                    "guild": data.get("guild"),
                    "expires_at": data.get("expires_at")
                }
        except Exception as e:
            return {"available": False, "error": str(e), "latency_ms": 0}

    async def get_guild(self, token, guild_id):
        session = await self.get_session()
        url = f"https://discord.com/api/v9/guilds/{guild_id}?with_counts=true"
        headers = {"Authorization": token, "User-Agent": self.user_agent}
        try:
            async with session.get(url, headers=headers) as resp:
                data = await resp.json()
                return {"status": resp.status, "data": data}
        except Exception as e:
            return {"status": 500, "error": str(e)}

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
