# -*- coding: utf-8 -*-


# URL轉 T-URL==anime_url_change=======================================================
# 每一集的連結 ========================================================================
def all_episode_url(url):
    import re
    import requests
    from bs4 import BeautifulSoup
    import time

    start = time.time()

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146  Safari/537.36"
    }
    webpage = requests.get(url, headers=HEADERS)
    print("all_episode_url", webpage)
    time.sleep(3)
    soup = BeautifulSoup(webpage.text, "html.parser")
    num_for_next = soup.select(
        "#BH_background > div.container-player > div.anime-title > div.anime-option > section.season > ul > li > a"
    )
    # print(num_for_next)

    if num_for_next != []:
        return [
            "https://ani.gamer.com.tw/animeVideo.php?sn="
            + re.findall('(?<=sn=).+?(?=")', str(i))[0]
            for i in num_for_next
        ]
    else:
        return [url]  # 轉成list才可以讀第0個


# 總頁數==連接 MySQL=============================================================
# 跑每一頁的動畫-->所有動畫的第一集 名稱 年份 網址 總觀看 集數  "抓要的值"===========
def total_page():
    # 總頁數====================================================================
    # =============================================================================
    from bs4 import BeautifulSoup
    import requests
    import re

    import time

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146  Safari/537.36"
    }
    url = "https://ani.gamer.com.tw/animeList.php?page=1&c=0&sort=1"
    webpage = requests.get(url, headers=HEADERS)
    print("total_page", webpage)
    time.sleep(3)
    soup = BeautifulSoup(webpage.text, "html.parser")

    lastpage = soup.select("#BH_background > div.container > div.page_control > div> a")
    # print(lastpage[-1])
    lastpage_num = re.findall('(?<=">).+?(?=</a)', str(lastpage[-1]))  # 總集數  ['55']
    # print(lastpage_num[0])  #55

    # 連接 MySQL  ------------------------------------------------------------------
    import time
    import mysql.connector
    from mysql.connector import Error

    global connection
    start = time.time()  # 測時間
    # ------------------------------------------------------------------------------
    try:
        # 連接 MySQL/MariaDB 資料庫
        connection = mysql.connector.connect(
            host="localhost",  # 主機名稱
            database="anime_ver2",  # 資料庫名稱  要先在workbench那邊建立 不然會找不到
            user="root",  # 帳號
            password="root",  # 密碼
            charset="utf8mb4",
        )

        sql = """CREATE TABLE IF NOT EXISTS anime0923(
                        url TEXT,
                        name VARCHAR(80) PRIMARY KEY,   #PK需要有個長度
                        year TEXT,
                        seesum TEXT,
                        listsum INT
                ); """  # 建立一個TABLE
        cursor = connection.cursor()
        cursor.execute(sql)  # 執行sql語句
        # ------------------------------------------------------------------------------
        # 跑每一頁的動畫-->所有動畫的第一集 名稱 年份 網址 總觀看 集數  "只有爬下來"
        for num in range(30, int(lastpage_num[0]) + 1):  # int(lastpage_num[0]) + 1
            print("第", num, "頁")
            url = (
                "https://ani.gamer.com.tw/animeList.php?page="
                + str(num)
                + "&c=0&sort=1"
            )
            webpage = requests.get(url, headers=HEADERS)
            print("animeall", webpage)
            time.sleep(3)
            soup = BeautifulSoup(webpage.text, "html.parser")

            all_anime = soup.select(
                "#BH_background > div > div.animate-theme-list > div.theme-list-block"
            )

            all_anime_url = all_anime[0].find_all(
                "a", {"class": "theme-list-main"}
            )  # 網址
            all_anime_name = all_anime[0].find_all(
                "div", {"class": "theme-info-block"}
            )  # 影片名稱
            all_anime_date = all_anime[0].find_all(
                "div", {"class": "theme-detail-info-block"}
            )  # 年份
            all_anime_seesum = all_anime[0].find_all(
                "div", {"class": "show-view-number"}
            )  # 總觀看
            all_anime_listsum = all_anime[0].find_all(
                "span", {"class": "theme-number"}
            )  # 總集數

            # =====================================================================
            # ---------------------------------------------------------------------
            # 跑每一頁的動畫-->所有動畫的第一集 名稱 年份 網址 總觀看 集數  "抓要的值"
            for i in range(len(all_anime_url)):
                all_anime_url2 = re.findall(
                    '(?<=href=").+?(?=">)', str(all_anime_url[i])
                )  # 網址
                # print(all_anime_url2)
                all_anime_name2 = re.findall(
                    '(?<=class="theme-name">).+?(?=</)', str(all_anime_name[i])
                )  # 影片名稱
                # print(all_anime_name2)
                all_anime_date2 = re.findall(
                    "(?<=年份：).+?(?=</)", str(all_anime_date[i])
                )  # 年份
                # print(all_anime_date2)
                all_anime_seesum2 = re.findall(
                    "(?<=p>).+?(?=</p)", str(all_anime_seesum[i])
                )  # 總觀看
                # print(all_anime_seesum2)
                all_anime_listsum2 = re.findall(
                    "(?<=共).+?(?=集)", str(all_anime_listsum[i])
                )  # 總集數

                # =====================================================================
                # 觀看數字完整化
                if "萬" in all_anime_seesum2[0]:
                    view_10000 = all_anime_seesum2[0][:-1]
                    # print(view_10000)
                    view_num = str(int(float(view_10000) * 10000))
                elif all_anime_seesum2[0] == "統計中":
                    view_num = "統計中"
                else:
                    view_num = int(float(all_anime_seesum2[0]))
                # print(all_anime_seesum2[0])

                # =====================================================================
                # 網址完整化
                url_new = "https://ani.gamer.com.tw/" + str(all_anime_url2[0])
                TURL_1 = all_episode_url(url_new)[0]  # 第一集
                # print(TURL_1)
                # ---------------------------------------------------------------------
                type, who_see, img = anime_imformation(TURL_1)

                # ---------------------------------------------------------------------
                # 把資料更新置資料庫
                # sql = "INSERT INTO anime0923 (name) VALUES (%s) ON DUPLICATE KEY UPDATE (url, year, seesum, #listsum) VALUES (%s, %s, %s, %s)"  # 這樣寫會1064(42000) 少參數
                sql = "INSERT INTO anime0923 (name, url, year, seesum, listsum, type, who_see, img) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE url = VALUES(url), year = VALUES(year), seesum = VALUES(seesum), listsum = VALUES(listsum), type = VALUES(type), who_see = VALUES(who_see), img = VALUES(img)"  # 有重複名稱就UPDATE  沒有就INSERT

                val = (
                    all_anime_name2[0],
                    TURL_1,
                    all_anime_date2[0],
                    view_num,
                    all_anime_listsum2[0],
                    type,
                    who_see,
                    img,
                )

                cursor.execute(sql, val)

                # =====================================================================
        connection.commit()
    except Error as e:
        print("資料庫連接失敗：", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")

    end = time.time()
    print(end - start)


# =============================================================================
# 修改資料庫屬性================================================================
def SQL_ALTER():
    import time
    import mysql.connector
    from mysql.connector import Error

    global connection
    try:
        connection = mysql.connector.connect(
            host="localhost",  # 主機名稱
            database="anime_ver2",  # 資料庫名稱  要先在workbench那邊建立 不然會找不到
            user="root",  # 帳號
            password="root",  # 密碼
            charset="utf8mb4",
        )

        # sql = (
        #    """ALTER TABLE anime0923 MODIFY name VARCHAR(80); """  # 修改name的長度  原本設定50不夠
        # )
        sql = """ALTER TABLE anime0923 ADD (type VARCHAR(8), who_see VARCHAR(8), img VARCHAR(160)); """  # 增加欄位
        cursor = connection.cursor()
        cursor.execute(sql)  # 執行sql語句
        connection.commit()
    except Error as e:
        print("資料庫連接失敗：", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")


# =============================================================================
# 抓取簡介.哈啦板(討論區)網址.詳細資料(作品資料)網址.類型 (不會變動的)
def anime_imformation(url):
    import re
    import requests
    from bs4 import BeautifulSoup

    # 抓哈拉版網址==============================================================
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146  Safari/537.36"
    }
    webpage = requests.get(url, headers=HEADERS)
    print("anime_imformation", webpage)
    soup = BeautifulSoup(webpage.text, "html.parser")

    hala = soup.select(
        "#BH_background > div:nth-child(20) > section.data > div.data-file > div > div > div > a:nth-child(1)"
    )
    hala_url = re.findall('(?<=href=").+?(?=" target)', str(hala[0]))
    hala_url = "https:" + str(hala_url[0])
    # print(hala[0])
    print(hala_url)
    # 哈拉版網址爬'作品類型' '對象族群' '圖片?'====================================
    webpage = requests.get(hala_url, headers=HEADERS)
    print("hala_imformation", webpage)
    soup = BeautifulSoup(webpage.text, "html.parser")

    # 作品類型===================================================================
    type = soup.select(
        "#BH-master > div.BH-lbox.ACG-mster_box1.hreview-aggregate.hreview > ul.ACG-box1listA > li:nth-child(2) > a"
    )
    print(type[0])
    type = re.findall('(?<=">).+?(?=</a)', str(type[0]))
    print(type[0])
    # 對象族群===================================================================
    who_see = soup.select(
        "#BH-master > div.BH-lbox.ACG-mster_box1.hreview-aggregate.hreview > ul.ACG-box1listA > li:nth-child(4)"
    )
    print(who_see[0])
    who_see = re.findall("(?<=<li>對象族群：).+?(?=</li>)", str(who_see[0]))
    print(who_see[0])
    # image===================================================================
    img_link = soup.select("#ACG-box1pic > img")
    print(img_link[0])
    img_link = re.findall('(?<=src=").+?(?="/>)', str(img_link[0]))
    print(img_link[0])

    return type[0], who_see[0], img_link[0]


# -------------------------------------------------
# total_page()
# SQL_ALTER()
# anime_imformation("https://ani.gamer.com.tw/animeVideo.php?sn=6044")


""" 沒用到
# 4. ==========================================================================
# 抓取各集URL ==================================================================
def anime_eachurl(url):
    import re
    import requests
    from bs4 import BeautifulSoup

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146  Safari/537.36"
    }
    webpage = requests.get(url, headers=HEADERS)
    print("anime_eachurl", webpage)
    soup = BeautifulSoup(webpage.text, "html.parser")

    num_for_next = soup.select(
        "#BH_background > div.container-player > div.anime-title > div > section > ul > li > a"
    )
    # 各集URL
    # BH_background > div.container-player > div.anime-title > div.anime-option > section.season > ul > li.playing > a
    each_url = []
    for i in range(len(num_for_next)):
        net_url = re.findall('(?<=sn=).+?(?=")', str(num_for_next[i]))
        each_url.append("https://ani.gamer.com.tw/animeVideo.php?sn=" + net_url[0])
        if net_url == []:
            each_url.append(url)
    return each_url


# BH_background > div.container-player > div.anime-title > div.anime-option > div > section > ul:nth-child(2) > li.playing > a
# 5. ==========================================================================
# 抓取各集影片名 id date =======================================================
# anime_see 併入 (觀看次數那項)
def anime_eachname(url):
    import re
    import requests
    from bs4 import BeautifulSoup

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146  Safari/537.36"
    }
    # url = 'https://ani.gamer.com.tw/animeVideo.php?sn=1#goog_rewarded'
    webpage = requests.get(url, headers=HEADERS)
    print("anime_eachname", webpage)
    soup = BeautifulSoup(webpage.text, "html.parser")
    titles = soup.find_all("div", {"class": "anime_name"})

    # 觀看次數
    see_times = soup.select(
        "#BH_background > div.container-player > div.anime-title > div.anime-option > section.videoname > div.anime_name > div > span > span"
    )

    anime_num = re.findall("\[.*\]", str(titles[0].h1.text))  # 集數
    if anime_num == []:
        print("no")
        anime_num.append("[1]")

    anime_name = re.findall(".+(?= \[\d)", str(titles[0].h1.text))  # 影片名稱
    if anime_name == []:
        anime_name = re.findall(".+", str(titles[0].h1.text))

    anime_update = re.findall("(?<=上架時間：).+", str(titles[0].p.text))  # 上架時間

    each_see_times = see_times[0].text  # 觀看次數
    if "萬" in each_see_times:
        each_see_times = each_see_times[:-1]
        # print(view)
        each_see_times = str(int(float(each_see_times) * 10000))
    elif each_see_times == "統計中":
        each_see_times = "統計中"
    else:
        each_see_times = str(int(float(each_see_times)))
    return anime_name[0], anime_num[0], anime_update[0], each_see_times


# 6. ==========================================================================
# 把各集名稱,id,date跟url弄成df=================================================
# +觀看次數
def each_df(url):
    import numpy as np
    import pandas as pd

    # url = 'https://ani.gamer.com.tw/animeRef.php?sn=110699'
    anime_eachurl_list = anime_eachurl(url)
    if anime_eachurl_list == []:
        anime_eachurl_list.append(url)
    # print(anime_eachurl_list)

    anime_eachname_list = []
    anime_eachid_list = []
    anime_eachdate_list = []
    anime_eachseetime_list = []

    for i in range(len(anime_eachurl_list)):
        anime_eachname_each = anime_eachname(anime_eachurl_list[i])
        anime_eachname_list.append(anime_eachname_each[0])
        anime_eachid_list.append(anime_eachname_each[1])
        anime_eachdate_list.append(anime_eachname_each[2])
        anime_eachseetime_list.append(anime_eachname_each[3])

    # print(anime_eachname_list)

    np_anime_eachname_list = np.array(anime_eachname_list)
    np_anime_eachid_list = np.array(anime_eachid_list)
    np_anime_eachdate_list = np.array(anime_eachdate_list)
    np_anime_eachurl_list = np.array(anime_eachurl_list)
    np_anime_eachseetime_list = np.array(anime_eachseetime_list)

    df_anime_eachname_list = pd.Series(np_anime_eachname_list)
    df_anime_eachid_list = pd.Series(np_anime_eachid_list)
    df_anime_eachdate_list = pd.Series(np_anime_eachdate_list)
    df_anime_eachurl_list = pd.Series(np_anime_eachurl_list)
    df_anime_eachseetime_list = pd.Series(np_anime_eachseetime_list)

    anime_each_concat = pd.concat(
        [
            df_anime_eachname_list,
            df_anime_eachid_list,
            df_anime_eachdate_list,
            df_anime_eachurl_list,
            df_anime_eachseetime_list,
        ],
        axis=1,
        ignore_index=True,
    )
    anime_each_concat.columns = ["影片名稱", "集別", "上架時間", "影片連結", "觀看次數"]
    # anime_each_concat.to_csv("test0317_5.csv",index=False,sep=',', encoding = 'utf-8-sig')
    return anime_each_concat


# 7. ==========================================================================
# 評分 人數 (這是用第一集網頁抓)================================================
# 影片名稱這裡一起抓好了========================================================
# 要append url 因為他是key=====================================================
def anime_score_times(url):
    import re
    import requests
    from bs4 import BeautifulSoup

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146  Safari/537.36"
    }
    # url = 'https://ani.gamer.com.tw/animeVideo.php?sn='+ str(num) +'#goog_rewarded'
    webpage = requests.get(url, headers=HEADERS)
    print("anime_score_times", webpage)
    soup = BeautifulSoup(webpage.text, "html.parser")

    # 影片名稱
    titles = soup.find_all("div", {"class": "anime_name"})
    # 評分
    ACG_scores = soup.find_all("div", {"class": "ACG-score"})

    # print(titles[0].h1.text)  #舞伎家的料理人 [1]

    anime_name = re.findall(".+(?= \[\d)", str(titles[0].h1.text))  # 影片名稱
    if anime_name == []:
        anime_name = re.findall(".+", str(titles[0].h1.text))
    # all_anime_name_list.append(anime_name[0])
    # print(anime_name[0])

    scores = re.findall('(?<=class="ACG-score">).+?(?=<span>)', str(ACG_scores))  # 評分
    each_scores = scores[0]
    # print(scores[0])  #9.6
    each_ACG_scores = ACG_scores[0].span.text  # 評分人數
    # print(ACG_scores[0].span.text)  #113人
    # print(each_ACG_scores[:-1])
    return anime_name[0], each_scores, each_ACG_scores[:-1], url


# 8.==========================================================================="""
