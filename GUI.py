# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 11:11:47 2021

@author: user
"""
def chr_sql(name_in_tree):
    import time
    import mysql.connector
    from mysql.connector import Error
    start = time.time()
    try:
        # 連接 MySQL/MariaDB 資料庫
        connection = mysql.connector.connect(
            host='localhost',          # 主機名稱
            database='key_url', # 資料庫名稱
            user='root',        # 帳號
            password='root')  # 密碼
    
        # 查詢資料庫
        cursor = connection.cursor()
        cursor.execute("SELECT name, listid, date, view, avgview, turl, finish_rate FROM anime_list;")
    #name, year, url, turl, seesum, avg_seesum, listsum, anime_type, anime_object, anime_supervise, anime_proxy, anime_firm, anime_score, score_people
        # 取回全部的資料
        records = cursor.fetchall()         # records[0~948][0:名稱 1:網址]
        print("資料筆數：", cursor.rowcount)
        
        import re
        import numpy as np
        import pandas as pd 
        idlist = []
        viewlist = []
        avgviewlist = []
        # finish_rate = []
        for i in range(cursor.rowcount):
            if name_in_tree == records[i][0]:
                # print(i)
                # print(type(records[i][1]))
                #(?<=href=").+?(?=">)
                id_li = re.findall('(?<=\[).+?(?=\])', str(records[i][1]))
                # print('me', id_li[0])
                idlist.append(float(id_li[0]))
                viewlist.append(int(records[i][3]))
                avgviewlist.append(int(records[i][4]))
                # finish_rate.append(float(records[i][6]))
                
                np_idlist = np.array(idlist)
                np_viewlist = np.array(viewlist)
                np_avgviewlist = np.array(avgviewlist)
                # np_finish_rate = np.array(finish_rate)

                df_idlist = pd.Series(np_idlist)
                df_viewlist = pd.Series(np_viewlist)
                df_avgviewlist = pd.Series(np_avgviewlist)
                # df_finish_rate = pd.Series(np_finish_rate)  
                
                fig1_concat = pd.concat([df_idlist, df_viewlist], axis = 1, ignore_index = True)
                fig1_concat.columns = ['集別', '觀看數']
                fig1_concat.sort_values('集別', inplace=True, ignore_index=True)
                
                fig2_concat = pd.concat([df_idlist, df_avgviewlist], axis = 1, ignore_index = True)
                fig2_concat.columns = ['集別', '日均觀看數']
                fig2_concat.sort_values('集別', inplace=True, ignore_index=True)
                
                print(fig1_concat, fig2_concat)
                
        return fig1_concat, fig2_concat
        connection.commit()

    except Error as e:
        print("資料庫連接失敗：", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")
    
    end = time.time()
    print(end - start)
# =============================================================================
chr_sql('鬼滅之刃')
# =============================================================================
import tkinter as tk
from tkinter import ttk
def createNewWin(tree):
    import matplotlib.pyplot as plt
    print ('NewWin')
    newWindow = tk.Toplevel(win)
    newWindow.geometry('960x600')
    newWindow.title('影片分析')
    newWindow.resizable(0, 0)
    
    for item in tree.selection():
        item_text = tree.item(item,"values")
        print(item_text[0])#輸出所選行的第一列的值
        A = item_text[0]
        # print(A)
        # print(type(A))
        labelExample = tk.Label(newWindow, text = item_text[0])
        labelExample.pack()
        viewlist, avgviewlist = chr_sql(A)
        # print(idlist)
        # print('c', viewlist)
        # print('a', finish_rate)
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']   #中文需要這兩行
    plt.rcParams['axes.unicode_minus'] = False
    
    # fig, ax = plt.subplots()
    # fig.subplots_adjust(hspace=0.4, wspace=0.4) #設定子圖的間隔
    # plt.subplot(2, 1, 1)
    
    fig=plt.figure(figsize=(1, 1))
    # view_plot = fig.add_subplot(111)
    # finish_plot = fig.add_subplot(212)
    ax1 = fig.add_subplot(111)
    ax2 = fig.add_subplot(222)
    fig.tight_layout()
    
    ax1.set_ylabel('觀看數',fontdict={'fontsize':24})
    ax1.set_xlabel('集別',fontdict={'fontsize':24})
    
    ax2.set_ylabel('日均觀看數',fontdict={'fontsize':24})
    ax2.set_xlabel('集別',fontdict={'fontsize':24})
    
    viewlist.plot(x = '集別', title  = '觀看數', grid = True, legend = False, kind='line', ax=ax1, subplots=True, sharex = None, sharey = None, figsize = 10, fontsize = 20)
    
    avgviewlist.plot(x = '集別', title  = '日均觀看數', grid = True, kind='line', legend = False, ax=ax2, subplots=True, sharex = None, sharey = None, fontsize = 15)

    # # ax1.set_ylim(1,10.1)  ##設定y軸範圍
  
    # ax1.plot(viewlist['集別'], viewlist['觀看數'], 's-',color = 'r', label="觀看數")
    # ax2.plot(finish_rate['集別'], finish_rate['忠實度'],'o-',color = 'g', label="忠實度")

    # plt.title("影片分析", x=0.5, y=1.03)
    # # plt.xticks(range(len(idlist)),idlist)
    # # plt.yticks(fontsize=20)
    # plt.xlabel('集別', fontsize=30, labelpad = 15)
    # # 標示y軸(labelpad代表與圖片的距離)
    # plt.ylabel("觀看數", fontsize=30, labelpad = 20)
    # # 顯示出線條標記位置
    # # plt.legend(loc = "best", fontsize=20)    #這是圖標
    # # 畫出圖片
    fig.show()
    
    canvas = FigureCanvasTkAgg(fig, master = newWindow)
    # canvas.show()
    canvas.get_tk_widget().pack(side = 'top', fill = 'both', expand=1)
    canvas._tkcanvas.pack()
    # canvas.get_tk_widget().grid(row = 1, column = 1)
    # canvas._tkcanvas.grid(row = 1, column = 1)
    #     # print(chr_sql(item_text[0]))
        # chr_sql(A)
    # buttonExample = tk.Button(newWindow, text = "New Window button", command = )

        
    # buttonExample.pack()

def treeviewClick(event):#單擊
    import webbrowser 
    print ('雙擊')
    for item in tree.selection():
        # global item_text
        item_text = tree.item(item,"values")
        print(item_text[6])#輸出所選行的第一列的值
        webbrowser.open_new(item_text[6]) 
        # return item_text[0]
    
def AnalysisClick(event):
    createNewWin(tree)
    # pass
    

# =============================================================================
#treeview_sort_column_int 點colunm排序
def treeview_sort_column_int(tv, col, reverse):

    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(key = lambda t : 0 if t[0] == '統計中' else int(t[0]), reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda: \
               treeview_sort_column_int(tv, col, not reverse))
def treeview_sort_column(tv, col, reverse):

    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)
    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda: \
               treeview_sort_column(tv, col, not reverse))
 
# =============================================================================
def click_func():      #關鍵字搜尋

    search_object = []
    for i in range(len(for_object)):
        if chk_object[i].get() == True:
            search_object.append(for_object[i])
            # print(i)
       
    if search_object == []:
        for i in range(len(for_object)):
            search_object.append(for_object[i])
    #-------------------------------------------------------------------
    search_type = []
    for i in range(len(whats_type)):
        if chk_type[i].get() == True:
            search_type.append(whats_type[i])
            # print(i)
            
    if search_type == []:
        for i in range(len(whats_type)):
            search_type.append(whats_type[i])
    #-------------------------------------------------------------------
    search_listsum = []
    import re
    for i in range(len(listsum_range)):
        a = [0, 0]
        if chk_listsum[i].get() == True:
            a = re.findall('\d+', listsum_range[i])
            # search_listsum.append(listsum_range[i])
        # print(a)
        if a[0] == str(52):
            for i in range(52, 1500):
                search_listsum.append(str(i))
        elif len(a) == 2:
            for i in range(int(a[0]) + 1, int(a[1]) + 1):
                search_listsum.append(str(i))
        elif a[0] == str(1):
            search_listsum.append(str(i))
        
    # print(search_listsum)
    
    if search_listsum == []:
        for i in range(1, 1500):
            search_listsum.append(str(i))
    #-------------------------------------------------------------------
    import re
    search_scorepeople = []
    for i in range(len(chk_scorepeople)):
        a = [0, 0]
        if chk_scorepeople[i].get() == True:
            a = re.findall('\d+', scorepeople_range[i])
        # print(a)
        if a[0] == str(5000):
            for i in range(5000, 100000):
                search_scorepeople.append(str(i))
        elif len(a) == 2:
            for i in range(int(a[0]) + 1, int(a[1]) + 1):
                search_scorepeople.append(str(i))
        elif a[0] == str(100):
            for i in range(0, 101):
                search_scorepeople.append(str(i))
        # elif:
        #     for i in range(100000):
        #         search_scorepeople.append(i)
        
    print(len(search_scorepeople))
    
    if search_scorepeople == []:
        for i in range(100000):
            search_scorepeople.append(str(i))
    
    #-------------------------------------------------------------------
    # print(search_object, search_type, search_listsum, search_scorepeople)
    
    #======================================================================================
    import time
    import mysql.connector
    from mysql.connector import Error
    import pandas as pd
    start = time.time()
    try:
        # 連接 MySQL/MariaDB 資料庫
        connection = mysql.connector.connect(
            host='localhost',          # 主機名稱
            database='key_url', # 資料庫名稱
            user='root',        # 帳號
            password='root')  # 密碼
    
        # 查詢資料庫
        cursor = connection.cursor()
        cursor.execute("SELECT name, year, turl, seesum, avg_seesum, listsum, anime_type, anime_object, anime_score, score_people FROM all_anime;")
    #name, year, url, turl, seesum, avg_seesum, listsum, anime_type, anime_object, anime_supervise, anime_proxy, anime_firm, anime_score, score_people
        # 取回全部的資料
        records = cursor.fetchall()         # records[0~948][0:名稱 1:網址]
        print("資料筆數：", cursor.rowcount)
        
        obj_id = []
        for i in range(cursor.rowcount):
            if records[i][7] in search_object:
                # print(i)
                obj_id.append(i)
        print(len(obj_id))
                
        obj_type_id = []
        for i in obj_id:
            if records[i][6] in search_type:
                obj_type_id.append(i)    
        print(len(obj_type_id))
        
        obj_type_listnum_id = []
        for i in obj_type_id:
            if records[i][5] in search_listsum:
                obj_type_listnum_id.append(i)    
        print(len(obj_type_listnum_id))
        
        obj_type_listnum_scorepeople_id = []
        for i in obj_type_listnum_id:
            if records[i][9] in search_scorepeople:
                obj_type_listnum_scorepeople_id.append(i)    
        print(len(obj_type_listnum_scorepeople_id))
        
        # list_total = len(obj_type_listnum_scorepeople_id)
        
        # return obj_type_listnum_scorepeople_id
        name_list = []
        listsum_list = []
        year_list = []
        seesum_list = []
        avg_seesum_list = []
        anime_score_list = []
        turl_list = []
        for i in obj_type_listnum_scorepeople_id:
            name_list.append(records[i][0])
            listsum_list.append(records[i][5])
            year_list.append(records[i][1])
            seesum_list.append(records[i][3])
            avg_seesum_list.append(records[i][4])
            anime_score_list.append(records[i][8])
            turl_list.append(records[i][2])
        # records[i][0], records[i][5], records[i][1], records[i][3], records[i][4], records[i][8]
        for i in tree.get_children():  #清空viewtree
            tree.delete(i) 
        chk_dic = {
            'name' : name_list, 
            'listsum' : listsum_list, 
            'year' : year_list,
            'seesum' : seesum_list,
            'avg_seesum' : avg_seesum_list, 
            'anime_score' : anime_score_list, 
            'turl' : turl_list            
            }
        chk_df = pd.DataFrame(data = chk_dic)
        # chk_df.to_string(index = False)
        # return chk_dic
        for i in range(len(obj_type_listnum_scorepeople_id)):
            tree.insert('','end', values = chk_df.values.tolist()[i])
        
        connection.commit()

    except Error as e:
        print("資料庫連接失敗：", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")
    
    end = time.time()
    print(end - start)
    
    global item_text
    for item in tree.selection():
        item_text = tree.item(item,"values")
    # return list_total    
#==============================================================================
def click_keyword(bh_url):
    import time
    import mysql.connector
    from mysql.connector import Error
    import pandas as pd
    start = time.time()
    try:
        # 連接 MySQL/MariaDB 資料庫
        connection = mysql.connector.connect(
            host='localhost',          # 主機名稱
            database='key_url', # 資料庫名稱
            user='root',        # 帳號
            password='root')  # 密碼
    
        # 查詢資料庫
        cursor = connection.cursor()
        cursor.execute("SELECT name, year, turl, seesum, avg_seesum, listsum, anime_type, anime_object, anime_score, score_people FROM all_anime;")
    #name, year, url, turl, seesum, avg_seesum, listsum, anime_type, anime_object, anime_supervise, anime_proxy, anime_firm, anime_score, score_people
        # 取回全部的資料
        records = cursor.fetchall()         # records[0~948][0:名稱 1:網址]
        print("資料筆數：", cursor.rowcount)
        
        
        for i in tree.get_children():  #清空viewtree
            tree.delete(i) 
        
        import re
        search_id = []
        for i in range(cursor.rowcount):
            find_in = re.findall(f'.*{bh_url.get()}.*', records[i][0])
            if find_in != []:
                search_id.append(i)  
                
        # list_total = len(search_id)
        
        
        name_list = []
        listsum_list = []
        year_list = []
        seesum_list = []
        avg_seesum_list = []
        anime_score_list = []
        turl_list = []
        for i in search_id:
            name_list.append(records[i][0])
            listsum_list.append(records[i][5])
            year_list.append(records[i][1])
            seesum_list.append(records[i][3])
            avg_seesum_list.append(records[i][4])
            anime_score_list.append(records[i][8])
            turl_list.append(records[i][2])
        # records[i][0], records[i][5], records[i][1], records[i][3], records[i][4], records[i][8]
        # for i in tree.get_children():  #清空viewtree
            # tree.delete(i) 
        search_dic = {
            'name' : name_list, 
            'listsum' : listsum_list, 
            'year' : year_list,
            'seesum' : seesum_list,
            'avg_seesum' : avg_seesum_list, 
            'anime_score' : anime_score_list,
            'turl' : turl_list            
            }
        search_df = pd.DataFrame(data = search_dic)
        # chk_df.to_string(index = False)
        # return chk_dic
        for i in range(len(search_id)):
            tree.insert('','end', values = search_df.values.tolist()[i])
            
        connection.commit()
    except Error as e:
        print("資料庫連接失敗：", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")
    
    end = time.time()
    print(end - start)  
        
    global item_text
    for item in tree.selection():
        item_text = tree.item(item,"values")
    # return list_total
#==============================================================================

# =============================================================================
#     
# =============================================================================
# A B C
# D E F
#=============================================================================
#==============================================================================
# import tkinter as tk
# from tkinter import ttk
# from tkinter import messagebox

win = tk.Tk()
win.geometry('1280x700')
win.title('巴哈姆特動畫瘋搜尋系統')
win.resizable(0, 0)
# 整體==============================================================================

filemenu = tk.Menu(win)
win.config(menu = filemenu)
# filemenu.add_command(label = '更多功能')
chr_menu1 = tk.Menu(filemenu, tearoff = 0)
chr_menu1.add_command(label = '分析')
chr_menu1.add_command(label = '關閉程式')
filemenu.add_cascade(label = "更多功能", menu = chr_menu1)
# filemenu.config(menu = chr_menu1)

fm_left_block1 = tk.Frame(win, width = 200, height = 250)
fm_left_block1.grid(row = 0, column = 0)

fm_left_block2 = tk.Frame(win, width = 200, height = 450)
fm_left_block2.grid(row = 1, column = 0)

fm_big_block1 = tk.Frame(win, width = 640, height = 150)
fm_big_block1.grid(row = 0, column = 1)

fm_big_block2 = tk.Frame(win, width = 640, height = 840)
fm_big_block2.grid(row = 1, column = 1)

fm_right_block1 = tk.Frame(win, width = 200, height = 250)
fm_right_block1.grid(row = 0, column = 2)

fm_right_block2 = tk.Frame(win, width = 200, height = 450)
fm_right_block2.grid(row = 1, column = 2)


# B =============================================================================
lb1 = tk.Label(fm_big_block1, text = '請輸入影片關鍵字', fg = 'black', bg = '#cdc9f0', font = ('標楷體', 16))
lb1.place(relx = 0.5, rely = 0.1, anchor = 'center')


# B =============================================================================
bh_url = tk.StringVar()
entry = tk.Entry(fm_big_block1, textvariable = bh_url, width = 50)
entry.place(relx = 0.5, rely = 0.5, anchor = 'center')
btn = tk.Button(fm_big_block1, text = '關鍵字搜尋', command = lambda : click_keyword(bh_url), bg = '#ffef85', fg = 'black', font=(12))
btn.place(relx = 0.86, rely = 0.5, anchor = 'center')
# E =============================================================================

#滾動條
scrollBar = tk.Scrollbar(fm_big_block2)
scrollBar.pack(side = 'right', fill = 'y')
#Treeview元件，6列，顯示錶頭，帶垂直滾動條
tree = ttk.Treeview(fm_big_block2, height = 16, columns=('c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7'), show="headings", yscrollcommand = scrollBar.set) 
#設定每列寬度和對齊方式
tree.column('c1', width=360, anchor='center')
tree.column('c2', width=60, anchor='center')
tree.column('c3', width=80, anchor='center')
tree.column('c4', width=80, anchor='center')
tree.column('c5', width=100, anchor='center')
tree.column('c6', width=80, anchor='center')
tree.column('c7', width=80, anchor='center')
#設定每列表頭標題文字
tree.heading('c1', text='影片名稱')
tree.heading('c2', text='總集數', command = lambda: \
                     treeview_sort_column_int(tree, 'c2', False))
tree.heading('c3', text='年份', command = lambda: \
                     treeview_sort_column(tree, 'c3', False))
tree.heading('c4', text='總觀看數', command = lambda: \
                     treeview_sort_column_int(tree, 'c4', False))
tree.heading('c5', text='平均觀看數/集', command = lambda: \
                     treeview_sort_column_int(tree, 'c5', False))
tree.heading('c6', text='觀眾評分', command = lambda: \
                     treeview_sort_column(tree, 'c6', False))
tree.heading('c7', text='影片連結')

tree.bind('<Double-1>', treeviewClick)
tree.bind('<3>', AnalysisClick)
   

tree.pack(side = 'right',padx = 10, pady = 0, fill = 'y')
# tree.place(relx = 0.5, rely = 0.5, anchor = 'center')
# for i in range(len(row1))
scrollBar.config(command=tree.yview)


# list_total = tk.IntVar()
# list_total = click_keyword(bh_url)
# lb1 = tk.Label(fm_big_block2, textvariable = list_total, fg = 'black', font = ('標楷體', 16))
# lb1.place(relx = 0.99, rely = 1, anchor = 'center')

#==============================================================================

# lb2 = tk.Label(fm_big_block2, text = '搜尋結果', fg = 'black', font = ('標楷體', 12), bg = 'lightblue')
# lb2.place(relx = 0.5, rely = 0, anchor = 'center')
# listbox = tk.Listbox(fm_big_block2, width = 70, height = 15)
# listbox.place(relx = 0.5, rely = 0.55, anchor='center')

# A ==============================================================================
lbA = tk.Label(fm_left_block1, text = '對象群族', fg = 'black', bg = '#cdc9f0', font = ('標楷體', 16))
lbA.place(relx = 0.5, rely = 0.1, anchor = 'center')

fm_chk_object = tk.Frame(fm_left_block1, width = 640, height = 120)
fm_chk_object.place(relx = 0.5, rely = 0.5, anchor = 'center')
for_object = ['少女', '少年', '淑女', '青年']
# chk_object = [0, 0, 0, 0] 
# chkValue1.set(False)
# result_obj = tk.StringVar()
chk_object = [0 for i in range(len(for_object))]
for i in range(len(for_object)):
    chk_object[i] = tk.BooleanVar() 
    # chk_object.set(True)
    chk = tk.Checkbutton(fm_chk_object, text = for_object[i], variable = chk_object[i], onvalue = 1, offvalue = 0).grid(row = i, column = 0, sticky = 'w')
# D ------------------------------------------------------------------------------
lbD = tk.Label(fm_left_block2, text = '影片類型', fg = 'black', bg = '#cdc9f0', font = ('標楷體', 16))
lbD.place(relx = 0.5, rely = 0.05, anchor = 'center')
fm_chk_type = tk.Frame(fm_left_block2, width = 640, height = 120)
fm_chk_type.place(relx = 0.5, rely = 0.5, anchor = 'center')
whats_type = ['青春校園', '靈異神怪', '運動競技', '科幻未來', '社會寫實', '溫馨', '歷史傳記', '料理美食', '推理懸疑', '戀愛', '幽默搞笑', '奇幻冒險', '其他']
chk_type = [0 for i in range(len(whats_type))]
for i in range(len(whats_type)):
    chk_type[i] = tk.BooleanVar() 
    # chk_type.set(True)
    chk = tk.Checkbutton(fm_chk_type, text = whats_type[i], variable = chk_type[i], onvalue = 1, offvalue = 0).grid(row = i, column = 0, sticky = 'w')
# C ------------------------------------------------------------------------------
lbC = tk.Label(fm_right_block1, text = '影片集數', fg = 'black', bg = '#cdc9f0', font = ('標楷體', 16))
lbC.place(relx = 0.5, rely = 0.1, anchor = 'center')
fm_chk_listsum = tk.Frame(fm_right_block1, width = 640, height = 120)
fm_chk_listsum.place(relx = 0.5, rely = 0.5, anchor = 'center')
listsum_range = ['大於52集', '26集~52(含)集', '13集~26(含)集', '1集~13(含)集', '只有1集']
chk_listsum = [0 for i in range(len(listsum_range))]
for i in range(len(listsum_range)):
    chk_listsum[i] = tk.BooleanVar() 
    # chk_listsum.set(True)
    chk = tk.Checkbutton(fm_chk_listsum, text = listsum_range[i], variable = chk_listsum[i], onvalue = 1, offvalue = 0).grid(row = i, column = 0, sticky = 'w')
# F ------------------------------------------------------------------------------  
lbF = tk.Label(fm_right_block2, text = '評分人數', fg = 'black', bg = '#cdc9f0', font = ('標楷體', 16))
lbF.place(relx = 0.5, rely = 0.05, anchor = 'center')
fm_chk_scorepeople = tk.Frame(fm_right_block2, width = 640, height = 120)
fm_chk_scorepeople.place(relx = 0.5, rely = 0.5, anchor = 'center')
scorepeople_range = ['5000人以上', '2000~5000人', '1000~2000人', '100~1000人', '100(含)人以下']
chk_scorepeople = [0 for i in range(len(scorepeople_range))]
for i in range(len(chk_scorepeople)):
    chk_scorepeople[i] = tk.BooleanVar() 
    # chk_scorepeople.set(True)
    chk = tk.Checkbutton(fm_chk_scorepeople, text = scorepeople_range[i], variable = chk_scorepeople[i], onvalue = 1, offvalue = 0).grid(row = i, column = 0, sticky = 'w')

btn = tk.Button(fm_right_block2, text = '條件搜尋', width = 15, command = click_func, bg = '#ffef85', fg = 'black', font=(12))
btn.place(relx = 0.5, rely = 0.85, anchor = 'center')
#==============================================================================



win.mainloop()



