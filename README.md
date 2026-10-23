# ⚡ Cherry Vanity Engine (Python Edition)

Ultra-Fast, Asynchronous Discord Vanity Sniper & Atomic Swapper written natively in **Python 3** with live terminal speed monitoring, TLS 1.3 keep-alive connection pooling, and the exact magenta UI layout from `aqxior`.

---

## ✨ Features

- **⚡ Millisecond Speed & Reaction Times**:
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
1. [Python 3.10+](https://python.org/) install karo (make sure "Add Python to PATH" tick ho).
2. Simply [`start.bat`](start.bat) par double click karo ya terminal me run karo:
   ```cmd
   pip install -r requirements.txt
   python main.py
   ```

### 💻 2. Chromebook (Chrome OS) & Linux Setup
> Detail step-by-step Hindi guide ke liye check karo: [`CHROMEBOOK_SETUP.md`](CHROMEBOOK_SETUP.md)

1. Chromebook **Settings ➔ Advanced ➔ Developers ➔ Turn on Linux (Crostini)**.
2. Chromebook Linux Terminal kholo aur run karo:
   ```bash
   sudo apt update && sudo apt install -y python3 python3-pip python3-aiohttp python3-requests
   pip install colorama --break-system-packages
   ```
3. Folder me jakar start karo:
   ```bash
   chmod +x start.sh
   ./start.sh
   ```
   *(Ya directly `python3 main.py`)*

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

(aqxior) Option: █
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
- `target_vanity`: Jo vanity claim/swap karni hai (e.g. `cherry`).
- `webhook`: Discord notification webhook URL.

> ⚠️ **Discord Server Boost Requirement**: Vanity URL lagane ke liye destination server par **Level 3 Boost (14 Boosts)** hona mandatory hai.

---

## 🔔 Discord Webhook Alerts
Jab bhi koi vanity claim ya swap hoti hai, Discord webhook embed me reaction speed (`ms`), vanity link, timestamp, aur proof automatic send ho jata hai!
