#必要なライブラリをインポート
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import io
import os
import streamlit as st

st.title("田村保乃のブログ保存サイト")
act = st.button("実行")
if act:
        #藤吉夏鈴のブログ一覧ページに飛ぶ
        browser = webdriver.Chrome(ChromeDriverManager().install())
        #山﨑天のブログ一覧ページのurlを記載
        ##保存したい人のブログ一覧ページのアドレスに変更
        browser.get("https://sakurazaka46.com/s/s46/diary/blog/list?ima=3416&ct=46")
        #最新ブログのページに遷移
        go_to_new_blog = browser.find_element_by_class_name("box")
        go_to_new_blog.click()
        #その最新ブログのurlを取得
        url = browser.current_url
        #htmlを取得
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        spots = soup.find_all("div", attrs = {"class": "gmail_quote"})

        #ブログの更新日付を取得
        date = soup.find_all("p", attrs = {"class": "date wf-a"})[1].text
        date = date.split(" ")[0]
        date = date.replace("/", "_")

        #山﨑天フォルダに保存
        os.makedirs(f"{date}")
        #画像取得
        img_tags = soup.find_all("img")[1:-5]
        for i, img_tag in enumerate(img_tags):
                try:
                        
                        root_url = "https://sakurazaka46.com"
                        img_url = root_url + img_tag["src"]

                        #画像表示
                        img = Image.open(io.BytesIO(requests.get(img_url).content)).convert("RGB")
                except:
                        print(f"{date}の{i}枚目の写真は特定できず、ダウンロードできませんでした。")
                        continue
                else:
                        #写真を藤吉夏鈴フォルダに保存
                        img.save(f"{date}/{i}.jpg")
                        
        print("処理が終了しました。")