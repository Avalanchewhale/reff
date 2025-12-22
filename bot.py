import time, random, string, os, requests, shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

last_ip = None

def kill_browser_processes():
    """Mematikan semua proses sisa agar sistem bersih dan folder bisa dihapus"""
    print("[1] Mematikan proses Chromium & Driver lama...")
    os.system("pkill -f chromium")
    os.system("pkill -f chromedriver")
    time.sleep(1)

def clean_all_data():
    """Menghapus folder profile untuk menghilangkan Session, Cache, dan Cookies"""
    profile_path = "/data/data/com.termux/files/home/chrome_profile"
    if os.path.exists(profile_path):
        try:
            shutil.rmtree(profile_path)
            print("[2] Folder data browser lama dihapus (Pembersihan Total).")
        except:
            pass
    return profile_path

def get_current_ip():
    """Cek IP saat ini sebelum mulai"""
    try:
        res = requests.get('https://api.ipify.org', timeout=10).text
        return res
    except:
        return "Gagal Cek IP"

def run_bot(my_reff_link):
    global last_ip
    
    # --- PROSES CLEANING ---
    kill_browser_processes()
    user_data_dir = clean_all_data()

    # --- CEK IP (SANGAT PENTING UNTUK SHARED IP) ---
    current_ip = get_current_ip()
    print(f"[3] IP Saat Ini: {current_ip}")
    
    if current_ip == last_ip and current_ip != "Gagal Cek IP":
        print("[!] GAGAL: IP masih sama dengan pendaftaran sebelumnya!")
        return False
    
    last_ip = current_ip

    # --- SETINGAN BROWSER ANTI-DETECT ---
    ua = f"Mozilla/5.0 (Linux; Android {random.randint(11, 14)}; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(120, 126)}.0.0.0 Mobile Safari/537.36"
    print(f"[4] User-Agent: {ua}")

    options = Options()
    options.binary_location = "/data/data/data/com.termux/files/usr/bin/chromium-browser"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'--user-agent={ua}')
    options.add_argument(f'--user-data-dir={user_data_dir}')
    
    # --- FITUR PRIVATE DNS & ANTI-LEAK ---
    # Menggunakan Google DNS-over-HTTPS untuk mencegah kebocoran DNS ISP
    options.add_argument('--use-cloudflare-dns-resolver') # Opsional: Menggunakan Cloudflare
    options.add_argument('--dns-over-https=https://dns.google/dns-query') 
    
    # Mematikan WebRTC agar IP asli di balik Shared IP tidak bocor
    options.add_argument('--disable-webrtc')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    service = Service("/data/data/com.termux/files/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    
    # Sembunyikan identitas webdriver
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        print(f"[5] Membuka Link: {my_reff_link}")
        driver.get(my_reff_link)
        time.sleep(5)

        # Klik Pendaftaran
        try:
            btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn2.btn-success")))
            driver.execute_script("arguments[0].click();", btn)
        except:
            driver.get("https://gamety.org/?pages=reg")

        # Isi Data
        user = "user" + "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "login")))
        
        driver.find_element(By.NAME, "login").send_keys(user)
        driver.find_element(By.NAME, "email").send_keys(f"{user}@gmail.com")
        driver.find_element(By.NAME, "pass").send_keys("Pass1234!")
        
        # Ambil Captcha
        captcha_el = driver.find_element(By.ID, "cap_img")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", captcha_el)
        time.sleep(3) 
        driver.save_screenshot("captcha.png")
        os.system("cp captcha.png /sdcard/Download/captcha.png 2>/dev/null")
        
        print(f"[6] Data Dibuat: {user}")
        captcha_code = input(">>> Masukkan Captcha: ")
        
        driver.find_element(By.NAME, "cap").send_keys(captcha_code)
        time.sleep(2)
        driver.find_element(By.NAME, "sub_reg").click()

        # Deteksi Respon
        print("[7] Menunggu respon web...")
        time.sleep(12)
        
        try:
            swal = driver.find_element(By.CLASS_NAME, "swal-text")
            print(f"\n[!] Respon Web Asli: {swal.text}")
        except:
            print(f"\n[✔] SUKSES: Akun {user} terdaftar!")

    except Exception as e:
        print(f"[!] Error: {str(e)[:100]}")
    finally:
        if driver:
            driver.quit()
        kill_browser_processes()
        print("[✔] Proses selesai & Chromium ditutup.")

if __name__ == "__main__":
    MY_LINK = "https://gamety.org/?ref=53636"
    while True:
        print("\n" + "="*45 + "\nWAJIB MODE PESAWAT 15 DETIK!\n" + "="*45)
        input(">>> Tekan ENTER setelah ganti IP...")
        run_bot(MY_LINK)
