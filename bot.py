import time, random, string, os, requests, shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def kill_browser_processes():
    """Langkah 1: Matikan semua proses sisa agar folder bisa dihapus tanpa error"""
    os.system("pkill -f chromium")
    os.system("pkill -f chromedriver")
    time.sleep(1)

def clean_all_data():
    """Langkah 2: Hapus folder profile secara fisik (Pembersihan Total)"""
    profile_path = "/data/data/com.termux/files/home/chrome_profile"
    if os.path.exists(profile_path):
        try:
            shutil.rmtree(profile_path)
            print("[✔] Folder Data Browser lama telah dihapus total (Fresh Start).")
        except:
            pass
    return profile_path

def run_bot(my_reff_link, last_ip):
    # --- PROSES CLEANING SEBELUM START ---
    kill_browser_processes()
    user_data_dir = clean_all_data()
    
    current_ip = requests.get('https://api.ipify.org').text
    if current_ip == last_ip:
        print("[!] IP masih sama, proses dibatalkan.")
        return last_ip

    ua = f"Mozilla/5.0 (Linux; Android {random.randint(11, 14)}; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(120, 126)}.0.0.0 Mobile Safari/537.36"
    print(f"[i] IP: {current_ip} | UA: {ua}")

    options = Options()
    options.binary_location = "/data/data/com.termux/files/usr/bin/chromium-browser"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument(f'--user-agent={ua}')
    
    # PAKAI FOLDER PROFILE (Data akan disimpan di sini lalu kita hapus di putaran berikutnya)
    options.add_argument(f'--user-data-dir={user_data_dir}')
    
    # HAPUS INCOGNITO agar terlihat seperti browser normal
    # options.add_argument('--incognito') # <-- Baris ini dihapus

    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    service = Service(executable_path="/data/data/com.termux/files/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(my_reff_link)
        # ... proses pendaftaran ...
        # (Lanjutkan dengan kode input captcha dan klik submit kamu)
        
        # Contoh deteksi respon original
        time.sleep(10)
        try:
            swal = driver.find_element(By.CLASS_NAME, "swal-text")
            print(f"[!] Respon Web: {swal.text}")
        except:
            print("[✔] SUKSES: Akun terdaftar!")
            
    finally:
        driver.quit()
        kill_browser_processes() # Langkah terakhir: Pastikan driver mati agar folder bisa dihapus di sesi berikutnya
        return current_ip

if __name__ == "__main__":
    REFF = "https://gamety.org/?ref=53636"
    ip_history = None
    while True:
        print("\n" + "="*40 + "\nWAJIB MODE PESAWAT 15 DETIK!\n" + "="*40)
        input(">>> Tekan ENTER setelah ganti IP...")
        ip_history = run_bot(REFF, ip_history)
