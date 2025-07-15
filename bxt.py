from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Setup WebDriver untuk Chrome Headless
chrome_options = Options()
chrome_options.add_argument("--headless")  # Menjalankan tanpa GUI
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Tentukan path ke chromedriver (pastikan chromedriver sudah diunduh dan ada di path yang sesuai)
chrome_driver_path = "/path/to/chromedriver"

driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

# URL yang ingin diakses
URL = "https://bxtnetwork.fun?ref=438CYUDN21"

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
    try:
        driver.get(URL)
        time.sleep(5)  # Tunggu 5 detik untuk memuat halaman

        # Cari input form wallet
        input_tag = driver.find_element(By.XPATH, "//input[@type='text']")
        if not input_tag:
            print("❌ Input wallet tidak ditemukan.")
            return

        # Kirim wallet ke form
        input_tag.send_keys(wallet)
        input_tag.send_keys(Keys.RETURN)

        # Tunggu respon klaim
        time.sleep(2)

        # Cek apakah klaim berhasil
        page_source = driver.page_source
        if "success" in page_source.lower() or "claimed" in page_source.lower():
            print("✅ Claim berhasil!")
        else:
            print("⚠️ Claim mungkin gagal. Cek manual.")
    except Exception as e:
        print(f"‼️ Error: {e}")

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
    time.sleep(3 * 60 * 60)  # Tunggu 3 jam
    run_all()
