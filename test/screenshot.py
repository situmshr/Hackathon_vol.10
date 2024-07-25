from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# ChromeDriverのパスを指定
chrome_driver_path = '/path/to/chromedriver'

# Chromeオプションを設定
chrome_options = Options()
chrome_options.add_argument('--headless')  # ヘッドレスモードで実行
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920x1080')  # ウィンドウサイズを設定

# Chromeドライバーのサービスを作成
service = Service(chrome_driver_path)

# Chromeブラウザーを起動
driver = webdriver.Chrome(service=service, options=chrome_options)

# HTMLファイルのパスを指定
file_path = 'file:///path/to/your/deck_map.html'

# 指定したURLを開く
driver.get(file_path)

# ページが完全に読み込まれるまで待機
time.sleep(5)

# スクリーンショットを撮る
screenshot_path = 'deck_map_screenshot.png'
driver.save_screenshot(screenshot_path)

# ブラウザーを閉じる
driver.quit()

print(f'Screenshot saved to {screenshot_path}')
