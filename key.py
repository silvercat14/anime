# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 10:03:32 2021

@author: user
"""

# 0. 總頁數====================================================================
# =============================================================================
def lastpage_number():    #把要的資料先append進去list裡面
    from bs4 import BeautifulSoup
    import requests
    import re
    HEADERS={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146  Safari/537.36'}
    url = 'https://ani.gamer.com.tw/animeList.php?page=1&c=0&sort=1'
    webpage = requests.get(url, headers = HEADERS)
    print('lastpage_number', webpage)
    soup = BeautifulSoup(webpage.text, 'html.parser')      
           
    lastpage = soup.select('#BH_background > div.container > div.page_control > div> a')
    # print(lastpage[-1])
    lastpage_num = re.findall('(?<=">).+?(?=</a)', str(lastpage[-1])) # 總集數

    # print(lastpage_num[0])
    return lastpage_num[0]

# 1. URL轉 T-URL===============================================================
# =============================================================================
def anime_url_change(url):    
    import re
    import requests
    from bs4 import BeautifulSoup
    HEADERS={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146  Safari/537.36'}
    webpage = requests.get(url, headers = HEADERS)
    print('anime_url_change', webpage)
    soup = BeautifulSoup(webpage.text, 'html.parser')  
    num_for_next = soup.select('#BH_background > div.container-player > div.anime-title > div.anime-option > section.season > ul > li > a')
    
    return 'https://ani.gamer.com.tw/animeVideo.php?sn=' + re.findall('(?<=sn=).+?(?=")', str(num_for_next[0]))[0]  #我現在只要第一集的T-URL   
# 2. 爬動漫瘋的所有動畫的第一集==================================================
# 名稱(先不要) 年份 轉換網址 真網址 總觀看 集數===================================
# 把要的資料先append進去list裡面==================================================
def animeall(num): 
    import re
    import requests
    from bs4 import BeautifulSoup
    
    for num in range(1, int(num) + 1):
        HEADERS={
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146  Safari/537.36'}
        url = 'https://ani.gamer.com.tw/animeList.php?page='+str(num)+'&c=0&sort=1'
        webpage = requests.get(url, headers = HEADERS)
        print('animeall', webpage)
        soup = BeautifulSoup(webpage.text, 'html.parser')  
         
        all_anime = soup.select('#BH_background > div > div.animate-theme-list > div.theme-list-block')
       
        all_anime_url = all_anime[0].find_all('a',{'class':'theme-list-main'}) # 網址
        # all_anime_name = all_anime[0].find_all('div',{'class':'theme-info-block'}) # 影片名稱
        all_anime_date = all_anime[0].find_all('div',{'class':'theme-detail-info-block'}) # 年份
        all_anime_seesum = all_anime[0].find_all('div',{'class':'show-view-number'}) # 總觀看
        all_anime_listsum = all_anime[0].find_all('span',{'class':'theme-number'}) # 總集數
        
        # =====================================================================
        for i in range(len(all_anime_url)):
            all_anime_url2 = re.findall('(?<=href=").+?(?=">)', str(all_anime_url[i])) # 網址
            # all_anime_name2 = re.findall('(?<=class="theme-name">).+?(?=</)', str(all_anime_name[i])) # 影片名稱
            all_anime_date2 = re.findall('(?<=年份：).+?(?=</)', str(all_anime_date[i]))   # 年份       
            all_anime_seesum2 = re.findall('(?<=p>).+?(?=</p)', str(all_anime_seesum[i])) # 總觀看 
            all_anime_listsum2 = re.findall('(?<=第).+?(?=集)', str(all_anime_listsum[i])) # 總集數
            
            if '萬' in all_anime_seesum2[0]:
                view_10000 = all_anime_seesum2[0][:-1]
                # print(view)
                view_num = str(int(float(view_10000)*10000))
            elif all_anime_seesum2[0] == '統計中':
                view_num = '統計中'
            else:
                view_num = int(float(all_anime_seesum2[0]))
            # print(all_anime_seesum2[0])
        # =====================================================================
            all_anime_url_list.append(all_anime_url2[0])
            # all_anime_name_list.append(all_anime_name2[0])
            all_anime_date_list.append(all_anime_date2[0])
            all_anime_seesum_list.append(view_num) # 總觀看
            all_anime_listsum_list.append(all_anime_listsum2[0]) # 總集數
      
    # =========================================================================
    # 要用URL去抓TRUE-URL    
    all_anime_turl_list = []
    # print(all_anime_url_list[0])
    for i in range(len(all_anime_url_list)):
        try:
            url_new = 'https://ani.gamer.com.tw/'+all_anime_url_list[i]
            TURL_1 = anime_url_change(url_new)
            # print(TURL_1)
        except:
            TURL_1 = 'https://ani.gamer.com.tw/'+all_anime_url_list[i]
        all_anime_turl_list.append(TURL_1)
    
    #BH_background > div.container-player > div.anime-title > div.anime-option > section.season > ul > li.playing > a
    # print(all_anime_seesum.text)
    # all_anime_name = all_anime[0].find_all('div',{'class':'theme-info-block'})
    # all_anime_date = all_anime[0].find_all('div',{'class':'theme-detail-info-block'})
    

    # =============================================================================          

    return all_anime_date_list, all_anime_url_list, all_anime_turl_list, all_anime_seesum_list, all_anime_listsum_list

# (3). 由分集頁面爬取動畫名稱======================================================
# 寫好了 先不跑

# 3. 爬動漫瘋的所有動畫的第一集==================================================
# 把append完的list轉df==========================================================              
def call_animeall():
    # lastpage = 1
    lastpage = lastpage_number()
    import numpy as np
    import pandas as pd 
    global all_anime_url_list  
    all_anime_url_list = []
    global all_anime_name_list  #名稱
    all_anime_name_list = []
    global all_anime_date_list
    all_anime_date_list = []
    global all_anime_turl_list
    all_anime_turl_list = []
    global all_anime_seesum_list
    all_anime_seesum_list = []
    global all_anime_listsum_list
    all_anime_listsum_list = []
    # for i in range(1, int(lastpage)):  #總頁數
    #     animeall(i)

    all_anime_date_list, all_anime_url_list, all_anime_turl_list, all_anime_seesum_list, all_anime_listsum_list = animeall(int(lastpage)) #最後一頁
    
    # for i in range(len(all_anime_turl_list)):
    #     import re
    #     import requests
    #     from bs4 import BeautifulSoup
    #     HEADERS={
    #         'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146  Safari/537.36'}
    #     webpage = requests.get(all_anime_turl_list[i], headers = HEADERS)
    #     soup = BeautifulSoup(webpage.text, 'html.parser')  
    #     titles = soup.find_all('div',{'class':'anime_name'}) 
    #     anime_name = re.findall('.+(?= \[\d)', str(titles[0].h1.text))
    #     if anime_name == []:
    #         anime_name = re.findall('.+', str(titles[0].h1.text))
    #     all_anime_name_list.append(anime_name[0])
        # print(anime_name[0])
    # all_anime_name_list.to_csv("test0317_1.csv",index=False,sep=',', encoding = 'utf-8-sig')
    
    
    np_all_anime_url_list = np.array(all_anime_url_list)
    # np_all_anime_name_list = np.array(all_anime_name_list)
    np_all_anime_date_list = np.array(all_anime_date_list)
    np_all_anime_turl_list = np.array(all_anime_turl_list)
    np_all_anime_seesum_list = np.array(all_anime_seesum_list)
    np_all_anime_listsum_list = np.array(all_anime_listsum_list)
    
    df_all_anime_url_list = pd.Series(np_all_anime_url_list)
    # df_all_anime_name_list = pd.Series(np_all_anime_name_list)
    df_all_anime_date_list = pd.Series(np_all_anime_date_list)
    df_all_anime_turl_list = pd.Series(np_all_anime_turl_list)  
    df_all_anime_seesum_list = pd.Series(np_all_anime_seesum_list)
    df_all_anime_listsum_list = pd.Series(np_all_anime_listsum_list)   

    anime_concat = pd.concat([df_all_anime_url_list, df_all_anime_date_list, df_all_anime_turl_list, df_all_anime_seesum_list, df_all_anime_listsum_list], axis = 1, ignore_index = True)
    anime_concat.columns = ['影片連結', '年份', '真-影片連結', '總觀看', '總集數']
    # anime_concat.to_csv("test0308_6.csv",index=False,sep=',', encoding = 'utf-8-sig')
    # anime_concat2 = pd.concat([df_all_anime_name_list], axis = 1, ignore_index = True)
    # anime_concat2.columns = ['影片']
    # anime_concat2.to_csv("test0317_3.csv",index=False,sep=',', encoding = 'utf-8-sig')

    return anime_concat
    
# =============================================================================  
# import time
# start = time.time()

# call_animeall()

# end = time.time()
# print(end - start)

# 4. ==========================================================================
# 抓取各集URL ==================================================================
def anime_eachurl(url):    
    import re
    import requests
    from bs4 import BeautifulSoup
    
    HEADERS={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146  Safari/537.36'}
    webpage = requests.get(url, headers = HEADERS)
    print('anime_eachurl', webpage)
    soup = BeautifulSoup(webpage.text, 'html.parser')  

    num_for_next = soup.select('#BH_background > div.container-player > div.anime-title > div > section > ul > li > a')
    #各集URL  
    #BH_background > div.container-player > div.anime-title > div.anime-option > section.season > ul > li.playing > a
    each_url = []
    for i in range(len(num_for_next)):
        net_url = re.findall('(?<=sn=).+?(?=")', str(num_for_next[i]))
        each_url.append('https://ani.gamer.com.tw/animeVideo.php?sn=' + net_url[0])
        if net_url == []:
            each_url.append(url)
    return each_url     
#BH_background > div.container-player > div.anime-title > div.anime-option > div > section > ul:nth-child(2) > li.playing > a
# 5. ==========================================================================
# 抓取各集影片名 id date =======================================================
# anime_see 併入 (觀看次數那項)
def anime_eachname(url):    
    import re
    import requests
    from bs4 import BeautifulSoup
    
    HEADERS={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146  Safari/537.36'}
    # url = 'https://ani.gamer.com.tw/animeVideo.php?sn=1#goog_rewarded'
    webpage = requests.get(url, headers = HEADERS)
    print('anime_eachname', webpage)
    soup = BeautifulSoup(webpage.text, 'html.parser')  
    titles = soup.find_all('div',{'class':'anime_name'})  
    
    #觀看次數
    see_times = soup.select('#BH_background > div.container-player > div.anime-title > div.anime-option > section.videoname > div.anime_name > div > span > span')

    anime_num = re.findall('\[.*\]', str(titles[0].h1.text))     #集數
    if anime_num == []:
        print('no')
        anime_num.append('[1]')
    
    anime_name = re.findall('.+(?= \[\d)', str(titles[0].h1.text)) #影片名稱
    if anime_name == []:
        anime_name = re.findall('.+', str(titles[0].h1.text))
        
    anime_update = re.findall('(?<=上架時間：).+', str(titles[0].p.text))     #上架時間
    
    each_see_times = see_times[0].text  #觀看次數
    if '萬' in each_see_times:
        each_see_times = each_see_times[:-1]
        # print(view)
        each_see_times =  str(int(float(each_see_times)*10000))
    elif each_see_times == '統計中' :
        each_see_times = '統計中'
    else:
        each_see_times =  str(int(float(each_see_times)))
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

    
    anime_each_concat = pd.concat([df_anime_eachname_list, df_anime_eachid_list, df_anime_eachdate_list, df_anime_eachurl_list, df_anime_eachseetime_list], axis = 1, ignore_index = True)
    anime_each_concat.columns = ['影片名稱','集別', '上架時間', '影片連結', '觀看次數']
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
    
    HEADERS={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146  Safari/537.36'}
    # url = 'https://ani.gamer.com.tw/animeVideo.php?sn='+ str(num) +'#goog_rewarded'
    webpage = requests.get(url, headers = HEADERS)
    print('anime_score_times', webpage)
    soup = BeautifulSoup(webpage.text, 'html.parser')  
     
    #影片名稱
    titles = soup.find_all('div',{'class':'anime_name'})  
    #評分
    ACG_scores = soup.find_all('div',{'class':'ACG-score'})

    # print(titles[0].h1.text)  #舞伎家的料理人 [1]

    anime_name = re.findall('.+(?= \[\d)', str(titles[0].h1.text))    #影片名稱
    if anime_name == []:
        anime_name = re.findall('.+', str(titles[0].h1.text))
    # all_anime_name_list.append(anime_name[0])
    # print(anime_name[0])
    
    scores = re.findall('(?<=class="ACG-score">).+?(?=<span>)', str(ACG_scores))     #評分
    each_scores = scores[0]
    # print(scores[0])  #9.6
    each_ACG_scores = ACG_scores[0].span.text      #評分人數
    # print(ACG_scores[0].span.text)  #113人
    # print(each_ACG_scores[:-1])
    return anime_name[0], each_scores, each_ACG_scores[:-1], url

# 8.===========================================================================
# =============================================================================
# 抓取簡介.哈啦板(討論區)網址.詳細資料(作品資料)網址.類型 (不會變動的)
def anime_unchange(url):    
    import re
    import requests
    from bs4 import BeautifulSoup
    
    HEADERS={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146  Safari/537.36'}
    # url = 'https://ani.gamer.com.tw/animeVideo.php?sn='+ str(num) +'#goog_rewarded'
    webpage = requests.get(url, headers = HEADERS)
    print('anime_unchange', webpage)
    soup = BeautifulSoup(webpage.text, 'html.parser')  
    #簡介
    # intros = soup.find_all('div',{'class':'data_intro'})
    
    #影片類別
    types = soup.select('#BH_background > div.container-player > div.anime-title > div.anime-option > ul > li')
    # print(intros[0].p)  #作品簡介
   
    # talks = re.findall('(?<=href=").+?(?=" target)', str(intros[0]))
    # print(talks[0])    #討論區網址
    # print(talks[1])    #作品資料
    
    tp_content1 = []
    for types in types: #影片類別
        # print(types.span.text)   
        tp_content = re.findall('(?<=</span>).+?(?=</li)', str(types))
        # print(tp_content[0])   #作品類型 對象族群 導演監督 台灣代理 製作廠商
        if tp_content != []:
            tp_content1.append(tp_content[0])
        else:
            tp_content1.append('NULL')
        
    return tp_content1
 
