import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = "你可以先填 test"
TELEGRAM_CHAT_ID = "你可以先填 123456"

def fetch_latest_weibo():
    url = "https://weibo.cn/5780100022"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    first = soup.find("div", class_="c")
    if not first: return
    text = first.find("span", class_="ctt").text
    link = "https://weibo.com/u/5780100022"
    return text.strip(), link

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, data=data)

def main():
    result = fetch_latest_weibo()
    if result:
        text, link = result
        send_telegram(f"夏之光发微博了：\n\n{text}\n\n→ 查看原文：{link}")

if __name__ == "__main__":
    main()
