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
    # Menghapus file captcha lama
    if os.path.exists("captcha.png"):
        os.remove("captcha.png")
    
    # Menghapus folder profile untuk memastikan tidak ada cookie yang tersisa
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

    # Cek IP Publik saat ini
    try:
        current_ip = requests.get('https://api.ipify.org', timeout=15).text
        print(f"[i] IP Sekarang: {current_ip}")
        if current_ip == last_ip:
            print("[!] Peringatan: IP masih sama dengan sebelumnya!")
        last_ip = current_ip
    except:
        print("[!] Gagal cek IP, pastikan data seluler aktif.")
        return False

    options = Options()
    # Path Chromium Termux yang sudah terverifikasi
    options.binary_location = "/data/data/com.termux/files/usr/bin/chromium-browser"
    
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--incognito') # Paksa mode samaran
    
    # DNS Cloudflare untuk menyembunyikan DNS Indosat/Tri
    options.add_argument('--dns-over-https=https://cloudflare-dns.com/dns-query')
    
    # Daftar User Agent HP agar setiap akun terlihat pakai HP berbeda
    ua_list = [
        "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.179 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; M2102J20SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
    ]
    options.add_argument(f'--user-agent={random.choice(ua_list)}')
    
    # Menghapus flag 'navigator.webdriver' agar tidak terdeteksi Cloudflare
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    try:
        service = Service("/data/data/com.termux/files/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)
        
        # Penyamaran Waktu sesuai lokasi IP Bandung
        driver.execute_cdp_cmd('Emulation.setTimezoneOverride', {'timezoneId': 'Asia/Jakarta'})
        
        # Pembersihan Cookies tambahan di tingkat browser
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("[+] Membuka halaman pendaftaran...")
        driver.get(my_reff_link)
        time.sleep(10) # Delay lebih lama agar load sempurna di jaringan 4G

        if "pages=reg" not in driver.current_url:
            driver.get("https://gamety.org/?pages=reg")

        # Input Data Form
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "login")))
        user = "user" + "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        
        driver.find_element(By.NAME, "login").send_keys(user)
        driver.find_element(By.NAME, "email").send_keys(f"{user}@gmail.com")
        driver.find_element(By.NAME, "pass").send_keys("Pass123!@#")
        
        # Proses Ambil Captcha
        print("[+] Mengambil screenshot captcha...")
        captcha_el = driver.find_element(By.ID, "cap_img")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", captcha_el)
        time.sleep(3)
        captcha_el.screenshot("captcha.png")
        
        # Copy ke folder Download agar bisa diakses Galeri
        os.system("cp captcha.png /sdcard/Download/captcha.png 2>/dev/null")
        
        print(f"\n[DATA] Username: {user}")
        captcha_input = input(">>> Masukkan Kode Captcha: ")
        
        driver.find_element(By.NAME, "cap").send_keys(captcha_input)
        driver.find_element(By.NAME, "sub_reg").click()

        # Deteksi Hasil
        print("[+] Menunggu verifikasi server...")
        time.sleep(10)
        try:
            swal = driver.find_element(By.CLASS_NAME, "swal-text").text
            print(f"[!] Pesan Sistem: {swal}")
            if "incorrect" in swal.lower():
                print("[×] Gagal: Captcha Salah!")
            elif "allowed" in swal.lower():
                print("[×] Gagal: IP diblokir (VPN/Proxy Detected)!")
        except:
            print("[✔] Berhasil! Silahkan cek akun kamu.")

    except Exception as e:
        print(f"[!] Terjadi Error: {e}")
    finally:
        if driver: driver.quit()
        kill_browser_processes()

if __name__ == "__main__":
    REFF_LINK = "https://gamety.org/?ref=53636"
    while True:
        print("\n" + "="*40)
        print("KARTU TRI: MODE PESAWAT MINIMAL 1 MENIT")
        input(">>> Tekan ENTER Jika Sudah Ganti IP...")
        run_bot(REFF_LINK)
