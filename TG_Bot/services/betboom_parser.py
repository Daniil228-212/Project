import pandas as pd
from datetime import datetime, timedelta
import os
import json
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
class BetBoomService:
    CACHE_FILE = "storage/betboom_cache.json"
    def __init__(self):
        self.driver = None
        os.makedirs("storage", exist_ok=True)
    def get_driver(self):
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        return Chrome(options=options)
    def load_cached_data(self):
        if not os.path.exists(self.CACHE_FILE):
            return None
        with open(self.CACHE_FILE, 'r', encoding='utf-8') as f:
            cache = json.load(f)
        last_update = datetime.fromisoformat(cache['last_update'])
        if datetime.now() - last_update < timedelta(hours=24):
            return pd.DataFrame(cache['data'])
        return None
    def save_to_cache(self, df):
        cache = {
            'last_update': datetime.now().isoformat(),
            'data': df.to_dict('records')
        }
        with open(self.CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    def parse_local_matches(self, context_element):
        data = []
        local_teams = context_element.find_elements(By.CSS_SELECTOR, '.eOSe1-bc4b27d8')
        local_odds = context_element.find_elements(By.CSS_SELECTOR, '.do7iP-bc4b27d8')
        teams = [el.text.strip() for el in local_teams if el.text.strip()]
        odds = []
        for el in local_odds:
            text = el.text.strip().replace(',', '.').replace('+', '').strip()
            if text.replace('.', '', 1).isdigit() and len(text) <= 6:
                odds.append(text)
        for j in range(0, len(teams) - 1, 2):
            if (j // 2) * 3 + 2 >= len(odds):
                continue
            p1, draw, p2 = odds[(j // 2) * 3: (j // 2) * 3 + 3]
            if all([p1, draw, p2]):
                data.append({
                    'team1': teams[j],
                    'team2': teams[j + 1],
                    'coeff_win1': float(p1),
                    'coeff_draw': float(draw),
                    'coeff_win2': float(p2),
                    'sport': 'football',
                    'timestamp': datetime.now().isoformat()
                })
        return data
    def scrape_betboom(self):
        cached_data = self.load_cached_data()
        if cached_data is not None:
            return cached_data
        self.driver = self.get_driver()
        try:
            url = "https://betboom.ru/sport/football"
            self.driver.get(url)
            time.sleep(5)
            for _ in range(4):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1.5)
            data = []
            data.extend(self.parse_local_matches(self.driver))
            match_buttons = self.driver.find_elements(By.CSS_SELECTOR, '.nFgMI-bc4b27d8')
            print(f"\nНайдено блоков для раскрытия: {len(match_buttons)}")
            for i, btn in enumerate(match_buttons[1:], start=2):
                try:
                    print(f"Обработка блока #{i}")
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                    time.sleep(0.2)
                    btn.click()
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '.eOSe1-bc4b27d8'))
                    )
                    container = btn.find_element(By.XPATH, './..')
                    block_data = self.parse_local_matches(container)
                    data.extend(block_data)
                except Exception as e:
                    print(f"Проблема с блоком #{i}: {e}")
                    continue
            df = pd.DataFrame(data)
            df.drop_duplicates(inplace=True)
            self.save_to_cache(df)
            return df
        except Exception as e:
            print(f"Ошибка парсинга: {e}")
            return pd.DataFrame()
        finally:
            if self.driver:
                self.driver.quit()