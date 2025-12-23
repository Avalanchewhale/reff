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

def clean_data():
    # Hapus captcha dan profile lama
    if os.path.exists("captcha.png"): os.remove("captcha.png")
    path = "/data/data/com.termux/files/home/chrome_profile"
    if os.path.exists(path): shutil.rmtree(path)
    return path

def run_bot(my_link):
    global last_ip
    driver = None
    kill_browser_processes()
    user_dir = clean_data()

    # Cek IP saat ini
    try:
        curr_ip = requests.get('https://api.ipify.org', timeout=10).text
        print(f"[i] IP Sekarang: {curr_ip}")
    except:
        return False

    if curr_ip == last_ip:
        print("[!] IP Masih Sama. Ganti IP dulu!")
        return False
    last_ip = curr_ip

    options = Options()
    # Path benar (Hanya 2x data)
    options.binary_location = "/data/data/com.termux/files/usr/bin/chromium-browser"
    
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # 1. DNS Over HTTPS agar ISP tidak bocor
    options.add_argument('--dns-over-https=https://cloudflare-dns.com/dns-query')
    
    # 2. Sembunyikan identitas otomasi (Selenium)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # 3. User Agent Acak
    ua = f"Mozilla/5.0 (Linux; Android {random.randint(11, 14)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
    options.add_argument(f'--user-agent={ua}')

    try:
        service = Service("/data/data/com.termux/files/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)
        
        # 4. Spoofing Timezone agar sesuai IP Bandung/Jakarta
        driver.execute_cdp_cmd('Emulation.setTimezoneOverride', {'timezoneId': 'Asia/Jakarta'})
        
        # 5. Sembunyikan Navigator Webdriver
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        print("[+] Membuka web...")
        driver.get(my_link)
        time.sleep(8)

        # Cek apakah langsung ke pendaftaran
        if "pages=reg" not in driver.current_url:
            driver.get("https://gamety.org/?pages=reg")

        # Isi Form
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "login")))
        user = "user" + "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        
        driver.find_element(By.NAME, "login").send_keys(user)
        driver.find_element(By.NAME, "email").send_keys(f"{user}@gmail.com")
        driver.find_element(By.NAME, "pass").send_keys("Pass123!@#")
        
        # Simpan Captcha
        captcha_el = driver.find_element(By.ID, "cap_img")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", captcha_el)
        time.sleep(2)
        captcha_el.screenshot("captcha.png")
        os.system("cp captcha.png /sdcard/Download/captcha.png 2>/dev/null")
        
        print(f"\n[DATA] Username: {user}")
        code = input(">>> Masukkan Captcha: ")
        
        driver.find_element(By.NAME, "cap").send_keys(code)
        driver.find_element(By.NAME, "sub_reg").click()

        # Deteksi Error
        time.sleep(10)
        try:
            res = driver.find_element(By.CLASS_NAME, "swal-text").text
            print(f"[!] Respon: {res}")
            if "incorrect" in res.lower():
                print("[!] Kesalahan: Kode Verifikasi Salah")
            elif "allowed" in res.lower():
                print("[!] Kesalahan: IP Terdeteksi Proxy/VPN")
        except:
            print("[✔] Sukses Terdaftar!")

    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        if driver: driver.quit()
        kill_browser_processes()

if __name__ == "__main__":
    LINK = "https://gamety.org/?ref=53636"
    while True:
        print("\n" + "="*35)
        input(">>> GANTI IP LALU TEKAN ENTER...")
        run_bot(LINK)
