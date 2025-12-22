import time, random, string, os, requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Variabel pemantau IP
last_ip = None

def get_current_ip():
    """Mengecek IP publik saat ini"""
    try:
        return requests.get('https://api.ipify.org', timeout=10).text
    except:
        return "Gagal Cek IP"

def get_random_ua():
    """Mengacak User-Agent Android (Samsung, Pixel, Xiaomi, Sony)"""
    devices = ["SM-S918B", "Pixel 7 Pro", "M2102K1G", "SM-A546B", "XQ-CT54"]
    chrome_ver = f"{random.randint(118, 125)}.0.{random.randint(5000, 6000)}"
    return f"Mozilla/5.0 (Linux; Android {random.randint(11, 14)}; {random.choice(devices)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Mobile Safari/537.36"

def save_account(user, password, status, ip):
    """Menyimpan hasil ke file data_reff.txt"""
    with open("data_reff.txt", "a") as f:
        f.write(f"User: {user} | Pass: {password} | IP: {ip} | Status: {status} | Tgl: {time.strftime('%Y-%m-%d %H:%M')}\n")

def run_bot(my_reff_link):
    global last_ip
    
    # 1. CEK IP SEBELUM JALAN
    current_ip = get_current_ip()
    print(f"\n[i] IP Publik: {current_ip}")
    
    if current_ip == last_ip and current_ip != "Gagal Cek IP":
        print("[!] GAGAL: IP belum berubah! Silahkan Mode Pesawat dulu.")
        return False
    
    last_ip = current_ip

    # 2. BERSIHKAN CAPTCHA LAMA
    if os.path.exists("captcha.png"):
        os.remove("captcha.png")

    PATH_BROWSER = "/data/data/com.termux/files/usr/bin/chromium-browser"
    PATH_DRIVER = "/data/data/com.termux/files/usr/bin/chromedriver"
    os.system(f"chmod +x {PATH_BROWSER} {PATH_DRIVER}")

    # 3. SETTING BROWSER
    ua = get_random_ua()
    options = Options()
    options.binary_location = PATH_BROWSER
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--incognito') 
    options.add_argument(f'--user-agent={ua}')
    options.add_argument('--window-size=1080,1920') 
    
    service = Service(executable_path=PATH_DRIVER)
    driver = None
    
    try:
        driver = webdriver.Chrome(service=service, options=options)
        print(f"[+] Membuka Link: {my_reff_link}")
        driver.get(my_reff_link) 

        # 4. KLIK TOMBOL 'CREATE AN ACCOUNT'
        try:
            btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn2.btn-success")))
            time.sleep(1)
            driver.execute_script("arguments[0].click();", btn)
        except:
            driver.get("https://gamety.org/?pages=reg")

        # 5. ISI FORM PENDAFTARAN
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "login")))
        user = "user" + "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        pw = "Pass1234!"
        
        driver.find_element(By.NAME, "login").send_keys(user)
        time.sleep(1)
        driver.find_element(By.NAME, "email").send_keys(f"{user}@gmail.com")
        time.sleep(1)
        driver.find_element(By.NAME, "pass").send_keys(pw)
        
        # 6. SCROLL KE CAPTCHA
        print("[+] Menarik layar ke Captcha...")
        captcha_el = driver.find_element(By.ID, "cap_img")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", captcha_el)
        time.sleep(3) 
        driver.save_screenshot("captcha.png")
        os.system("cp captcha.png /sdcard/Download/captcha.png 2>/dev/null")
        
        print(f"\n[!] DATA: {user} | {pw}")
        captcha_code = input(">>> Masukkan 4 angka captcha: ")
        
        # 7. INPUT CAPTCHA & SUBMIT DENGAN JEDA
        print(f"[+] Memasukkan captcha: {captcha_code}")
        input_cap = driver.find_element(By.NAME, "cap")
        input_cap.send_keys(captcha_code)
        
        time.sleep(2) # Jeda sebelum klik pendaftaran
        print("[+] Menekan tombol pendaftaran...")
        driver.find_element(By.NAME, "sub_reg").click()
        
        # 8. JEDA SETELAH SUBMIT & DETEKSI ERROR
        print("[+] Menunggu respon server (7 detik)...")
        time.sleep(7) 
        
        try:
            # Cek popup SweetAlert
            swal = driver.find_element(By.CLASS_NAME, "swal-text")
            pesan = swal.text
            if "already been registration from this IP" in pesan:
                print(f"[×] GAGAL: {pesan}")
                save_account(user, pw, "GAGAL (IP ADDRESS)", current_ip)
                return False
        except:
            print(f"[✔] SUKSES: Akun {user} terdaftar!")
            save_account(user, pw, "SUKSES", current_ip)
            return True

    except Exception as e:
        print(f"[!] Error: {str(e)[:50]}")
        return False
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    MY_LINK = "https://gamety.org/?ref=53636"
    print("=== BOT REFERRAL FINAL (TERMUX) ===")
    while True:
        status = run_bot(MY_LINK)
        print("\n" + "="*40)
        print("WAJIB MODE PESAWAT SELAMA 10 DETIK!")
        print("="*40)
        input(">>> Tekan ENTER setelah ganti IP...")
