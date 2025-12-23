import time, random, string, os, requests, shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

last_ip = None

def kill_browser_processes():
    os.system("pkill -f chromium")
    os.system("pkill -f chromedriver")
    time.sleep(1)

def clean_all_traces():
    # Bersihkan captcha dan profile lama
    if os.path.exists("captcha.png"):
        os.remove("captcha.png")
    
    profile_path = "/data/data/com.termux/files/home/chrome_profile"
    if os.path.exists(profile_path):
        try: shutil.rmtree(profile_path)
        except: pass
    return profile_path

def run_bot(my_reff_link):
    global last_ip
    driver = None 
    kill_browser_processes()
    user_data_dir = clean_all_traces()

    # Cek IP Publik (Identifikasi blok 114)
    try:
        current_ip = requests.get('https://api.ipify.org', timeout=15).text
        print(f"\n[i] IP Sekarang: {current_ip}")
        if current_ip == last_ip:
            print("[!] Peringatan: IP masih sama dengan pendaftaran sebelumnya!")
        last_ip = current_ip
    except:
        print("[!] Gagal cek IP. Periksa koneksi data kamu.")
        return False

    options = Options()
    # Path Chromium Termux
    options.binary_location = "/data/data/com.termux/files/usr/bin/chromium-browser"
    
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--incognito')
    
    # --- FITUR DNS ACAK ---
    dns_list = [
        "https://cloudflare-dns.com/dns-query",      # Cloudflare
        "https://dns.google/dns-query",             # Google
        "https://dns.adguard-dns.com/dns-query",    # AdGuard
        "https://doh.opendns.com/dns-query"         # OpenDNS
    ]
    chosen_dns = random.choice(dns_list)
    options.add_argument(f'--dns-over-https={chosen_dns}')
    print(f"[i] Jalur DNS: {chosen_dns.split('/')[2]}")
    
    # --- FITUR RANDOM USER-AGENT ---
    ua_list = [
        "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; M2102J20SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
    ]
    options.add_argument(f'--user-agent={random.choice(ua_list)}')
    
    # Sembunyikan jejak bot
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    try:
        service = Service("/data/data/com.termux/files/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)
        
        # Samakan Waktu dengan Lokasi Bandung/Jakarta
        driver.execute_cdp_cmd('Emulation.setTimezoneOverride', {'timezoneId': 'Asia/Jakarta'})
        
        # Hapus flag navigator.webdriver
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("[+] Membuka Link...")
        driver.get(my_reff_link)
        time.sleep(10) # Jeda loading

        if "pages=reg" not in driver.current_url:
            driver.get("https://gamety.org/?pages=reg")

        # Input Form
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "login")))
        user = "user" + "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        
        driver.find_element(By.NAME, "login").send_keys(user)
        driver.find_element(By.NAME, "email").send_keys(f"{user}@gmail.com")
        driver.find_element(By.NAME, "pass").send_keys("Pass123!@#")
        
        # Screenshot Captcha
        captcha_el = driver.find_element(By.ID, "cap_img")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", captcha_el)
        time.sleep(3)
        captcha_el.screenshot("captcha.png")
        os.system("cp captcha.png /sdcard/Download/captcha.png 2>/dev/null")
        
        print(f"\n[USER] {user}")
        code = input(">>> Ketik Captcha: ")
        
        driver.find_element(By.NAME, "cap").send_keys(code)
        driver.find_element(By.NAME, "sub_reg").click()

        # Deteksi hasil
        time.sleep(10)
        try:
            msg = driver.find_element(By.CLASS_NAME, "swal-text").text
            print(f"[!] Respon: {msg}")
            if "incorrect" in msg.lower():
                print("[×] Gagal: Captcha Salah!")
            elif "allowed" in msg.lower():
                print("[×] Gagal: IP 114 Kamu Terdeteksi Proxy!")
        except:
            print("[✔] Berhasil Mendaftar!")
            # Simpan data yang sukses
            with open("sukses.txt", "a") as f:
                f.write(f"{user} | {current_ip}\n")

    except Exception as e:
        print(f"[!] Masalah: {e}")
    finally:
        if driver: driver.quit()
        kill_browser_processes()

if __name__ == "__main__":
    LINK = "https://gamety.org/?ref=53636"
    while True:
        print("\n" + "="*45)
        print("TIPS: JEDA 10 MENIT SETIAP AKUN BERHASIL")
        input(">>> [MODE PESAWAT 60 DETIK] Lalu Tekan ENTER...")
        run_bot(LINK)
