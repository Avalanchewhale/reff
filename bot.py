import time, random, string, os, requests, shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

last_ip = None

def kill_browser_processes():
    """Memastikan tidak ada chromium/driver yang terbuka di latar belakang"""
    print("[+] Membersihkan sisa proses Chromium & Driver...")
    os.system("pkill -f chromium")
    os.system("pkill -f chromedriver")
    time.sleep(1)

def get_current_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=10).text
    except:
        return "Gagal Cek IP"

def clean_all_data():
    """Hapus Session & Cache secara fisik"""
    profile_path = "/data/data/com.termux/files/home/chrome_profile"
    if os.path.exists(profile_path):
        try:
            shutil.rmtree(profile_path)
            print("[✔] Data Browser (Cache & Session) telah dihapus total.")
        except:
            pass
    return profile_path

def get_random_ua():
    devices = ["SM-S918B", "Pixel 8 Pro", "M2101K6G", "SM-G973F", "Xiaomi 13T", "POCO F5"]
    chrome_ver = f"{random.randint(120, 126)}.0.{random.randint(6000, 7000)}"
    return f"Mozilla/5.0 (Linux; Android {random.randint(11, 14)}; {random.choice(devices)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Mobile Safari/537.36"

def run_bot(my_reff_link):
    global last_ip
    
    # 1. Pastikan bersih dari proses lama sebelum mulai
    kill_browser_processes()
    
    # 2. Cek IP (Mode Pesawat)
    current_ip = get_current_ip()
    print(f"\n[i] IP Publik : {current_ip}")
    
    if current_ip == last_ip and current_ip != "Gagal Cek IP":
        print("[!] GAGAL: IP belum berubah!")
        return False
    
    last_ip = current_ip
    
    # 3. Hapus Data Cache & Session
    user_data_dir = clean_all_data()
    ua = get_random_ua()
    print(f"[i] User-Agent: {ua}")

    if os.path.exists("captcha.png"): os.remove("captcha.png")

    PATH_BROWSER = "/data/data/com.termux/files/usr/bin/chromium-browser"
    PATH_DRIVER = "/data/data/com.termux/files/usr/bin/chromedriver"

    options = Options()
    options.binary_location = PATH_BROWSER
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'--user-agent={ua}')
    options.add_argument('--window-size=1080,1920')
    options.add_argument(f'--user-data-dir={user_data_dir}')
    options.add_argument('--incognito')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    service = Service(executable_path=PATH_DRIVER)
    driver = None
    
    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # 4. Buka Link & Daftar
        driver.get(my_reff_link)
        time.sleep(3)

        try:
            btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn2.btn-success")))
            driver.execute_script("arguments[0].click();", btn)
        except:
            driver.get("https://gamety.org/?pages=reg")

        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "login")))
        user = "user" + "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        
        driver.find_element(By.NAME, "login").send_keys(user)
        driver.find_element(By.NAME, "email").send_keys(f"{user}@gmail.com")
        driver.find_element(By.NAME, "pass").send_keys("Pass1234!")
        
        # Ambil Captcha
        captcha_el = driver.find_element(By.ID, "cap_img")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", captcha_el)
        time.sleep(3) 
        driver.save_screenshot("captcha.png")
        os.system("cp captcha.png /sdcard/Download/captcha.png 2>/dev/null")
        
        print(f"\n[!] DATA: {user}")
        captcha_code = input(">>> Masukkan Captcha: ")
        
        driver.find_element(By.NAME, "cap").send_keys(captcha_code)
        time.sleep(2)
        driver.find_element(By.NAME, "sub_reg").click()

        # 5. Cek Success / Failed (Pesan Original)
        print("[+] Menunggu respon server (10 detik)...")
        time.sleep(10)
        
        try:
            swal = driver.find_element(By.CLASS_NAME, "swal-text")
            original_msg = swal.text
            print(f"[!] Respon Web: {original_msg}")
            return False
        except:
            print(f"[✔] SUKSES: Akun {user} terdaftar!")
            return True

    except Exception as e:
        print(f"[!] Error: {str(e)[:50]}")
        return False
    finally:
        # 6. Tutup Driver & Force Kill lagi untuk memastikan bersih
        if driver:
            driver.quit()
        kill_browser_processes()
        print("[+] Semua proses ditutup total.")

if __name__ == "__main__":
    MY_LINK = "https://gamety.org/?ref=53636"
    while True:
        print("\n" + "="*40)
        print(" LANGKAH 1: WAJIB MODE PESAWAT SEKARANG! ")
        print("="*40)
        input(">>> Tekan ENTER jika sudah ganti IP...")
        
        run_bot(MY_LINK)
