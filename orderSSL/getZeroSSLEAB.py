import requests
import os
from dotenv import load_dotenv

def gen_zero_ssl_eab():
    load_dotenv()    
    apikey = os.getenv("ZEROSSL_API")
    if not apikey:
        print("Error: API key not found. Ensure it's set in your environment variables.")
        return "Error", "Error"
    
    url = f"https://api.zerossl.com/acme/eab-credentials?access_key={apikey}"
    headers = {'Content-Type': 'application/json'}
    
    try:
        resp = requests.post(url, headers=headers)
        resp_json = resp.json()
        
        if resp.status_code == 200 and resp_json.get('success') == 1:
            kid = resp_json.get('eab_kid')
            hmac = resp_json.get('eab_hmac_key')
            print(f"Kid: {kid}\nHMAC: {hmac}")
            return kid, hmac
        else:
            print(f"Error: {resp_json.get('error', 'Unknown error')}")
            return "Error", "Error"
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return "Error", "Error"
