#必要なライブラリをインポート
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import io
import os
import streamlit as st

st.title("ブログ保存サイト")
act = st.button("実行")

num_lists = {
        "上村 莉奈":"03",
        "尾関 梨香":"04",
        "小池 美波":"06",
        "小林 由依":"07",
        "齋藤 冬優花":"08",
        "菅井 友香":"11",
        "土生 瑞穂":"14",
        "原田 葵":"15",
        "渡邊 理佐":"21",
        "井上 梨名":"43",
        "遠藤 光莉":"53",
        "大園 玲":"54",
        "大沼 晶保":"55",
        "幸阪 茉里乃":"56",
        "関 有美子":"44",
        "武元 唯衣":"45",
        "田村 保乃":"46",
        "藤吉夏鈴":"47",
        "増本 綺良":"57",
        "松田 里奈":"48",
        "森田 ひかる":"50",
        "守屋 麗奈":"58",
        "山﨑 天":"51"
}
member = st.selectbox("メンバーを選択してください。",(
        "上村 莉奈",
        "尾関 梨香",
        "小池 美波",
        "小林 由依",
        "齋藤 冬優花",
        "菅井 友香",
        "土生 瑞穂",
        "原田 葵",
        "渡邊 理佐",
        "井上 梨名",
        "遠藤 光莉",
        "大園 玲",
        "大沼 晶保",
        "幸阪 茉里乃",
        "関 有美子",
        "武元 唯衣",
        "田村 保乃",
        "藤吉夏鈴",
        "増本 綺良",
        "松田 里奈",
        "森田 ひかる",
        "守屋 麗奈",
        "山﨑 天"
)
                      )

st.write("選択したメンバー：",member)
if act:
        #藤吉夏鈴のブログ一覧ページに飛ぶ
        browser = webdriver.Chrome(ChromeDriverManager().install())
        #山﨑天のブログ一覧ページのurlを記載
        ##保存したい人のブログ一覧ページのアドレスに変更
        browser.get(f"https://sakurazaka46.com/s/s46/diary/blog/list?ima=3416&ct={num_lists[member]}")
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
        browser.close()