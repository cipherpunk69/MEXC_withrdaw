import time
import hmac
import hashlib
import requests
import json
from urllib.parse import urlencode

API_KEY = ''
API_SECRET = ''
BASE_URL = 'https://api.mexc.com'

def get_signature(query_string: str, secret: str) -> str:
    return hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def withdraw(coin, address, amount, network):
    endpoint = '/api/v3/capital/withdraw/apply'
    url = BASE_URL + endpoint
    timestamp = int(time.time() * 1000)
    params = {
        'coin': coin,
        'address': address,
        'amount': amount,
        'network': network,
        'timestamp': timestamp
    }
    query_string = urlencode(sorted(params.items()))
    signature = get_signature(query_string, API_SECRET)
    full_query = f"{query_string}&signature={signature}"
    headers = {
        'X-MEXC-APIKEY': API_KEY
    }
    final_url = f"{url}?{full_query}"
    response = requests.post(final_url, headers=headers)
    print("📡 Status:", response.status_code)
    print("📦 Response:", response.text)

def main():
    coin_name = input("Enter coin name: ")
    networks = []
    addresses = []
    with open('data.json', 'r') as f:
        data = json.load(f)
    with open('address_book.txt', 'r') as f:
        for line in f:
            addresses.append(line.strip())
    for coin in data:
        if coin['coin'] == coin_name:
            for network in coin['networkList']:
                networks.append(network['network'])
    if len(networks) == 0:
        print("NO SUCH COIN")
    else:
        for network in networks:
            print(network)
        network_name = input("Enter network name: ")
        amount = input("Enter amount: ")
    for address in addresses:
        withdraw(coin_name, address, amount, network_name)

if __name__ == "__main__":
    main()