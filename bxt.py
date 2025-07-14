import requests
import time
from bs4 import BeautifulSoup

# URL dan Header
URL = "https://bxtnetwork.fun?ref=438CYUDN21"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36'
}

# Baca wallet dari file
def load_wallets():
    try:
        with open("wallets.txt", "r") as f:
            wallets = [line.strip() for line in f if line.strip()]
        return wallets
    except FileNotFoundError:
        print("‼️ File wallets.txt tidak ditemukan.")
        return []

def auto_claim(wallet):
    print(f"\n[{time.strftime('%H:%M:%S')}] ▶️ Wallet: {wallet}")
    session = requests.Session()
    try:
        res = session.get(URL, headers=HEADERS)
        soup = BeautifulSoup(res.text, 'html.parser')

        # Cari input form wallet
        input_tag = soup.find("input", {"type": "text"})
        if not input_tag:
            print("❌ Input wallet tidak ditemukan.")
            return

        input_name = input_tag.get('name', 'wallet')
        form = input_tag.find_parent("form")
        action = form.get('action', URL) if form else URL
        claim_url = action if action.startswith('http') else URL + action

        payload = {input_name: wallet}

        print("🚀 Mengirim klaim...")
        claim_res = session.post(claim_url, data=payload, headers=HEADERS)

        if "success" in claim_res.text.lower() or "claimed" in claim_res.text.lower():
            print("✅ Claim berhasil!")
        else:
            print("⚠️ Claim mungkin gagal. Cek manual.")
    except Exception as e:
        print("‼️ Error:", e)

# Jalankan semua wallet
def run_all():
    wallets = load_wallets()
    if not wallets:
        print("❌ Tidak ada wallet ditemukan.")
        return
    for wallet in wallets:
        auto_claim(wallet)

# Jalankan pertama kali
run_all()

# Loop setiap 3 jam
while True:
    print("\n⏳ Tunggu 3 jam untuk klaim berikutnya...\n")
    time.sleep(3 * 60 * 60)
    run_all()
