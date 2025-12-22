import time, random, string, os, requests, shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

last_ip = None

def kill_browser_processes():
    """Memastikan tidak ada proses yang nyangkut"""
    os.system("pkill -f chromium")
    os.system("pkill -f chromedriver")
    time.sleep(1)

def get_current_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=10).text
    except:
        return "Gagal Cek IP"

def clean_all_data():
    profile_path = "/data/data/com.termux/files/home/chrome_profile"
    if os.path.exists(profile_path):
        try:
            shutil.rmtree(profile_path)
        except:
            pass
    return profile_path

def get_random_ua():
    # Gunakan UA yang sangat spesifik dan terbaru
    devices = ["SM-S918B", "Pixel 8 Pro", "M2101K6G", "SM-G973F", "Xiaomi 13T", "POCO F5"]
    chrome_ver = f"{random.randint(120, 126)}.0.{random.randint(6000, 7000)}"
    return f"Mozilla/5.0 (Linux; Android {random.randint(11, 14)}; {random.choice(devices)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Mobile Safari/537.36"

def run_bot(my_reff_link):
    global last_ip
    
    kill_browser_processes()
    current_ip = get_current_ip()
    print(f"\n[i] IP Publik : {current_ip}")
    
    if current_ip == last_ip and current_ip != "Gagal Cek IP":
        print("[!] GAGAL: IP belum berubah!")
        return False
    
    last_ip = current_ip
    user_data_dir = clean_all_data()
    ua = get_random_ua()
    print(f"[i] User-Agent: {ua}")

    PATH_BROWSER = "/data/data/com.termux/files/usr/bin/chromium-browser"
    PATH_DRIVER = "/data/data/com.termux/files/usr/bin/chromedriver"

    options = Options()
    options.binary_location = PATH_BROWSER
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'--user-agent={ua}')
    options.add_argument(f'--user-data-dir={user_data_dir}')
    options.add_argument('--incognito')
    
    # --- TAMBAHAN ANTI-FINGERPRINT AGAR TIDAK KEDETEK ---
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # Mematikan fitur yang sering dipakai web untuk melacak bot
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-site-isolation-trials")

    driver = webdriver.Chrome(service=Service(PATH_DRIVER), options=options)
    
    # Script untuk menyembunyikan Selenium & mengacak sidik jari Canvas
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.chrome = { runtime: {} };
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) return 'Intel Inc.';
                if (parameter === 37446) return 'Intel(R) Iris(R) Xe Graphics';
                return getParameter(parameter);
            };
        """
    })

    try:
        driver.get(my_reff_link)
        time.sleep(random.uniform(4, 6)) # Jeda lebih lama agar terlihat natural

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
            time.sleep(random.uniform(0.1, 0.3))
        
        driver.find_element(By.NAME, "email").send_keys(f"{user}@gmail.com")
        driver.find_element(By.NAME, "pass").send_keys("Pass1234!")
        
        # Simpan Captcha
        captcha_el = driver.find_element(By.ID, "cap_img")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", captcha_el)
        time.sleep(3) 
        driver.save_screenshot("captcha.png")
        os.system("cp captcha.png /sdcard/Download/captcha.png 2>/dev/null")
        
        print(f"\n[!] DATA: {user}")
        captcha_code = input(">>> Masukkan Captcha: ")
        
        driver.find_element(By.NAME, "cap").send_keys(captcha_code)
        time.sleep(random.uniform(2, 4))
        driver.find_element(By.NAME, "sub_reg").click()

        print("[+] Menunggu respon server (12 detik)...")
        time.sleep(12)
        
        try:
            swal = driver.find_element(By.CLASS_NAME, "swal-text")
            print(f"[!] Respon Web: {swal.text}")
            return False
        except:
            print(f"[✔] SUKSES: Akun {user} terdaftar!")
            return True

    finally:
        if driver: driver.quit()
        kill_browser_processes()

if __name__ == "__main__":
    MY_LINK = "https://gamety.org/?ref=53636"
    while True:
        print("\n" + "="*40 + "\nWAJIB MODE PESAWAT 15 DETIK!\n" + "="*40)
        input(">>> Tekan ENTER setelah ganti IP...")
        run_bot(MY_LINK)
