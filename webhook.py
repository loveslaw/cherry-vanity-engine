import aiohttp

class WebhookNotifier:
    def __init__(self, url, enabled=True):
        self.url = url
        self.enabled = enabled and bool(url)

    async def send(self, embed):
        if not self.enabled or not self.url:
            return

        payload = {
            "username": "🍒 Vanity Engine (Python)",
            "avatar_url": "https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f352.png",
            "embeds": [embed]
        }

        try:
            async with aiohttp.ClientSession() as session:
                await session.post(self.url, json=payload)
        except Exception:
            pass

    async def send_snipe_success(self, vanity, guild_id, latency_ms):
        await self.send({
            "title": "🎯 [SUCCESS] Vanity Sniped Instantly!",
            "color": 0xFF007F,
            "description": f"Successfully claimed **`discord.gg/{vanity}`** on target server!",
            "fields": [
                {"name": "🔗 Vanity URL", "value": f"`discord.gg/{vanity}`", "inline": True},
                {"name": "⚡ Reaction Speed", "value": f"`{latency_ms} ms`", "inline": True},
                {"name": "🏰 Guild ID", "value": f"`{guild_id}`", "inline": True}
            ],
            "footer": {"text": "Cherry Vanity Engine • Python Ultra-Fast"},
        })

    async def send_swap_success(self, vanity, source_guild, dest_guild, latency_ms):
        await self.send({
            "title": "🔁 [SUCCESS] Vanity Swapped with Zero Gap!",
            "color": 0x00FF88,
            "description": f"Successfully transferred **`discord.gg/{vanity}`**!",
            "fields": [
                {"name": "🔗 Vanity URL", "value": f"`discord.gg/{vanity}`", "inline": True},
                {"name": "⚡ Total Gap", "value": f"`{latency_ms} ms`", "inline": True},
                {"name": "📤 Source Guild", "value": f"`{source_guild}`", "inline": True},
                {"name": "📥 Dest Guild", "value": f"`{dest_guild}`", "inline": True}
            ],
            "footer": {"text": "Cherry Vanity Engine • Atomic Swapper"},
        })

    async def send_alert(self, title, message, is_error=False):
        await self.send({
            "title": f"⚠️ {title}" if is_error else f"ℹ️ {title}",
            "color": 0xFF3333 if is_error else 0x00D9FF,
            "description": message,
            "footer": {"text": "Cherry Vanity Engine"},
        })
