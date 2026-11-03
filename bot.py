import os
import requests
from bs4 import BeautifulSoup

MARKET_URL = "https://bless.gs/en/index.php?page=market&serv=server2"
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
SEARCH_KEYWORD = "Wings"  # Change to your target item

def check_market():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(MARKET_URL, headers=headers, timeout=10)
        if response.status_code != 200:
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('tr')
        
        for row in rows:
            row_text = row.get_text(strip=True)
            if SEARCH_KEYWORD.lower() in row_text.lower():
                payload = {
                    "username": "Bless Market Bot",
                    "embeds": [{
                        "title": "🚨 Target Item Found!",
                        "description": f"**Match:** {row_text}\n[Check Market]({MARKET_URL})",
                        "color": 5763719
                    }]
                }
                requests.post(DISCORD_WEBHOOK_URL, json=payload)
                break  # Alert once per check if found
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_market()
