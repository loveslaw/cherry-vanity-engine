# 💻 Chromebook (Chrome OS) Setup Guide - AHME Vanity Engine

Ye guide unke liye hai jo **Chromebook / Chrome OS** par ye tool run karna chahte hain. Chromebook par Linux (Crostini) support hota hai, jisse tum directly Python scripts run kar sakte ho bina kisi problem ke!

---

## 📌 STEP 1: Chromebook par Linux Turn ON karo

Agar tumhare Chromebook par Linux pehle se ON nahi hai:
1. Chromebook ki **Settings** kholo (bottom-right me clock par click karke gear icon dabao).
2. Left side menu me **About ChromeOS** ya **Advanced ➔ Developers** par click karo.
3. Wahan **Linux development environment** dikhega, uske samne **"Turn on"** button par click karo.
4. Next-next karke install hone do (ye 2-3 minute lega).
5. Install hone ke baad automatically ek **Terminal** window khul jayegi.

---

## 📌 STEP 2: Zip File ko Chromebook me daalo

1. Jo zip file tumhe mili hai (`AHME.zip`), usko download karo.
2. Chromebook ki **Files app** kholo.
3. `AHME.zip` par double-click karo (Chromebook isko mount kar deta hai).
4. Uske andar ke folder `AHME` ko drag karke left side me **"Linux files"** me drop/copy kar do!

---

## 📌 STEP 3: Chromebook Terminal me Run karo

Ab Chromebook ka **Terminal** app kholo aur ye commands copy-paste karo (ek ek karke ya sath me):

### 1. Python & Required Packages Install karo (Sirf ek baar karna hai):
```bash
sudo apt update && sudo apt install -y python3 python3-pip python3-aiohttp python3-requests
pip install colorama pyotp --break-system-packages
```

### 2. Project Folder me jaao:
```bash
cd ~/AHME
```

### 3. Launcher ko executable permission do:
```bash
chmod +x start.sh
```

### 4. Tool Run karo:
```bash
./start.sh
```
*(Ya directly `python3 main.py` bhi chala sakte ho!)*

---

## ⚙️ Configuration Setup (Chromebook se directly)

Tool start hone ke baad:
- Terminal menu me **`[ 5] EDIT CONFIGURATION`** choose karo.
- Wahan se hi apna **Discord Token**, **Server IDs**, **Vanity Code**, aur **Webhook** live type karke save kar sakte ho!
- Kisi text editor ko alag se kholne ki zaroorat nahi hai.

---

## ❓ Common Chromebook Troubleshooting

1. **Error: "externally-managed-environment" jab pip install karte ho:**
   - Solution: Command me `--break-system-packages` flag lagao:
     ```bash
     pip install -r requirements.txt --break-system-packages
     ```
2. **Permission Denied for start.sh:**
   - Solution: Ye command chalao:
     ```bash
     chmod +x start.sh
     ```
3. **Terminal me Color nahi aa rahe:**
   - ChromeOS Terminal naturally 256 colors aur RGB support karta hai, `colorama` already enabled hai.

---

Enjoy ultra-low latency vanity sniping & swapping on your Chromebook! ⚡
