from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ChromeDriverのパスを指定
chrome_driver_path = '../chromedriver/chromedriver'

# Chromeオプションを設定
chrome_options = Options()
# ヘッドレスモードをオフにする
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920x1080')  # ウィンドウサイズを設定

# Chromeドライバーのサービスを作成
service = Service(chrome_driver_path)

# Chromeブラウザーを起動
driver = webdriver.Chrome(service=service, options=chrome_options)

# HTMLファイルのパスを指定
file_path = 'file:///Users/shota/programs/rand/Hackathon/Hackathon_vol.10/html/deck_map.html'
file_path = 'file:///Users/shota/Downloads/Mac%E3%81%AE%E3%83%95%E3%82%9A%E3%83%AD%E3%82%BB%E3%83%83%E3%82%B5%E3%81%8B%E3%82%99ARM%E3%81%8BIntel%E3%81%8B%E3%82%92%E7%B0%A1%E5%8D%98%E3%81%AB%E7%A2%BA%E8%AA%8D%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95%20%23intel%20-%20Qiita.html'

# 指定したURLを開く
driver.get(file_path)
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'canvas')))
# ページが完全に読み込まれるまで待機
time.sleep(30)  # 待機時間を増やす

# 特定の要素が表示されるまで待機
try:
    element_present = EC.presence_of_element_located((By.CSS_SELECTOR, 'canvas'))  # 'canvas'要素が存在することを確認
    WebDriverWait(driver, 30).until(element_present)
except Exception as e:
    print("Error:", e)

# スクリーンショットを撮る
screenshot_path = 'deck_map_screenshot.png'
driver.save_screenshot(screenshot_path)

# ブラウザーを閉じる
driver.quit()

print(f'Screenshot saved to {screenshot_path}')
