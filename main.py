import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import threading
import requests
import yaml
import random

class BotView:
    def __init__(self, config_path='config.yml'):
        self.config_path = config_path
        self.load_config(config_path)
        self.time_session = self.config.get('time_session', 25)
        self.enable_proxy = self.config.get('enable_proxy', False)
        self.link_attack = self.config.get('link_attack', '')
        self.proxies = self.convert_proxies(self.config.get('proxies', ''))
        self.semaphore = threading.Semaphore(self.config.get('semaphore', 5))

    def setLinkAttack(self, link):
        self.link_attack = link
    
    def setProxies(self, proxies = None):
        if proxies is None:
            self.proxies = self.convert_proxies(self.config.get('proxies', ''))
        else:
            self.proxies = proxies

    def setSemaphore(self, semaphore: int):
        self.semaphore = threading.Semaphore(semaphore)
    
    def setEnableProxy(self, enable_proxy: bool):
        self.enable_proxy = enable_proxy
    
    def setTimeSession(self, time_session: int):
        self.time_session = time_session

    def load_config(self, config_path):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

    def save_config(self):
        self.config['samephore'] = self.semaphore._value
        with open(self.config_path, 'w') as file:
            yaml.safe_dump(self.config, file)

    def convert_proxies(self, proxies_str):
        return [proxy.strip() for proxy in proxies_str.split('\n') if proxy.strip()]
    
    def get_random_user_agent(self):
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.3 Safari/602.3.12",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"
        ]
        return random.choice(user_agents)
    
    def is_proxy_working(self, proxy):
        try:
            response = requests.get(self.link_attack, proxies={'http': proxy, 'https': proxy}, timeout=5)
            return response.status_code == 200
        except:
            return False

    def run(self, proxy: str):
        with self.semaphore:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument(f'user-agent={self.get_random_user_agent()}')
            if self.enable_proxy and proxy:
                if not self.is_proxy_working(proxy):
                    print(f'Proxy {proxy} is not working')
                    return
                else:
                    print(f'Running session with proxy {proxy}')
                chrome_options.add_argument(f'--proxy-server={proxy}')
            else:
                print('No proxy, running session')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

            driver = webdriver.Chrome(options=chrome_options)
            driver.get(self.link_attack)
            time.sleep(self.time_session)
            driver.quit()
    
    def lopp(self):
        while True:
            for proxy in self.proxies:
                threading.Thread(target=self.run, args=(proxy,)).start()
            time.sleep(60)
        

    def start(self):
        print('Bienvenido al BotView\nPuedes descargar una lista de proxis en https://free-proxy-list.net/')
        if self.link_attack == 'None':
            link = input('Ingrese el link del video/web: ')
            self.setLinkAttack(link)
        else:
            print(f'Link de ataque: {self.link_attack}')
            change_link = input(f'¿Desea cambiar el link de ataque? (y/n): ')
            if change_link.lower() == 'y':
                link = input('Ingrese el link del video/web: ')
                self.setLinkAttack(link)
        enable_proxy = input('¿Desea habilitar el uso de proxy? (y/n): ')
        if enable_proxy.lower() == 'y':
            self.setEnableProxy(True)
        else:
            self.setEnableProxy(False)
        semaphore_change = input('¿Desea cambiar el número de hilos? (y/n): ')
        if semaphore_change.lower() == 'y':
            semaphore = int(input('Ingrese el número de hilos: '))
            self.setSemaphore(semaphore)
        save_config = input('¿Desea guardar la configuración? (y/n): ')
        if save_config.lower() == 'y':
            self.config['link_attack'] = self.link_attack
            self.config['enable_proxy'] = self.enable_proxy
            self.save_config()
        self.lopp()

bot = BotView()
bot.start()