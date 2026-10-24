import asyncio
import aiohttp
import time
import sys
import pyotp

async def claim_with_mfa(secret_or_password=None, token=None):
    token = token or "YOUR_DISCORD_TOKEN_HERE"
    guild_id = "1563409836794839161"
    vanity_code = "aqxilorcore"
    
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    async with aiohttp.ClientSession() as s:
        # Step 1: Initial Claim to trigger ticket
        payload = {"code": vanity_code}
        async with s.patch(f"https://discord.com/api/v9/guilds/{guild_id}/vanity-url", headers=headers, json=payload) as r:
            data = await r.json()
            if r.status == 200:
                print(f"🎉 SUCCESS! Vanity claimed directly: {data}")
                return True
            
            if r.status == 401 and data.get("code") == 60003 and data.get("mfa"):
                ticket = data["mfa"].get("ticket")
                methods = [m.get("type") for m in data["mfa"].get("methods", [])]
                print(f"[*] 2FA/Elevation ticket received: {ticket[:25]}...")
                print(f"[*] Allowed MFA methods by Discord: {methods}")
                
                if not secret_or_password:
                    print("[!] No 2FA Secret or Password provided to solve MFA ticket.")
                    return False

                clean_input = secret_or_password.strip()

                # Determine whether it's a 6-digit TOTP, 2FA Secret Key, or Password
                if clean_input.isdigit() and len(clean_input) == 6:
                    # Direct 6-digit TOTP code
                    mfa_payload = {"mfa_type": "totp", "data": clean_input, "ticket": ticket}
                    print(f"[*] Submitting 6-digit TOTP code: {clean_input}...")
                elif "totp" in methods and len(clean_input.replace(" ", "")) in (16, 26, 32):
                    # 2FA Secret Key (pyotp generation)
                    try:
                        totp_code = pyotp.TOTP(clean_input.replace(" ", "")).now()
                        mfa_payload = {"mfa_type": "totp", "data": totp_code, "ticket": ticket}
                        print(f"[*] Generated TOTP code {totp_code} via pyotp from Secret Key!")
                    except Exception as e:
                        print(f"[!] pyotp failed: {e}, falling back to password")
                        mfa_payload = {"mfa_type": "password", "data": clean_input, "ticket": ticket}
                else:
                    # Password method
                    mfa_payload = {"mfa_type": "password", "data": clean_input, "ticket": ticket}
                    print(f"[*] Submitting Password to MFA...")

                async with s.post("https://discord.com/api/v9/mfa/finish", headers=headers, json=mfa_payload) as mfa_res:
                    mfa_data = await mfa_res.json()
                    print(f"MFA Finish Status: HTTP {mfa_res.status} -> {mfa_data}")
                    
                    if mfa_res.status == 200 and mfa_data.get("token"):
                        mfa_token = mfa_data["token"]
                        print(f"✅ Elevation verified! Got MFA Token: {mfa_token[:20]}...")
                        
                        # Step 3: Final Claim with elevated token & cookie!
                        claim_headers = headers.copy()
                        claim_headers["X-Discord-MFA"] = mfa_token
                        claim_headers["X-Discord-MFA-Ticket"] = mfa_token
                        claim_headers["Cookie"] = f"__Secure-recent_mfa={mfa_token}"
                        
                        async with s.patch(f"https://discord.com/api/v9/guilds/{guild_id}/vanity-url", headers=claim_headers, json=payload) as final_res:
                            final_data = await final_res.json()
                            print(f"\n🎉 🎉 🎉 FINAL CLAIM STATUS: HTTP {final_res.status} 🎉 🎉 🎉")
                            print(f"Result: {final_data}")
                            return final_res.status == 200
                    else:
                        print(f"❌ Failed to verify MFA: {mfa_data}")
                        return False

if __name__ == "__main__":
    val = sys.argv[1] if len(sys.argv) > 1 else None
    tok = sys.argv[2] if len(sys.argv) > 2 else None
    asyncio.run(claim_with_mfa(val, tok))
