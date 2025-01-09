import os
import time
import urllib3
import warnings
import requests
from dotenv import load_dotenv

warnings.simplefilter(action='ignore', category=FutureWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

API_KEY = os.getenv('API_KEY')
PFSENSE_URL = os.getenv('PFSENSE_URL')
PFSENSE_PORT = os.getenv('PFSENSE_PORT')
PHYSICAL_PORT = os.getenv('PHYSICAL_PORT')
HEADERS = {
        'accept': 'application/json',
        'x-api-key': API_KEY,
        'Content-Type': 'application/json'
    }

def _apply_get(h, section='interface'):
    try:
        time.sleep(5) # Required for the request to the Server to be updated
        response = requests.get(f'https://{PFSENSE_URL}:{PFSENSE_PORT}/api/v2/{section}/apply', verify=False, headers=h)
        if response.status_code != 200:
            raise(f"Failed to get request. status code: {response.status_code}")
        data = response.json()
        if data:
            applied = data.get('data').get('applied')
        return applied
    except Exception as e:
        print("_apply_get: Failed to connect")
        print(e)
        return False

def _apply_post(h, section='interface'):
    try:
        time.sleep(5) # Required for the request to the Server to be updated
        response = requests.post(f'https://{PFSENSE_URL}:{PFSENSE_PORT}/api/v2/{section}/apply', verify=False, headers=h, json={})
        if response.status_code != 200:
            raise(f"Failed to post request. status code: {response.status_code}")
        data = response.json()
        if data:
            applied = data.get('data').get('applied')
        return applied
    except Exception as e:
        print("_apply_post: Failed to connect")
        print(e)
        return False
                
def get_wan_status(h):
    try:
        response = requests.get(f'https://{PFSENSE_URL}:{PFSENSE_PORT}/api/v2/status/interfaces?limit=0&offset=0', verify=False, headers=h)
        if response.status_code != 200:
            raise(f"Failed to get request. status code: {response.status_code}")
        data = response.json()
        if data:
            status = data.get('data')[0].get('status') # [0] is the WAN Interface in the output, Change depend on your output
        return status
    except Exception as e:
        print("get_wan_status: Failed to connect")
        print(e)

def reset_wan_interface(h, status):
    try:
        data = f'{{"id": "wan", "if": "{PHYSICAL_PORT}", "enable": {status}}}'
        response = requests.patch(f'https://{PFSENSE_URL}:{PFSENSE_PORT}/api/v2/interface', verify=False, headers=h, data=data)
        if response.status_code != 200:
            raise(f"Failed to get request. status code: {response.status_code}")
        data = response.json()
        if data:
            _apply_post(h=HEADERS, section='interface')
            result_get = _apply_get(h=HEADERS, section='interface')
        if (result_get and status == 'false'):
            reset_wan_interface(h=HEADERS, status='true')
        return result_get
    except Exception as e:
        print("reset_wan_interface: Failed to connect")
        print(e)
       
if __name__ == "__main__":
    while True:
        status = get_wan_status(h=HEADERS)
        if status != 'up':
            print('WAN is OFFLINE!!!\nInitiate WAN Reset...')
            result = reset_wan_interface(h=HEADERS, status='false')
            if result:
                print("WAN is Back ONLINE!")
        time.sleep(20)
    