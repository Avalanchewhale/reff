import time, random, string, os, requests, shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Variabel pemantau IP agar tidak duplikat
last_ip = None

def kill_browser_processes():
    """Langkah 1: Membersihkan background dari proses Chromium/Driver yang nyangkut"""
    print("[1] Memeriksa proses latar belakang...")
    os.system("pkill -f chromium")
    os.system("pkill -f chromedriver")
    print("[✔] Semua proses Chromium & Driver telah dimatikan.")
    time.sleep(1)

def clean_all_data():
    """Langkah 2: Menghapus folder data browser (Cache/Session/Cookies)"""
    print("[2] Membersihkan Cache, Cookies, dan Session lama...")
    profile_path = "/data/data/com.termux/files/home/chrome_profile"
    if os.path.exists(profile_path):
        try:
            shutil.rmtree(profile_path)
            print("[✔] Folder profile (/chrome_profile) berhasil dihapus total.")
        except Exception as e:
            print(f"[!] Gagal menghapus folder: {e}")
    else:
        print("[i] Folder profile sudah bersih.")
    return profile_path

def run_bot(my_reff_link):
    global last_ip
    
    # --- MULAI PROSES PEMBERSIHAN ---
    kill_browser_processes()
    user_data_dir = clean_all_data()

    # --- CEK IP ---
    print("[3] Mengecek alamat IP saat ini...")
    try:
        current_ip = requests.get('https://api.ipify.org', timeout=10).text
        print(f"[i] IP Publik Terdeteksi: {current_ip}")
    except:
        print("[!] Gagal mendapatkan IP. Periksa koneksi internet!")
        return False
    
    if current_ip == last_ip:
        print("[×] ERROR: IP masih sama dengan sebelumnya! Harap Mode Pesawat lagi.")
        return False
    
    last_ip = current_ip

    # --- PREPARASI BROWSER ---
    ua = f"Mozilla/5.0 (Linux; Android {random.randint(11, 14)}; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(120, 126)}.0.0.0 Mobile Safari/537.36"
    print(f"[4] Menggunakan User-Agent: {ua}")
    
    if os.path.exists("captcha.png"): 
        os.remove("captcha.png")
        print("[i] File captcha lama dihapus.")

    options = Options()
    options.binary_location = "/data/data/com.termux/files/usr/bin/chromium-browser"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'--user-agent={ua}')
    options.add_argument(f'--user-data-dir={user_data_dir}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    print("[5] Meluncurkan browser Chromium...")
    driver = webdriver.Chrome(service=Service("/data/data/com.termux/files/usr/bin/chromedriver"), options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        # --- NAVIGASI ---
        print(f"[6] Membuka Link Reff: {my_reff_link}")
        driver.get(my_reff_link)
        time.sleep(3)

        print("[7] Mencari tombol 'Create Account'...")
        try:
            btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn2.btn-success")))
            driver.execute_script("arguments[0].click();", btn)
            print("[✔] Tombol diklik.")
        except:
            print("[!] Tombol tidak ketemu, bypass langsung ke halaman registrasi...")
            driver.get("https://gamety.org/?pages=reg")

        # --- ISI FORM ---
        print("[8] Mengisi formulir pendaftaran...")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "login")))
        user = "user" + "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        
        driver.find_element(By.NAME, "login").send_keys(user)
        driver.find_element(By.NAME, "email").send_keys(f"{user}@gmail.com")
        driver.find_element(By.NAME, "pass").send_keys("Pass1234!")
        print(f"[i] Data Dibuat: {user} | Pass1234!")
        
        # --- CAPTCHA ---
        print("[9] Menarik layar ke posisi Captcha...")
        captcha_el = driver.find_element(By.ID, "cap_img")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", captcha_el)
        time.sleep(3) 
        driver.save_screenshot("captcha.png")
        os.system("cp captcha.png /sdcard/Download/captcha.png 2>/dev/null")
        print("[✔] Captcha disimpan di /sdcard/Download/captcha.png")
        
        captcha_code = input(">>> Masukkan 4 angka captcha: ")
        
        print(f"[10] Memasukkan captcha '{captcha_code}' dan mengirim data...")
        driver.find_element(By.NAME, "cap").send_keys(captcha_code)
        time.sleep(2)
        driver.find_element(By.NAME, "sub_reg").click()

        # --- RESPON ---
        print("[11] Menunggu konfirmasi dari server (10 detik)...")
        time.sleep(10)
        
        try:
            swal = driver.find_element(By.CLASS_NAME, "swal-text")
            original_msg = swal.text
            print(f"\n[!] RESPON WEB ASLI: {original_msg}")
            
            with open("data_reff.txt", "a") as f:
                f.write(f"User: {user} | IP: {current_ip} | Status: {original_msg}\n")
        except:
            print(f"\n[✔] SUKSES: Akun {user} berhasil terdaftar!")
            with open("data_reff.txt", "a") as f:
                f.write(f"User: {user} | IP: {current_ip} | Status: SUKSES\n")

    except Exception as e:
        print(f"[!] Terjadi kesalahan teknis: {str(e)[:100]}")
    finally:
        print("[12] Menutup browser dan membersihkan sisa proses...")
        if driver:
            driver.quit()
        kill_browser_processes()
        print("[✔] Selesai. Sistem kembali bersih.")

if __name__ == "__main__":
    MY_LINK = "https://gamety.org/?ref=53636"
    print("="*45)
    print("   BOT REFERRAL GAMETY - MODE LOG DETAIL   ")
    print("="*45)
    while True:
        print("\n--- PERSIAPAN PUTARAN BARU ---")
        print("PENTING: Aktifkan Mode Pesawat selama 15 detik!")
        input(">>> Tekan ENTER jika sudah ganti IP (Mode Pesawat OFF)...")
        run_bot(MY_LINK)
        print("\n" + "="*45)
