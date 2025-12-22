import time, random, string, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_bot(my_reff_link):
    # --- PENYESUAIAN PATH SESUAI HASIL CEK KAMU ---
    # Karena 'chromium-browser --version' berhasil, maka lokasinya di sini:
    PATH_BROWSER = "/data/data/com.termux/files/usr/bin/chromium-browser"
    PATH_DRIVER = "/data/data/com.termux/files/usr/bin/chromedriver"

    # Otomatis chmod supaya tidak 'Permission Denied'
    os.system(f"chmod +x {PATH_BROWSER} {PATH_DRIVER}")

    options = Options()
    # Beritahu Selenium bahwa aplikasi browsernya bernama 'chromium-browser'
    options.binary_location = PATH_BROWSER
    
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36')
    
    # Gunakan chromedriver sebagai penghubung
    service = Service(executable_path=PATH_DRIVER)
    
    try:
        driver = webdriver.Chrome(service=service, options=options)
        print(f"\n[+] Membuka Link Reff...")
        driver.get("https://gamety.org/?pages=reg")
        time.sleep(5)

        # Generate Data
        user = "user" + "".join(random.choices(string.ascii_lowercase, k=5))
        email = f"{user}@gmail.com"
        
        print(f"[+] Mencoba daftar: {user}")
        
        # Isi Form
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "login"))).send_keys(user)
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "pass").send_keys("Pass1234")
        
        # Ambil Captcha
        driver.save_screenshot("captcha.png")
        os.system("cp captcha.png /sdcard/Download/captcha.png 2>/dev/null")
        
        print("\n" + "!"*30)
        print(" CEK CAPTCHA DI FOLDER DOWNLOAD ")
        print("!"*30)
        captcha_code = input(">>> Masukkan 4 angka captcha: ")
        
        driver.find_element(By.NAME, "cap").send_keys(captcha_code)
        driver.find_element(By.NAME, "sub_reg").click()
        
        time.sleep(5)
        print(f"[✔] Selesai! Cek di web apakah reff masuk.")

    except Exception as e:
        print(f"[!] Terjadi Kendala: {e}")
    finally:
        try: driver.quit()
        except: pass

if __name__ == "__main__":
    MY_LINK = "https://gamety.org/?ref=53636"
    while True:
        run_bot(MY_LINK)
        print("\n[!] GANTI IP (MODE PESAWAT) SEKARANG!")
        input(">>> Tekan ENTER jika sudah ganti IP...")
