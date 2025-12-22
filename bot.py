import time
import random
import string
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def run_bot(my_reff_link):
    # --- PATH SESUAI HASIL LS KAMU ---
    PATH_BIN = "/data/data/com.termux/files/usr/bin"
    PATH_BROWSER = f"{PATH_BIN}/chromium"
    PATH_DRIVER = f"{PATH_BIN}/chromium-browser" # File hasil grep kamu

    # Otomatis memberi izin eksekusi
    os.system(f"chmod +x {PATH_BROWSER} {PATH_DRIVER}")

    options = Options()
    options.binary_location = PATH_BROWSER
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--user-agent=Mozilla/5.0 (Linux; Android 12; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36')
    
    service = Service(executable_path=PATH_DRIVER)
    
    try:
        driver = webdriver.Chrome(service=service, options=options)
        
        print(f"\n[+] Membuka Link Reff: {my_reff_link}")
        driver.get(my_reff_link)
        time.sleep(5)

        # Langsung ke halaman registrasi
        driver.get("https://gamety.org/?pages=reg")
        time.sleep(5)

        user = "user" + random_string(5)
        email = user + "@gmail.com"
        password = "Pass" + random_string(4).upper()

        print(f"[+] Mengisi Form: {user}")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "login"))).send_keys(user)
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "pass").send_keys(password)
        
        # Simpan Captcha ke Download HP
        driver.save_screenshot("captcha.png")
        os.system("cp captcha.png /sdcard/Download/captcha.png 2>/dev/null")
        
        print("\n" + "="*30)
        print(" CEK CAPTCHA DI FOLDER DOWNLOAD ")
        print("="*30)
        captcha_code = input(">>> Masukkan 4 angka captcha: ")
        
        driver.find_element(By.NAME, "cap").send_keys(captcha_code)
        driver.find_element(By.NAME, "sub_reg").click()
        
        time.sleep(5)
        
        with open("hasil_pendaftaran.txt", "a") as f:
            f.write(f"USER: {user} | PASS: {password} | EMAIL: {email}\n")
            
        print(f"\n[✔] SELESAI: Akun {user} berhasil dibuat!")

    except Exception as e:
        print(f"[!] Terjadi Error: {e}")
    finally:
        try: driver.quit()
        except: pass

if __name__ == "__main__":
    MY_REFF = "https://gamety.org/?ref=53636"
    
    while True:
        print("\n" + "🚀" * 5 + " BOT GAMETY START " + "🚀" * 5)
        run_bot(MY_REFF)
        
        print("\n" + "🔄" * 15)
        print("WAJIB GANTI IP (MODE PESAWAT) SEKARANG!")
        print("🔄" * 15)
        
        input("\n>>> Tekan ENTER jika internet sudah nyala lagi...")
