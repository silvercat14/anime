2021/01/04 ~ 2021/03/30 修習Python商業人才培訓計畫

前兩個月以學習 Python, MySQL為主

* key_url_all_anime.sql  更改後以url為pk的main table

* key_url_anime_list.sql  更改後以url為pk的child table

* key.py 抓取資料主程式(使用 BeautifulSoup, requests, re, numpy, pandas套件)

* GUI.py 資料庫寫入、更新、讀取，以及使用者介面顯示(使用 mysql.connector, re, numpy, pandas, tkinter, matplotlib.pyplot, matplotlib.figure, matplotlib.backends.backend_tkagg, webbrowser套件)


2021/03/02 開始建立專題架構。

2021/03/04 抓取各部影片第一集，發現影片跳轉問題。

2021/03/05 解決影片跳轉問題，成功獲得完整資料。 
設計資料庫，main table(all_anime.sql)以影片名稱為pk，child table(anime_list.sql)以影片名稱與集別為複合pk。

2021/03/08 完成資料庫更新可成功覆蓋功能。

2021/03/08 抓取各集影片相關資料(此時9000多筆)，並存入資料庫的child table。

2021/03/09 摸索自動化爬蟲方法。(僅知識層面)

2021/03/10 嘗試於動態頁面抓取資訊失敗。

2021/03/15 開始以tkinter套件建立介面。

2021/03/16 發現有資料有誤，有同名稱影片但不同版本之情形(版本顯示位置並分名稱抓取位置)。

2021/03/17~18 計畫重新建立資料庫，更改pk，並順便將各個def統整，將py檔案只分為抓取資料用(key.py)以及更新資料庫以及介面抓取用的(GUI.py)。

2021/03/19 成功重新建立以網址為pk(main child table 都是)的資料庫，並確認匯入以及更新資料無產生問題。

2021/03/20 tk介面區塊設定，多重buttone連結資料庫。

2021/03/21 tk介面，查詢結果設定，使用viewtree套件。

2021/03/22 viewtree套件之功能延伸，點擊column sort以及按鍵事件-連結至網頁。

2021/03/23 按鍵事件-新增新視窗、觀看數圖表製作。

2021/03/26 錄製與剪輯實作影片，作為成果報告ppt素材。

2021/03/29 成果報告練習。

2021/03/30 3分鐘成果報告。

#---------------------------------------------------------------------------------------------------------

2023/09 修正資料庫無直接更新問題  
        更新資料庫(刪除無使用到資料、新增顯示圖片之圖片網址)  
        [Creat_SQL.py] [anime0923.ibd]

2023/10 更新GUI介面(優化樣式、增加顯示圖片功能)  
<br>[Replanning_GUI]
        新增優化說明檔案
        [python小作品優化說明.pdf]
