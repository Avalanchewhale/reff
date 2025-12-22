import time, random, string, os, requests, shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

last_ip = None

def get_current_ip():
    """Mengecek IP publik saat ini"""
    try:
        return requests.get('https://api.ipify.org', timeout=10).text
    except:
        return "Gagal Cek IP"

def get_random_ua():
    """Mengacak User-Agent Android multi-perangkat"""
    devices = ["SM-S918B", "Pixel 8 Pro", "M2101K6G", "SM-G973F", "Xiaomi 13T", "POCO F5"]
    chrome_ver = f"{random.randint(120, 126)}.0.{random.randint(6000, 7000)}.{random.randint(10, 99)}"
    ua = f"Mozilla/5.0 (Linux; Android {random.randint(11, 14)}; {random.choice(devices)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Mobile Safari/537.36"
    return ua

def clean_browser_data():
    """Menghapus paksa folder profile untuk membersihkan Cache & Session"""
    profile_path = "/data/data/com.termux/files/home/chrome_profile"
    if os.path.exists(profile_path):
        try:
            shutil.rmtree(profile_path)
            print("[✔] Session & Cache Browser lama telah dibersihkan.")
        except:
            pass
    return profile_path

def save_account(user, password, status, ip):
    """Menyimpan data ke data_reff.txt"""
    with open("data_reff.txt", "a") as f:
        f.write(f"User: {user} | Pass: {password} | IP: {ip} | Status: {status} | Tgl: {time.strftime('%Y-%m-%d %H:%M')}\n")

def run_bot(my_reff_link):
    global last_ip
    current_ip = get_current_ip()
    print(f"\n[i] IP Publik : {current_ip}")
    
    if current_ip == last_ip and current_ip != "Gagal Cek IP":
        print("[!] GAGAL: IP belum berubah! Silahkan Mode Pesawat dulu.")
        return False
    
    last_ip = current_ip
    
    user_data_dir = clean_browser_data()
    ua = get_random_ua()
    print(f"[i] User-Agent: {ua}")

    if os.path.exists("captcha.png"): os.remove("captcha.png")

    PATH_BROWSER = "/data/data/com.termux/files/usr/bin/chromium-browser"
    PATH_DRIVER = "/data/data/com.termux/files/usr/bin/chromedriver"
    os.system(f"chmod +x {PATH_BROWSER} {PATH_DRIVER}")

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
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    driver = webdriver.Chrome(service=Service(PATH_DRIVER), options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        driver.get(my_reff_link)
        time.sleep(random.uniform(2, 4))

        # Masuk ke Registrasi
        try:
            btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn2.btn-success")))
            driver.execute_script("arguments[0].click();", btn)
        except:
            driver.get("https://gamety.org/?pages=reg")

        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "login")))
        user = "user" + "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        
        # Simulasi ngetik lambat
        for char in user:
            driver.find_element(By.NAME, "login").send_keys(char)
            time.sleep(random.uniform(0.1, 0.2))
            
        driver.find_element(By.NAME, "email").send_keys(f"{user}@gmail.com")
        driver.find_element(By.NAME, "pass").send_keys("Pass1234!")
        
        # Ambil Captcha
        captcha_el = driver.find_element(By.ID, "cap_img")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", captcha_el)
        time.sleep(3) 
        driver.save_screenshot("captcha.png")
        os.system("cp captcha.png /sdcard/Download/captcha.png 2>/dev/null")
        
        print(f"\n[!] USER : {user}")
        captcha_code = input(">>> Masukkan 4 angka captcha: ")
        
        # Input Captcha & Submit
        driver.find_element(By.NAME, "cap").send_keys(captcha_code)
        time.sleep(2)
        driver.find_element(By.NAME, "sub_reg").click()
        
        # Deteksi Respon Original
        print("[+] Menunggu respon server (10 detik)...")
        time.sleep(10)
        
        try:
            swal = driver.find_element(By.CLASS_NAME, "swal-text")
            original_msg = swal.text # Ambil teks murni dari web
            print(f"[!] Respon Web: {original_msg}")
            save_account(user, "Pass1234!", original_msg, current_ip)
            return False
        except:
            print(f"[✔] SUKSES: Akun {user} terdaftar!")
            save_account(user, "Pass1234!", "SUKSES", current_ip)
            return True

    except Exception as e:
        print(f"[!] Error: {str(e)[:50]}")
        return False
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    MY_LINK = "https://gamety.org/?ref=53636"
    print("=== BOT REFF FINAL (TRANSPARENT MODE) ===")
    while True:
        run_bot(MY_LINK)
        print("\n" + "="*40)
        print("WAJIB MODE PESAWAT SELAMA 15 DETIK!")
        print("="*40)
        input(">>> Tekan ENTER jika sudah ganti IP...")
