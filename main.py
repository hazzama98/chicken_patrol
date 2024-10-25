from datetime import datetime
import json
import os
import random
import sys
from urllib.parse import parse_qs, unquote
import time
import requests
import base64
import json

def print_(word):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"[⚔] | {word}")

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
        
def key_bot():
    url = base64.b64decode("aHR0cDovL2l0YmFhcnRzLmNvbS9hcGkuanNvbg==").decode('utf-8')
    try:
        response = requests.get(url)
        response.raise_for_status()
        try:
            data = response.json()
            header = data['header']
            print(header)
        except json.JSONDecodeError:
            print(response.text)
    except requests.RequestException as e:
        print_(f"Failed to load header")
    
def load_query():
    try:
        with open('query.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        return queries
    except FileNotFoundError:
        print("Failed find query.txt ")
        return []
    except Exception as e:
        print("Failed find query.txt ", str(e))
        return []

def parse_query(query: str):
    parsed_query = parse_qs(query)
    parsed_query = {k: v[0] for k, v in parsed_query.items()}
    user_data = json.loads(unquote(parsed_query['user']))
    parsed_query['user'] = user_data
    return parsed_query

def get(id):
    tokens = json.loads(open("tokens.json").read())
    if str(id) not in tokens.keys():
        return None
    return tokens[str(id)]

def save(id, token):
    tokens = json.loads(open("tokens.json").read())
    tokens[str(id)] = token
    open("tokens.json", "w").write(json.dumps(tokens, indent=4))

def print_delay(delay):
    print()
    while delay > 0:
        now = datetime.now().isoformat(" ").split(".")[0]
        hours, remainder = divmod(delay, 3600)
        minutes, seconds = divmod(remainder, 60)
        sys.stdout.write(f"\r[⚔] | Waiting Time: {round(hours)} hours, {round(minutes)} minutes, and {round(seconds)} seconds")
        sys.stdout.flush()
        time.sleep(1)
        delay -= 1
    print_("\nWaiting Done, Starting....\n")

class ChickenPatrol:
    def __init__(self):
        self.header = {
            "accept": "*/*",
            "accept-language": "id-ID,id;q=0.9",
            "content-type": "application/json",
            "priority": "u=1, i",
            "sec-ch-ua": '"Telegram";v="8.4", "Not=A?Brand";v="8", "Chromium";v="110"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"iOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "Referer": "https://app.chickenpatrol.xyz/",
            "Origin":"https://app.chickenpatrol.xyz",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
        }
    def make_request(self, method, url, headers, json=None, data=None):
        retry_count = 0
        while True:
            time.sleep(2)
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, json=json)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=json, data=data)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=json, data=data)
            else:
                raise ValueError("Invalid method.")
            if response.status_code >= 500:
                if retry_count >= 4:
                    print_(f"Status Code: {response.status_code} | {response.text}")
                    return None
                retry_count += 1
                return None
            elif response.status_code >= 400:
                print_(f"Status Code: {response.status_code} | {response.text}")
                return None
            elif response.status_code >= 200:
                return response
    
    def auth(self, query):
        url = 'https://api.chickenpatrol.xyz/app/auth/authenAuthSignature'
        headers = {
            **self.header
        }
        payload = {"initData": query,"invite":"eDf33rSL"}
        
        response = self.make_request('post', url=url, headers=headers, json=payload)
        if response is not None:
            jsons = response.json()
            return jsons
    
    def get_user(self, token):
        url = 'https://api.chickenpatrol.xyz/app/user'
        headers = {
            **self.header,
            'Authorization': f"Bearer {token}"
        }
        response = self.make_request('get', url=url, headers=headers)
        if response is not None:
            jsons = response.json()
            return jsons
    
    def tap(self, token, tap):
        url = 'https://api.chickenpatrol.xyz/app/user/tap'
        headers = {
            **self.header,
            'Authorization': f"Bearer {token}"
        }
        payload = {"count":tap}
        response = self.make_request('post', url=url, headers=headers, json=payload)
        if response is not None:
            jsons = response.json()
            return jsons
    
    def buy_tcn(self, token):
        url = 'https://api.chickenpatrol.xyz/app/user/buychicktcn'
        headers = {
            **self.header,
            'Authorization': f"Bearer {token}"
        }
        response = self.make_request('get', url=url, headers=headers)
        if response is not None:
            jsons = response.json()
            data = jsons.get('data')
            print_(f"Buy Done : Rank {data.get('rank')}")
            return jsons
    
    def clear_task(self, token, title):
        url = f'https://api.chickenpatrol.xyz/app/task/{title}'
        headers = {
            **self.header,
            'Authorization': f"Bearer {token}"
        }
        response = self.make_request('get', url=url, headers=headers)
        if response is not None:
            print_(f"Tugas {title} selesai")

def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print_("File konfigurasi tidak ditemukan. Menggunakan pengaturan default.")
        return {"auto_buy_chicken": False, "auto_play_game": False, "waiting_time": 21600}
    except json.JSONDecodeError:
        print_("JSON tidak valid dalam file konfigurasi. Menggunakan pengaturan default.")
        return {"auto_buy_chicken": False, "auto_play_game": False, "waiting_time": 21600}

def main():
    config = load_config()
    auto_buy = config.get('auto_buy_chicken', False)
    auto_game = config.get('auto_play_game', False)
    waiting_time = config.get('waiting_time', 21600)
    auto_clear_tasks = config.get('auto_clear_tasks', False)
    
    while True:
        start_time = time.time()
        delay = waiting_time
        clear_terminal()
        key_bot()
        queries = load_query()
        sum = len(queries)
        chicken = ChickenPatrol()
        for index, query in enumerate(queries, start=1):
            users = parse_query(query).get('user')
            print_(f"Account {index}/{sum} | {users.get('username','')}")
            data_auth = chicken.auth(query)
            if data_auth is not None:
                token = data_auth.get('access_token')
                print_("Autentication Success")
            
                data_user = chicken.get_user(token)
                if data_user is not None:
                    user = data_user.get('user',{})
                    airdropPoint = user.get('airdropPoint',0)
                    usdt = user.get('usdt',0)
                    tap = user.get('tap',0)
                    print_(f"Balance : {usdt} USDT | {airdropPoint} TCN")
                    if auto_buy:
                        if airdropPoint >= 1000:
                            print_(f"Buying Chicken...")
                            chicken.buy_tcn(token)
                    chick = user.get('chick',[])
                    for item in chick:
                        print_(f"Chick Army : Rank {item.get('rank')}")
                    data_tap = chicken.tap(token=token, tap=tap)
                    if data_tap is not None:
                        usdt = data_tap.get('usdt')
                        airdrop = data_tap.get('airdrop')
                        print_(f"Tap : {usdt} USDT | {airdrop} TCN")
                    
                  #  if auto_game:
                        # Implementasi auto play game di sini
                    #    print_("Auto playing game...")
                        # Tambahkan logika untuk auto play game
                    
                    if auto_clear_tasks:
                        task = data_user.get('task')
                        taskOne = task.get('taskOne')
                        if not taskOne:
                            chicken.clear_task(token, 'joinchannel')
                        taskTwo = task.get('taskTwo')
                        if not taskTwo:
                            chicken.clear_task(token, 'joinchat')
                        taskThree = task.get('taskThree')
                        if not taskThree:
                            chicken.clear_task(token, 'followx')
                        taskFour = task.get('taskFour')
                        taskFive = task.get('taskFive')
                        if not taskFive:
                            chicken.clear_task(token, 'followxbinance')
                        taskSix = task.get('taskSix')
                
                end_time = time.time()
                delays = delay - (end_time - start_time)
                print_delay(delays)

if __name__ == "__main__":
    main()
