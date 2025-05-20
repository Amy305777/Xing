import os
import requests
from bs4 import BeautifulSoup

# 从 GitHub Secrets 获取配置
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def fetch_latest_weibo():
    url = "https://weibo.cn/5780100022"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")
    divs = soup.find_all("div", class_="c")
    for div in divs:
        if div.get("id") and "M_" in div.get("id"):
            text = div.find("span", class_="ctt").text.strip()
            return text, "https://weibo.com/u/5780100022"
    return None

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    print("== 发送请求到 Telegram ==")
    print(f"URL: {url}")
    print(f"DATA: {data}")
    response = requests.post(url, data=data)
    print("== 返回状态码 ==")
    print(response.status_code)
    print("== 返回内容 ==")
    print(response.text)
    response.raise_for_status()

def main():
    print("== 开始抓取微博 ==")
    result = fetch_latest_weibo()
    if result:
        text, link = result
        message = f"夏之光发微博了：\\n\\n{text}\\n\\n→ 查看原文：{link}"
        send_telegram(message)
    else:
        print("没有获取到微博内容")

if __name__ == "__main__":
    main()
