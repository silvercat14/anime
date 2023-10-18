# -*- coding: utf-8 -*-
def read_sql(anime_name):  # 讀取資料庫
    import time
    import mysql.connector
    from mysql.connector import Error

    start = time.time()  # 測時間
    try:
        # 連接 MySQL/MariaDB 資料庫
        connection = mysql.connector.connect(
            host="localhost",  # 主機名稱
            database="anime_ver2",  # 資料庫名稱  要先在workbench那邊建立 不然會找不到
            user="root",  # 帳號
            password="root",  # 密碼
            charset="utf8mb4",
        )

        # 查詢資料庫
        cursor = connection.cursor()
        cursor.execute(
            "SELECT name, listsum, year, seesum, type, who_see, url, img FROM anime0923;"
        )
        # name, year, url, turl, seesum, avg_seesum, listsum, anime_type, anime_object, anime_supervise, anime_proxy, anime_firm, anime_score, score_people
        # 取回全部的資料
        records = cursor.fetchall()  # records[0~948][0:名稱 1:網址]
        print("資料筆數：", cursor.rowcount)
        print(records[11][0])

        import re

        # a = "A3"
        print(re.findall(anime_name, str(records[11][0])))
        for i in range(cursor.rowcount):
            if re.findall(anime_name, str(records[i][0])):
                print(records[i][0])

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


def treeviewClick(event):  # 單擊  連點兩下開啟網頁
    import webbrowser

    print("雙擊")
    for item in tree.selection():
        # global item_text
        item_text = tree.item(item, "values")
        print(item_text[6])  # 輸出所選行的第一列的值
        webbrowser.open_new(item_text[6])
        # return item_text[0]


def AnalysisClick(event):  # 右鍵  顯示圖片
    import webbrowser
    from PIL import Image, ImageTk
    from urllib.request import urlopen
    from io import BytesIO

    print("右鍵")
    for item in tree.selection():
        # global item_text
        item_text = tree.item(item, "values")
        print(item_text[7])  # 輸出所選行的第一列的值
        # webbrowser.open_new(item_text[7])
        # return item_text[0]
        # lb_text = tk.Label(
        #    fm_right_block1, text="作品圖片", fg="black", bg="#cdc9f0", font=("標楷體", 12)
        # )
        # lb_text.place(relx=0.5, rely=0.05, anchor="center")

        fm_chk_type123 = tk.Frame(
            fm_right_block1, width=170, height=240
        )  # 原本是 226, 260 約縮成0.75倍
        fm_chk_type123.place(relx=0.5, rely=0.5, anchor="center")

        URL = item_text[7]
        u = urlopen(URL)
        raw_data = u.read()
        u.close()

        im = Image.open(BytesIO(raw_data))
        # im = im.resize(113, 160)
        im = im.resize((170, 240))

        photo = ImageTk.PhotoImage(im)

        # tk_img = ImageTk.PhotoImage(raw_data)
        label_img = tk.Label(fm_chk_type123, image=photo)

        label_img.image = photo
        label_img.place(relx=0.5, rely=0.5, anchor="center")


# =============================================================================
# 點colunm排序  (數字排序)
def treeview_sort_column_int(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children("")]
    l.sort(key=lambda t: 0 if t[0] == "統計中" else int(t[0]), reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, "", index)

    # reverse sort next time
    tv.heading(col, command=lambda: treeview_sort_column_int(tv, col, not reverse))


# 點colunm排序  (文字排序)
def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children("")]
    l.sort(reverse=reverse)
    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, "", index)

    # reverse sort next time
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))


# =============================================================================


def click_func():  # checkbox 類型&對象篩選
    search_object = []
    for i in range(len(for_object)):
        if chk_object[i].get() == True:
            search_object.append(for_object[i])
            # print(i)

    if search_object == []:
        for i in range(len(for_object)):
            search_object.append(for_object[i])
    # -------------------------------------------------------------------
    search_type = []
    for i in range(len(whats_type)):
        if chk_type[i].get() == True:
            search_type.append(whats_type[i])
            # print(i)

    if search_type == []:
        for i in range(len(whats_type)):
            search_type.append(whats_type[i])
    # -------------------------------------------------------------------

    # ======================================================================================
    import time
    import mysql.connector
    from mysql.connector import Error
    import pandas as pd

    start = time.time()
    try:
        # 連接 MySQL/MariaDB 資料庫
        connection = mysql.connector.connect(
            host="localhost",  # 主機名稱
            database="anime_ver2",  # 資料庫名稱  要先在workbench那邊建立 不然會找不到
            user="root",  # 帳號
            password="root",  # 密碼
            charset="utf8mb4",
        )

        # 查詢資料庫
        cursor = connection.cursor()
        cursor.execute(
            "SELECT name, listsum, year, seesum, type, who_see, url, img FROM anime0923;"
        )

        # 取回全部的資料
        records = cursor.fetchall()
        print("資料筆數：", cursor.rowcount)

        first_filter_by_whosee = []
        for i in range(cursor.rowcount):
            print(search_object)
            if records[i][5] in search_object:
                print(records[i][5])
                first_filter_by_whosee.append(i)
        print(len(first_filter_by_whosee))
        print(first_filter_by_whosee)

        second_filter_by_type = []
        for i in first_filter_by_whosee:
            if records[i][4] in search_type:
                second_filter_by_type.append(i)
        print(len(second_filter_by_type))

        for i in tree.get_children():  # 清空viewtree
            tree.delete(i)

        for i in range(len(second_filter_by_type)):
            tree.insert("", "end", values=records[second_filter_by_type[i]])

    except Error as e:
        print("資料庫連接失敗：", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")

    end = time.time()
    print(end - start)

    global item_text
    for item in tree.selection():
        item_text = tree.item(item, "values")
    # return list_total


# ==============================================================================


def click_keyword(bh_url):  # 關鍵字搜尋
    import time
    import mysql.connector
    from mysql.connector import Error
    import pandas as pd

    start = time.time()
    try:
        # 連接 MySQL/MariaDB 資料庫
        connection = mysql.connector.connect(
            host="localhost",  # 主機名稱
            database="anime_ver2",  # 資料庫名稱  要先在workbench那邊建立 不然會找不到
            user="root",  # 帳號
            password="root",  # 密碼
            charset="utf8mb4",
        )

        # 查詢資料庫
        cursor = connection.cursor()
        cursor.execute(
            "SELECT name, listsum, year, seesum, type, who_see, url, img FROM anime0923;"
        )
        # name, year, url, turl, seesum, avg_seesum, listsum, anime_type, anime_object, anime_supervise, anime_proxy, anime_firm, anime_score, score_people
        # 取回全部的資料
        records = cursor.fetchall()  # records[0~948][0:名稱 1:網址]
        print("資料筆數：", cursor.rowcount)

        for i in tree.get_children():  # 清空viewtree
            tree.delete(i)

        import re

        # search_id = []
        for i in range(cursor.rowcount):
            find_in = re.findall(f".*{bh_url.get()}.*", records[i][0])
            if find_in != []:
                tree.insert("", "end", values=records[i])

        # list_total = len(search_id)

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

    global item_text
    for item in tree.selection():
        item_text = tree.item(item, "values")
    # return list_total


# =============================================================================
# A B C
# D E F
# =============================================================================
import tkinter as tk
from tkinter import ttk

# from tkinter import messagebox

win = tk.Tk()
win.geometry("1040x700")
win.title("巴哈姆特動畫瘋搜尋系統")
win.resizable(0, 0)
# win.configure(background="#ff0000")
# 整體==============================================================================

filemenu = tk.Menu(win)  # 功能列
win.config(menu=filemenu)
# filemenu.add_command(label="更多功能")

# chr_menu1 = tk.Menu(filemenu, tearoff=0)
# chr_menu1.add_command(label="分析")
# chr_menu1.add_command(label="關閉程式")
# filemenu.add_cascade(label="更多功能", menu=chr_menu1 )
# filemenu.config(menu=chr_menu1)

fm_left_block1 = tk.Frame(win, width=200, height=250, background="#f0bdbd")  # 紅
fm_left_block1.grid(row=0, column=0)

fm_left_block2 = tk.Frame(win, width=200, height=450, background="#ffe6ba")  # 橘
fm_left_block2.grid(row=1, column=0)

fm_big_block1 = tk.Frame(win, width=540, height=250, background="#fffdbf")  # 黃
fm_big_block1.grid(row=0, column=1)

fm_big_block2 = tk.Frame(win, width=840, height=450, background="#c9edb9")  # 綠
fm_big_block2.grid(row=1, column=1, columnspan=2)

fm_right_block1 = tk.Frame(win, width=300, height=250, background="#e0ffff")  # 藍
fm_right_block1.grid(row=0, column=2)

# fm_right_block2 = tk.Frame(win, width=200, height=450, background="#9d43d9")  # 紫
# fm_right_block2.grid(row=1, column=2)

# A ==============================================================================
lbA = tk.Label(
    fm_left_block1, text="對象群族", fg="black", bg="#cdc9f0", font=("微軟正黑體", 20)
)
lbA.place(relx=0.5, rely=0.1, anchor="center")

fm_chk_object = tk.Frame(fm_left_block1, width=640, height=120)
fm_chk_object.place(relx=0.5, rely=0.5, anchor="center")
for_object = ["少女", "少年", "淑女", "青年"]
# chk_object = [0, 0, 0, 0]
# chkValue1.set(False)
# result_obj = tk.StringVar()
chk_object = [0 for i in range(len(for_object))]
for i in range(len(for_object)):
    chk_object[i] = tk.BooleanVar()
    # chk_object.set(True)
    chk = tk.Checkbutton(
        fm_chk_object,
        text=for_object[i],
        variable=chk_object[i],
        onvalue=1,
        offvalue=0,
        bg="#f0bdbd",
        # selectcolor="black",
        font=("微軟正黑體", 15),
    ).grid(row=i, column=0, sticky="w")

# D ------------------------------------------------------------------------------
lbD = tk.Label(
    fm_left_block2, text="作品類型", fg="black", bg="#cdc9f0", font=("微軟正黑體", 20)
)
lbD.place(relx=0.5, rely=0.05, anchor="center")
fm_chk_type = tk.Frame(fm_left_block2, width=640, height=120)
fm_chk_type.place(relx=0.5, rely=0.5, anchor="center")
whats_type = [
    "青春校園",
    "靈異神怪",
    "運動競技",
    "科幻未來",
    "社會寫實",
    "溫馨",
    "歷史傳記",
    "料理美食",
    "推理懸疑",
    "戀愛",
    "幽默搞笑",
    "奇幻冒險",
    "其他",
]
chk_type = [0 for i in range(len(whats_type))]
for i in range(len(whats_type)):
    chk_type[i] = tk.BooleanVar()
    # chk_type.set(True)
    chk = tk.Checkbutton(
        fm_chk_type,
        text=whats_type[i],
        variable=chk_type[i],
        onvalue=1,
        offvalue=0,
        bg="#ffe6ba",  # 背景顏色
        # selectcolor="#ffe6ba",  #框框顏色
        # fg="#ffe6ba", #字體顏色
        # indicatorbackground="#ffe6ba",
        # indicatorforeground="white",
        font=("微軟正黑體", 10),
    ).grid(row=i, column=0, sticky="w")
# ==============================================================================
btn = tk.Button(
    fm_left_block2,
    text="條件搜尋",
    height=1,
    width=8,
    command=click_func,
    bg="#ffef85",
    fg="black",
    font=("微軟正黑體", 12),
)
btn.place(relx=0.5, rely=0.95, anchor="center")

# ==============================================================================
# lb2 = tk.Label(fm_left_block2, text="搜尋結果", fg="black", font=("標楷體", 12), bg="lightblue")
# lb2.place(relx=0.5, rely=0, anchor="center")
# listbox = tk.Listbox(fm_left_block2, width=70, height=15)
# listbox.place(relx=0.5, rely=0.55, anchor="center")
# ==============================================================================
# frame_up_left = tk.Frame(win, width=600, height=150, background="#8bb0e8")  # 淺藍
# frame_up_left.grid(row=0, column=0)

# frame_up_center = tk.Frame(win, width=200, height=150, background="#f1f0a0")
# frame_up_center.grid(row=0, column=1)

# frame_up_right = tk.Frame(win, width=200, height=150, background="#f2f0a0")
# frame_up_right.grid(row=0, column=2)

# frame_button = tk.Frame(win, width=600, height=840, background="#f2f0a0")  # 淺黃
# frame_button.grid(row=2, column=0)


# -------------------------------------------------------------------------------

# B =============================================================================
lb1 = tk.Label(
    fm_big_block1, text="請輸入影片關鍵字", fg="black", bg="#cdc9f0", font=("微軟正黑體", 20)
)
lb1.place(relx=0.5, rely=0.1, anchor="center")


# B =============================================================================
bh_url = tk.StringVar()
entry = tk.Entry(fm_big_block1, textvariable=bh_url, width=50)
entry.place(relx=0.5, rely=0.5, anchor="center")
btn = tk.Button(
    fm_big_block1,
    text="關鍵字搜尋",
    height=1,
    width=10,
    command=lambda: click_keyword(bh_url),
    bg="#ffef85",
    fg="black",
    font=("微軟正黑體", 12),
)
btn.place(relx=0.86, rely=0.5, anchor="center")


# E 下面的treeview框框 ========================================================================

# 滾動條
scrollBar = tk.Scrollbar(fm_big_block2)
scrollBar.pack(side="right", fill="y")
# Treeview元件，6列，顯示錶頭，帶垂直滾動條
tree = ttk.Treeview(
    fm_big_block2,
    height=20,
    columns=("c1", "c2", "c3", "c4", "c5", "c6", "c7"),
    show="headings",
    yscrollcommand=scrollBar.set,
)

# 設定每列寬度和對齊方式
tree.column("c1", width=280, anchor="center")
tree.column("c2", width=60, anchor="center")
tree.column("c3", width=80, anchor="center")
tree.column("c4", width=80, anchor="center")
tree.column("c5", width=100, anchor="center")
tree.column("c6", width=80, anchor="center")
tree.column("c7", width=120, anchor="center")
# 設定每列表頭標題文字
tree.heading("c1", text="影片名稱", command=lambda: treeview_sort_column(tree, "c1", False))
tree.heading(
    "c2", text="總集數", command=lambda: treeview_sort_column_int(tree, "c2", False)
)
tree.heading("c3", text="年份", command=lambda: treeview_sort_column(tree, "c3", False))
tree.heading(
    "c4", text="總觀看數", command=lambda: treeview_sort_column_int(tree, "c4", False)
)
tree.heading("c5", text="作品類型", command=lambda: treeview_sort_column(tree, "c5", False))
tree.heading("c6", text="對象族群", command=lambda: treeview_sort_column(tree, "c6", False))
tree.heading("c7", text="影片連結")

tree.bind("<Double-1>", treeviewClick)  # 連點兩下 開啟網頁
tree.bind("<3>", AnalysisClick)  # 點右鍵 顯示圖片


tree.pack(side="right", padx=10, pady=0, fill="y")
# tree.place(relx = 0.5, rely = 0.5, anchor = 'center')
# for i in range(len(row1))
scrollBar.config(command=tree.yview)

# ==============================================================================
list_total = tk.IntVar()
list_total = click_keyword(bh_url)
lb1 = tk.Label(fm_big_block2, textvariable=list_total, fg="black", font=("標楷體", 16))
lb1.place(relx=0.99, rely=1, anchor="center")


win.mainloop()

# ====測試數據時先不執行


read_sql("A3")
