import time
import random
import string
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def run_bot(my_reff_link):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # 1. Buka Link Referral
        print(f"[+] Step 1: Membuka Link Referral: {my_reff_link}")
        driver.get(my_reff_link)
        time.sleep(5)

        # 2. Klik tombol 'Create an account'
        print("[+] Step 2: Mengalihkan ke halaman pendaftaran...")
        try:
            btn_reg = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn2.btn-success"))
            )
            btn_reg.click()
            time.sleep(5)
        except Exception as e:
            print(f"[!] Gagal klik tombol awal: {e}")
            return

        # 3. Generate Data Akun Otomatis
        user = "user" + random_string(5)
        email = user + "@gmail.com"
        password = "Pass_" + random_string(4).upper() # Password unik tiap akun

        # 4. Isi Form
        print(f"[+] Step 3: Mengisi form untuk {user}...")
        driver.find_element(By.NAME, "login").send_keys(user)
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "pass").send_keys(password)
        
        # 5. Captcha
        driver.save_screenshot("captcha.png")
        os.system("cp captcha.png /sdcard/Download/ 2>/dev/null")
        
        print("\n" + "!"*30)
        print("WAJIB ISI CAPTCHA!")
        print("Cek file 'captcha.png' di folder Download HP kamu.")
        print("!"*30)
        captcha_code = input(">>> Masukkan 4 angka captcha: ")
        
        driver.find_element(By.NAME, "cap").send_keys(captcha_code)

        # 6. Submit
        submit_btn = driver.find_element(By.NAME, "sub_reg")
        submit_btn.click()
        
        time.sleep(5)
        print(f"\n[✔] SUCCESS: Akun {user} terdaftar!")
        
        # MENYIMPAN DATA LOGIN (Username, Email, Password)
        with open("hasil_pendaftaran.txt", "a") as f:
            f.write(f"USER: {user} | EMAIL: {email} | PASS: {password}\n")
        print(f"[+] Data login telah disimpan di 'hasil_pendaftaran.txt'")

    except Exception as e:
        print(f"[!] Terjadi error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    MY_REFF = "https://gamety.org/?ref=53636"
    
    while True:
        print("\n" + "="*50)
        print("🚀 MEMULAI PROSES PENDAFTARAN BARU")
        print("="*50)
        
        run_bot(MY_REFF)
        
        print("\n" + "🔄" * 15)
        print("PENTING: PROSES ROTASI IP")
        print("1. Aktifkan MODE PESAWAT")
        print("2. Tunggu 5-10 detik")
        print("3. Matikan MODE PESAWAT & Aktifkan DATA SELULER")
        print("🔄" * 15)
        
        lanjut = input("\n>>> Jika INTERNET SUDAH NYALA, tekan ENTER untuk lanjut (atau 'n' untuk stop): ")
        if lanjut.lower() == 'n':
            break