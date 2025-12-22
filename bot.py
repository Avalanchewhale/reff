import time, random, string, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_bot(my_reff_link):
    PATH_BROWSER = "/data/data/com.termux/files/usr/bin/chromium-browser"
    PATH_DRIVER = "/data/data/com.termux/files/usr/bin/chromedriver"

    os.system(f"chmod +x {PATH_BROWSER} {PATH_DRIVER}")

    options = Options()
    options.binary_location = PATH_BROWSER
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36')
    
    # PERBAIKAN: Set layar agak panjang agar form tidak terpotong
    options.add_argument('--window-size=1080,1920') 
    
    service = Service(executable_path=PATH_DRIVER)
    driver = None
    
    try:
        driver = webdriver.Chrome(service=service, options=options)
        print(f"\n[+] Membuka Link Reff...")
        driver.get(my_reff_link) 

        # 1. Klik Tombol 'Create an account'
        try:
            btn_reg = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn2.btn-success"))
            )
            driver.execute_script("arguments[0].click();", btn_reg)
            print("[✔] Masuk ke halaman pendaftaran.")
        except:
            print("[!] Gagal klik tombol, mencoba akses langsung URL pendaftaran...")
            driver.get("https://gamety.org/?pages=reg")

        # 2. Isi Form
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "login")))
        user = "user" + "".join(random.choices(string.ascii_lowercase, k=5))
        email = f"{user}@gmail.com"
        
        driver.find_element(By.NAME, "login").send_keys(user)
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "pass").send_keys("Pass1234")
        
        # 3. PERBAIKAN CAPTCHA: Scroll ke bawah agar gambar terlihat
        print("[+] Menggeser layar ke Captcha...")
        captcha_img = driver.find_element(By.ID, "cap_img")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", captcha_img)
        time.sleep(3) # Tunggu render gambar angka

        # 4. Ambil Screenshot
        driver.save_screenshot("captcha.png")
        os.system("cp captcha.png /sdcard/Download/captcha.png 2>/dev/null")
        
        print("\n" + "!"*30)
        print(" CEK CAPTCHA DI FOLDER DOWNLOAD ")
        print("!"*30)
        captcha_code = input(">>> Masukkan 4 angka captcha: ")
        
        # 5. Submit
        driver.find_element(By.NAME, "cap").send_keys(captcha_code)
        driver.find_element(By.NAME, "sub_reg").click()
        
        time.sleep(5)
        print(f"[✔] Selesai! User {user} terdaftar.")

    except Exception as e:
        print(f"[!] Kendala: {str(e)}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    MY_LINK = "https://gamety.org/?ref=53636"
    while True:
        run_bot(MY_LINK)
        print("\n[!] GANTI IP (MODE PESAWAT) SEKARANG!")
        input(">>> Tekan ENTER jika sudah ganti IP...")
