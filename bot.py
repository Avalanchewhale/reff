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

def clean_all_data():
    # Hapus folder profile
    profile_path = "/data/data/com.termux/files/home/chrome_profile"
    if os.path.exists(profile_path):
        try: shutil.rmtree(profile_path)
        except: pass
    
    # AUTO-DELETE: Hapus captcha lama agar tidak tertukar
    if os.path.exists("captcha.png"):
        os.remove("captcha.png")
        print("[✔] File captcha lama dihapus.")
    
    return profile_path

def run_bot(my_reff_link):
    global last_ip
    driver = None 
    kill_browser_processes()
    user_data_dir = clean_all_data()

    try:
        current_ip = requests.get('https://api.ipify.org', timeout=10).text
        print(f"[i] IP Sekarang: {current_ip}")
    except:
        print("[!] Gagal cek IP!")
        return False
    
    if current_ip == last_ip:
        print("[!] Ganti IP dulu!")
        return False
    
    last_ip = current_ip

    ua = f"Mozilla/5.0 (Linux; Android {random.randint(11, 14)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
    options = Options()
    # Path yang benar (Hanya 2x kata data)
    options.binary_location = "/data/data/com.termux/files/usr/bin/chromium-browser"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'--user-agent={ua}')
    options.add_argument(f'--user-data-dir={user_data_dir}')
    options.add_argument('--dns-over-https=https://dns.google/dns-query')
    options.add_argument('--disable-webrtc')

    try:
        service = Service("/data/data/com.termux/files/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)
        
        print("[+] Membuka web...")
        driver.get(my_reff_link)
        time.sleep(7)

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
        
        # Simpan Captcha Baru
        captcha_el = driver.find_element(By.ID, "cap_img")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", captcha_el)
        time.sleep(2) 
        driver.save_screenshot("captcha.png")
        os.system("cp captcha.png /sdcard/Download/captcha.png 2>/dev/null")
        
        print(f"\n[DATA] User: {user}")
        captcha_code = input(">>> Ketik Captcha: ")
        
        driver.find_element(By.NAME, "cap").send_keys(captcha_code)
        driver.find_element(By.NAME, "sub_reg").click()

        # DETEKSI CAPTCHA SALAH
        print("[+] Menunggu respon...")
        time.sleep(10)
        try:
            # Mencari tulisan "incorrect" seperti di foto kamu
            msg = driver.find_element(By.CLASS_NAME, "swal-text").text
            print(f"[!] NOTIF: {msg}")
            if "incorrect" in msg.lower():
                print("[×] Captcha salah, putaran ini gagal.")
                return False
        except:
            print("[✔] Tidak ada error, kemungkinan besar sukses!")

    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        if driver: driver.quit()
        kill_browser_processes()

if __name__ == "__main__":
    MY_LINK = "https://gamety.org/?ref=53636"
    while True:
        input("\n>>> [ENTER] Setelah Ganti IP...")
        run_bot(MY_LINK)
