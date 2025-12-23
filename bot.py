import time, random, string, os, requests, shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import pytesseract

def kill_processes():
    os.system("pkill -f chromium")
    os.system("pkill -f chromedriver")
    time.sleep(1)

def deep_clean():
    # Hapus file sampah dan profile lama
    if os.path.exists("captcha.png"): os.remove("captcha.png")
    path = "/data/data/com.termux/files/home/chrome_profile"
    if os.path.exists(path):
        try: shutil.rmtree(path)
        except: pass

def get_true_random_dns():
    # Daftar DNS global untuk menyamarkan jejak Indosat
    doh_list = [
        "https://cloudflare-dns.com/dns-query",
        "https://dns.google/dns-query",
        "https://dns.adguard-dns.com/dns-query",
        "https://doh.opendns.com/dns-query",
        "https://dns.quad9.net/dns-query"
    ]
    return random.choice(doh_list)

def solve_captcha(img_path):
    try:
        # Optimasi gambar agar terbaca jelas
        img = Image.open(img_path).convert('L')
        # Config tesseract khusus angka
        config = r'--oem 3 --psm 6 outputbase digits'
        result = pytesseract.image_to_string(img, config=config)
        return "".join(filter(str.isdigit, result))
    except:
        return ""

def run_bot(target_url):
    kill_processes()
    deep_clean()
    
    # Cek IP saat ini
    try:
        ip = requests.get('https://api.ipify.org', timeout=10).text
        print(f"\n[i] IP Aktif: {ip}")
    except:
        print("[!] Koneksi terputus.")
        return

    options = Options()
    options.binary_location = "/data/data/com.termux/files/usr/bin/chromium-browser"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--incognito')
    
    # Random DNS & Fingerprint
    dns = get_true_random_dns()
    options.add_argument(f'--dns-over-https={dns}')
    print(f"[i] Menggunakan DNS: {dns.split('/')[2]}")
    
    ua = [
        "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    ]
    options.add_argument(f'--user-agent={random.choice(ua)}')
    options.add_argument('--disable-blink-features=AutomationControlled')

    try:
        service = Service("/data/data/com.termux/files/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_cdp_cmd('Emulation.setTimezoneOverride', {'timezoneId': 'Asia/Jakarta'})
        
        print("[+] Membuka Gamety...")
        driver.get(target_url)
        time.sleep(10)

        # Cek apakah terblokir IP
        if "pages=reg" not in driver.current_url:
            driver.get("https://gamety.org/?pages=reg")

        # Isi Form
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "login")))
        user = "reg" + "".join(random.choices(string.digits, k=7))
        driver.find_element(By.NAME, "login").send_keys(user)
        driver.find_element(By.NAME, "email").send_keys(f"{user}@gmail.com")
        driver.find_element(By.NAME, "pass").send_keys("Admin123!")

        # Screenshot & Solve Captcha
        captcha_el = driver.find_element(By.ID, "cap_img")
        captcha_el.screenshot("captcha.png")
        code = solve_captcha("captcha.png")
        
        if not code or len(code) < 4:
            os.system("cp captcha.png /sdcard/Download/captcha.png 2>/dev/null")
            code = input(f"[!] OCR Gagal ({code}). Masukkan Manual: ")
        else:
            print(f"[+] OCR Berhasil: {code}")
            time.sleep(2)

        driver.find_element(By.NAME, "cap").send_keys(code)
        driver.find_element(By.NAME, "sub_reg").click()
        
        # Deteksi hasil pendaftaran
        time.sleep(10)
        try:
            swal = driver.find_element(By.CLASS_NAME, "swal-text").text
            print(f"[!] Respon Server: {swal}")
        except:
            print("[✔] Akun Berhasil Dibuat!")
            with open("hasil.txt", "a") as f: f.write(f"{user} | {ip}\n")

    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    REFF = "https://gamety.org/?ref=53636"
    while True:
        print("\n" + "="*40)
        input(">>> GANTI IP SEKARANG LALU ENTER...")
        run_bot(REFF)
