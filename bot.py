import time, random, string, os, requests, shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Variabel Global
last_ip = None

def kill_browser_processes():
    """Membereskan proses sisa agar folder profile tidak terkunci"""
    print("[1] Mematikan proses Chromium & Driver Lama...")
    os.system("pkill -f chromium")
    os.system("pkill -f chromedriver")
    time.sleep(1)

def clean_all_data():
    """Menghapus total folder profile untuk pendaftaran baru"""
    profile_path = "/data/data/com.termux/files/home/chrome_profile"
    if os.path.exists(profile_path):
        try:
            shutil.rmtree(profile_path)
            print("[✔] Data browser lama dibersihkan.")
        except:
            pass
    return profile_path

def run_bot(my_reff_link):
    global last_ip
    driver = None 
    
    kill_browser_processes()
    user_data_dir = clean_all_data()

    # CEK IP (Kunci utama menembus Shared IP)
    try:
        current_ip = requests.get('https://api.ipify.org', timeout=10).text
        print(f"[3] IP Saat Ini: {current_ip}")
    except:
        print("[!] Gagal cek IP. Pastikan internet stabil!")
        return False
    
    if current_ip == last_ip:
        print(f"[!] IP Masih Sama ({current_ip}). Harap Mode Pesawat Lagi!")
        return False
    
    last_ip = current_ip

    # SETUP BROWSER (Sesuai Path di Termux Kamu)
    ua = f"Mozilla/5.0 (Linux; Android {random.randint(11, 14)}; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
    print(f"[4] User-Agent: {ua}")

    options = Options()
    # Path yang benar berdasarkan foto kamu (Hanya dua kali kata 'data')
    options.binary_location = "/data/data/com.termux/files/usr/bin/chromium-browser"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'--user-agent={ua}')
    options.add_argument(f'--user-data-dir={user_data_dir}')
    
    # Proteksi DNS & WebRTC
    options.add_argument('--dns-over-https=https://dns.google/dns-query')
    options.add_argument('--disable-webrtc')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    try:
        # Path Service yang benar berdasarkan hasil 'which chromedriver' kamu
        service = Service("/data/data/com.termux/files/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        print(f"[5] Membuka Link Reff...")
        driver.get(my_reff_link)
        time.sleep(7)

        # Cari Tombol Daftar
        try:
            btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn2.btn-success")))
            driver.execute_script("arguments[0].click();", btn)
        except:
            driver.get("https://gamety.org/?pages=reg")

        # Isi Form
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "login")))
        user = "user" + "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        
        driver.find_element(By.NAME, "login").send_keys(user)
        driver.find_element(By.NAME, "email").send_keys(f"{user}@gmail.com")
        driver.find_element(By.NAME, "pass").send_keys("Pass1234!")
        
        # Capture Captcha
        captcha_el = driver.find_element(By.ID, "cap_img")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", captcha_el)
        time.sleep(3) 
        driver.save_screenshot("captcha.png")
        os.system("cp captcha.png /sdcard/Download/captcha.png 2>/dev/null")
        
        print(f"\n[DATA] Username: {user}")
        captcha_code = input(">>> Masukkan Captcha: ")
        
        driver.find_element(By.NAME, "cap").send_keys(captcha_code)
        driver.find_element(By.NAME, "sub_reg").click()

        print("[6] Menunggu hasil pendaftaran...")
        time.sleep(12)
        
        try:
            swal = driver.find_element(By.CLASS_NAME, "swal-text")
            print(f"[!] Respon: {swal.text}")
        except:
            print(f"[✔] SUKSES: Akun {user} terdaftar!")

    except Exception as e:
        print(f"[!] Terjadi Error: {e}")
    
    finally:
        if driver is not None:
            driver.quit()
        kill_browser_processes()

if __name__ == "__main__":
    MY_LINK = "https://gamety.org/?ref=53636"
    print("="*45)
    print("   BOT GAMETY FIX PATH   ")
    print("="*45)
    while True:
        print("\nWAJIB MODE PESAWAT 15 DETIK!")
        print("="*45)
        input(">>> Tekan ENTER setelah ganti IP...")
        try:
            run_bot(MY_LINK)
        except Exception as main_e:
            print(f"[!] Fatal Error: {main_e}")
