import os
import sys
import time
import requests
from colorama import *
from datetime import datetime

red = Fore.LIGHTRED_EX
yellow = Fore.LIGHTYELLOW_EX
green = Fore.LIGHTGREEN_EX
black = Fore.LIGHTBLACK_EX
blue = Fore.LIGHTBLUE_EX
white = Fore.LIGHTWHITE_EX
reset = Style.RESET_ALL

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the full paths to the files
data_file = os.path.join(script_dir, "data.txt")


# Clear the terminal
def clear_terminal():
    # For Windows
    if os.name == "nt":
        _ = os.system("cls")
    # For macOS and Linux
    else:
        _ = os.system("clear")


class Pocketfi:
    def __init__(self):
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Host": "rubot.pocketfi.org",
            "Origin": "https://pocketfi.app",
            "Referer": "https://pocketfi.app/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
            "sec-ch-ua": '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
        }
        self.line = white + "~" * 50

    def next_claim_is(self, last_claim):
        next_claim = last_claim + 3600
        now = datetime.now().timestamp()
        tetod = round(next_claim - now)
        return tetod

    def http(self, url, headers, data=None):
        while True:
            try:
                if data is None:
                    res = requests.get(url, headers=headers)
                    return res

                if data == "":
                    res = requests.post(url, headers=headers)
                    return res

                res = requests.post(url, headers=headers, data=data)
                return res

            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                self.log(f"{red}Connection error / Connection timeout !")
                time.sleep(1)
                continue

    def countdown(self, t):
        while t:
            menit, detik = divmod(t, 60)
            jam, menit = divmod(menit, 60)
            jam = str(jam).zfill(2)
            menit = str(menit).zfill(2)
            detik = str(detik).zfill(2)
            print(f"{white}Time left: {jam}:{menit}:{detik} ", flush=True, end="\r")
            t -= 1
            time.sleep(1)
        print("                          ", flush=True, end="\r")

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{black}[{now}] {reset}{msg}")

    def get_user_mining(self, tg_data):
        url = "https://rubot.pocketfi.org/mining/getUserMining"
        url_claim = "https://rubot.pocketfi.org/mining/claimMining"
        headers = self.headers.copy()
        headers["telegramRawData"] = tg_data
        res = self.http(url, headers)
        balance = res.json()["userMining"]["gotAmount"]
        last_claim = res.json()["userMining"]["dttmLastClaim"] / 1000
        self.log(f"{green}Balance : {white}{balance}")
        can_claim = self.next_claim_is(last_claim)
        if can_claim >= 0:
            self.log(f"{yellow}Claim too early !")
            return can_claim

        res = self.http(url_claim, headers, "")
        new_balance = res.json()["userMining"]["gotAmount"]
        self.log(f"{green}Balance after claim : {white}{new_balance}")
        return 3600

    def main(self):
        clear_terminal()
        banner = f"""
    {blue}Smart Airdrop {white}PocketFi Auto Claimer
    t.me/smartairdrop2120
    
        """
        print(banner)
        datas = open(data_file, "r").read().splitlines()
        if len(datas) <= 0:
            self.log(f"{red}Add data account in data.txt first !")
            sys.exit()
        self.log(f"{blue}Number of accounts : {white}{len(datas)}")
        print(self.line)
        while True:
            list_countdown = []
            _start = int(time.time())
            for no, data in enumerate(datas):
                self.log(f"{blue}Account number : {white}{no + 1}/{len(datas)}")
                res = self.get_user_mining(data)
                print(self.line)
                list_countdown.append(res)
            _end = int(time.time())
            _tot = _end - _start
            if _tot <= 0:
                continue

            _min = min(list_countdown) - _tot
            self.countdown(_min)


if __name__ == "__main__":
    try:
        pocketfi = Pocketfi()
        pocketfi.main()
    except KeyboardInterrupt:
        sys.exit()
