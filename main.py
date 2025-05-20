import os
import requests
from bs4 import BeautifulSoup

# 从 GitHub Secrets 读取环境变量
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def fetch_latest_weibo():
    url = "https://weibo.cn/5780100022"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    first = soup.find("div", class_="c")
    if not first: return None
    text = first.find("span", class_="ctt")
    if not text: return None
    return text.text.strip(), "https://weibo.com/u/5780100022"

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
