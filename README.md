# ⚡ aqxilorcore

Ultra-Fast, Asynchronous Discord Vanity Sniper & Atomic Swapper written natively in **Python 3** with live terminal speed monitoring, TLS 1.3 keep-alive connection pooling, and the signature hot-pink / magenta terminal UI.

---

## ✨ Features

- **⚡ Sub-Millisecond Local Execution**:
  - `aiohttp` non-blocking async event loop with persistent `TCPConnector(limit=0, keepalive_timeout=60)`.
  - Sockets are pre-warmed before trigger so zero DNS/SSL handshake latency is incurred.
  - Pre-encoded Byte Buffers in RAM to eliminate JSON serialization overhead.
- **📊 Real-Time Terminal Speed Monitoring**:
  - Live socket latency gauge, continuous ping tracking, and moving average/min/max/jitter statistics.
- **🎯 Dual Mode (Sniper & Swapper in One)**:
  - **Gateway Sniper**: Real-time Discord WebSocket (v10) listener catching `GUILD_UPDATE` event packets.
  - **Atomic Swapper**: Simultaneous Server A drop and Server B claim with near-zero gap.
- **⚙️ Live In-App Config Editor**:
  - Option `[ 5]` allows editing tokens, guild IDs, vanities, and webhook URLs directly in the terminal and auto-saves to `config.json`.
- **💻 Cross-Platform**:
  - Runs natively on **Windows, Linux, and Chromebook (Chrome OS)**.

---

## 🚀 Quick Setup & Run

### 🪟 1. Windows Setup
1. Double-click [`start.bat`](start.bat) or run in terminal:
   ```cmd
   python vanity.py
   ```
   *(Ya agar python alias error aaye: `py -3 vanity.py`)*

### 💻 2. Chromebook (Chrome OS) & Linux Setup
> Detail step-by-step Hindi guide: [`CHROMEBOOK_SETUP.md`](CHROMEBOOK_SETUP.md)

1. Chromebook **Settings ➔ Advanced ➔ Developers ➔ Turn on Linux (Crostini)**.
2. Chromebook Linux Terminal me run karo:
   ```bash
   git clone https://github.com/loveslaw/cherry-vanity-engine.git
   cd cherry-vanity-engine
   python3 vanity.py
   ```

---

## 📋 Terminal Menu Layout

```text
 /__  \|  \  \ \ / /  _   | |   _   \
/ /\  \| | \  \ V /  | | | | | |_)  /
|  _   | |  \   /   | | | | |  _  < 
| | |  | \  / / \ \ | |_| | | | \  \
\_| |_/\__// /   \_\ \___/|_|_|  \_\

──────────────────────────────────────────────────────────────────────────────
                               MADE BY - aqxior

╭───────────────────────────────────────────────────────────────────────────╮
│  [ 1] FAST VANITY SNIPER           │  [ 6] SEND TEST WEBHOOK              │
│  [ 2] INSTANT VANITY SWAPPER       │  [ 7] CHECK VANITY STATUS            │
│  [ 3] GUILD BOOST INSPECTOR        │  [ 8] SPEED BENCHMARK & JITTER       │
│  [ 4] LIVE SPEED MONITOR           │  [ 9] VIEW TOKENS & CONFIG           │
│  [ 5] EDIT CONFIGURATION           │  [10] EXIT PROGRAM                   │
╰───────────────────────────────────────────────────────────────────────────╯

(@/aqxilorcore) Option: █
```

---

## ⚙️ Configuration Setup

App khol kar Option `[ 5]` choose karo, ya directly [`config.json`](config.json) me edit karo:

- `sniper_token`: Jis account se vanity claim karni hai (Admin / Manage Server permission).
- `swapper_token_a`: Server A (source) ka token.
- `swapper_token_b`: Server B (destination) ka token.
- `target_guild_id`: Jis server par vanity lagani hai.
- `source_guild_id`: Jaha se vanity hatani hai.
- `destination_guild_id`: Jaha nayi vanity shift karni hai.
- `target_vanity`: Jo vanity claim/swap karni hai.
- `webhook`: Discord notification webhook URL.

> ⚠️ **Discord Server Boost Requirement**: Vanity URL lagane ke liye destination server par **Level 3 Boost (14 Boosts)** hona mandatory hai.
