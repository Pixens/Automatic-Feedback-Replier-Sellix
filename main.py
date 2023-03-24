import yaml, requests, time, os
from colorama import Fore, Style

os.system("")

config = yaml.safe_load(open(f"config.yml", "r"))

key = config['api_key']

r = requests.get("https://dev.sellix.io/v1/feedback", headers = {"Authorization": f"Bearer {key}"})
if r.status_code == 401:
    print(f"{Fore.RED}{Style.BRIGHT}[-] Input a valid API key dumbfuck")
    quit()

no_reply = []

def countdown(t):
    
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(f"{Fore.GREEN}{Style.BRIGHT}[+] {timer}{Fore.RESET}", end="\r")
        time.sleep(1)
        t -= 1
      
    print(f"{Fore.GREEN}{Style.BRIGHT}[+] Checking for new reviews {Fore.RESET}")

while True:
    r = requests.get("https://dev.sellix.io/v1/feedback", headers = {"Authorization": f"Bearer {key}"})

    for i in r.json()['data']['feedback']:
        if i['reply'] == None:
            no_reply.append(i['uniqid'])
            print(f"{Fore.YELLOW}{Style.BRIGHT}[+] Found a new review with ID: {i['uniqid']}{Fore.RESET}")
    

        
    if no_reply:
        for i in no_reply:
            r = requests.post(f"https://dev.sellix.io/v1/feedback/reply/{i}", headers = {"Authorization": f"Bearer {key}"}, json = {"reply": config['message']})
            if r.status_code == 200:
                print(f"{Fore.CYAN}{Style.BRIGHT}[+] Successfully replied to review with ID: {i}{Fore.RESET}")
    else:
        print(f"{Fore.RED}{Style.BRIGHT}[-] No new reviews found {Fore.RESET}")
        
    no_reply = []
    
    countdown(config['delay'])
