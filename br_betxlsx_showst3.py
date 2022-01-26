# coding: UTF-8

from pandas.io import excel
import streamlit as st
import sys
import datetime
import os
import glob
import re
import pandas as pd
#import openpyxl
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

folder="csvdata"
month_regex=re.compile(r'(\d){6}')
yesterday=datetime.date.today()-datetime.timedelta(days=1)
if len(sys.argv)>1:
    order_list=sys.argv[1:]
    for aa in range(len(order_list)):
        if order_list[aa]=="help":
            print("取得したい月を入力してください 2021年9月→202109")
            print("xlsxファイルがcsvdataフォルダ以外にある場合はフォルダ名を頭に'folder='をつけて入力してください files→folder=files")
            sys.exit()
        elif order_list[aa].startswith("folder="):
            folder=order_list[aa][7:]
        else:
            want_to_get_month=order_list[aa]
            month_mo=month_regex.search(want_to_get_month)
            if month_mo==None:
                raise Exception("日付の文法エラー \n日付は 2021年9月→202109 のように入力してください")
            month_want=int(want_to_get_month[4:])
            if month_want not in [1,2,3,4,5,6,7,8,9,10,11,12]:
                raise Exception("日付の文法エラー 月の入力に誤りがあります\n日付は 2021年9月→202109 のように入力してください")
else:
    wantdata=datetime.datetime.strftime(yesterday,"%Y%m")
    want_to_get_month=wantdata
    month_want=int(wantdata[4:])
    print("csvdataフォルダの前日月のデータを参照します")
    
print("xlsxファイルを検索中……")
if folder!="":
    f=glob.glob("./"+folder+"/*.xlsx")
else:
    f=glob.glob("./*.xlsx")

file_list=[]
file_regex=re.compile(want_to_get_month+r"M\.xlsx")
for i in range(len(f)):
    file_mo=file_regex.search(f[i])
    if file_mo!=None:
        if f[i][2:].startswith("~$"): #excel開いたときの隠しファイル
            pass
        else:   
            file_list.append(f[i][2:])

if len(file_list)==0:
    raise Exception("指定年月のXLSXファイルがありませんでした")

file_M_list=[]
for j in range(len(file_list)):
    if "M" in file_list[j]:
        print(file_list[j]+"を読み込み中……")
        trioAB_df=pd.read_excel(file_list[j],sheet_name="三連単AB_M",index_col=0)
        fuk3_4_df=pd.read_excel(file_list[j],sheet_name="三連複４点_M",index_col=0)
        fuk3_8_df=pd.read_excel(file_list[j],sheet_name="三連複８点_M",index_col=0)
        try:
            trioAB_month_df=pd.read_excel(file_list[j],sheet_name="月次集計_三連単AB",index_col=0)
            fuk3_4_month_df=pd.read_excel(file_list[j],sheet_name="月次集計_三連複４点",index_col=0)
            fuk3_8_month_df=pd.read_excel(file_list[j],sheet_name="月次集計_三連複８点",index_col=0)
        except ValueError:
            raise Exception("月次集計テーブルが存在しません")
        #print(trioAB_df_sorted)
    break
trioAB_list=trioAB_df.values.tolist()
fuk3_4_list=fuk3_4_df.values.tolist()
fuk3_8_list=fuk3_8_df.values.tolist()
start_of_daylist_3tAB=int(want_to_get_month+"31")
start_of_daylist_3f4=int(want_to_get_month+"31")
start_of_daylist_3f8=int(want_to_get_month+"31")
end_of_daylist_3tAB=int(want_to_get_month+"01")
end_of_daylist_3f4=int(want_to_get_month+"01")
end_of_daylist_3f8=int(want_to_get_month+"01")
for i in range(len(trioAB_list)):
    if int(trioAB_list[i][0])>end_of_daylist_3tAB:
        end_of_daylist_3tAB=int(trioAB_list[i][0])
    if int(trioAB_list[i][0])<start_of_daylist_3tAB:
        start_of_daylist_3tAB=int(trioAB_list[i][0])
for i in range(len(fuk3_4_list)):
    if int(fuk3_4_list[i][0])>end_of_daylist_3f4:
        end_of_daylist_3f4=int(fuk3_4_list[i][0])
    if int(fuk3_4_list[i][0])<start_of_daylist_3f4:
        start_of_daylist_3f4=int(fuk3_4_list[i][0])
for i in range(len(fuk3_8_list)):
    if int(fuk3_8_list[i][0])>end_of_daylist_3f8:
        end_of_daylist_3f8=int(fuk3_8_list[i][0])
    if int(fuk3_8_list[i][0])<start_of_daylist_3f8:
        start_of_daylist_3f8=int(fuk3_8_list[i][0])

racestarttime=datetime.datetime.strptime("0830","%H%M")

#ページ名
st.set_page_config(page_title='YOKABOAT DATA',layout='wide')

#ヘッダー
t1, t2 = st.columns((0.07,1)) 
t2.title("YOKABOAT DATA")

#中身
with st.spinner('読み込み中……'):
    try:
        fuk3_4_df_want=fuk3_4_df.query("OPDT==@end_of_daylist_3f4")
    except:
        fuk3_4_df_want=fuk3_4_df[fuk3_4_df['OPDT']==end_of_daylist_3f4]
    # try:
    #     fuk3_4_month_df_want=fuk3_4_month_df.query("OPDT==@end_of_daylist_3f4")
    # except:
    #     fuk3_4_month_df_want=fuk3_4_month_df[fuk3_4_month_df['OPDT']==end_of_daylist_3f4]
    #hosp = st.selectbox('レース場を選択', hosp_df, help = '特定のレース場のみを選択します')

    #三連複４点テーブル、月次集計_三連複４点テーブル
    tableshowarea1,amari1=st.columns((1,0.01))

    #三連複４点テーブル
    fuk3_4_df_show=fuk3_4_df[["OPDT","RCOURSECD","RNO","締切時刻","勝式","投票方式","合成オッズ","合成オッズ2","該当数",\
        "組番１","組番１オッズ","組番１人気","組番２","組番２オッズ","組番２人気","組番３","組番３オッズ","組番３人気","組番４","組番４オッズ","組番４人気",\
        "返還艇","的中１","払戻金１","的中２","払戻金２","結果","払戻１","払戻２"]]
    
    fig=go.Figure(
        data=[go.Table(
            columnwidth=[25,30,10,20,20,30,20,20,10,\
                15,15,10,15,15,10,15,15,10,15,15,10,\
                10,15,15,15,15,15,15,15],
            header=dict(
                values=list(fuk3_4_df_show.columns),
                font=dict(size=12,color="white"),
                fill_color="#264653",
                line_color="rgba(255,255,255,0.2)",
                align=["left","center"],
                height=20
            ),
            cells=dict(
                values=[fuk3_4_df_show[K].tolist() for K in fuk3_4_df_show.columns],
                font=dict(size=12),
                align=["left","center"],
                line_color="rgba(255,255,255,0.2)",
                height=20
            )
        )]
    )
    if end_of_daylist_3f4==int(want_to_get_month+"01"):
        titletext="三連複４点 1日"
    else:
        titletext="三連複４点 1〜"+str(int(str(end_of_daylist_3f4)[6:]))+"日"
    fig.update_layout(title_text=titletext,\
        title_font_color="#264653",\
        title_x=0,\
        margin=dict(l=0,r=10,b=10,t=30),\
        height=480)
        
    tableshowarea1.plotly_chart(fig,use_container_width=True)

    tableshowarea2,amari2=st.columns((1,0.01))

    #月次集計_三連複４点テーブル
    fuk3_4_month_df_show=fuk3_4_month_df[["開催日","開催場数","レース数","総レース数","モーニング","デイ","サマー","ナイター","ミッドナイト",\
        "的中件数1","小計金額1","平均値1","的中件数2","小計金額2","平均値2","的中件数3","小計金額3","平均値3","的中件数4","小計金額4","平均値4",\
        "的中件数","的中率","日合計1","日合計2","平均値"]]
    #" "," "," "," "," ","的中件数","的中率","日合計1","日合計2","平均値"]]
    fig=go.Figure(
        data=[go.Table(
            columnwidth=[20,15,15,10,10,10,10,10,10,\
                10,10,10,10,10,10,10,10,10,10,10,10,\
                10,10,10,10,10],
            header=dict(
                values=list(fuk3_4_month_df_show.columns),
                font=dict(size=12,color="white"),
                fill_color="#264653",
                line_color="rgba(255,255,255,0.2)",
                align=["left","center"],
                height=20
            ),
            cells=dict(
                values=[fuk3_4_month_df_show[K].tolist() for K in fuk3_4_month_df_show.columns],
                font=dict(size=12),
                align=["left","center"],
                line_color="rgba(255,255,255,0.2)",
                height=20
            )
        )]
    )
    titletext="月次集計_三連複４点"
    fig.update_layout(title_text=titletext,\
        title_font_color="#264653",\
        title_x=0,\
        margin=dict(l=0,r=10,b=10,t=30),\
        height=480)
            
    tableshowarea2.plotly_chart(fig,use_container_width=True)

    #グラフ
    g1,g2,g3=st.columns((1,1,1))
    wantday=20211201
    # try:
    #     race_order_df=fuk3_4_df.query("OPDT==@wantday")
    # except:
    #     race_order_df=fuk3_4_df[fuk3_4_df["OPDT"]==wantday]
    # xlist=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    # ylist=race_order_df[["-2.0","2.0-2.9","3.0-3.9","4.0-4.9","5.0-5.9","6.0-6.9","7.0-7.9","8.0-8.9","9.0-9.9",\
    #     "10.0-19.9","20.0-29.9","30.0-39.9","40.0-49.9","50.0-74.9","75.0-99.9","100.0-"]].sum().tolist()
    # #print(ylist)
    # fig=px.bar(x=xlist,y=ylist,template="seaborn")
    # fig.update_traces(marker_color='#264653')
    # fig.update_layout(title_text="三連複・オッズ ヒストグラム "+str(wantday),title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
    # g1.plotly_chart(fig, use_container_width=True) 

    if fuk3_4_df_want.empty==False:
        race_3f4_list=fuk3_4_df_want.values.tolist()
        xlist=[] #場、レースごと
        xlist_2=[] #時間ごと
        ylist=[]
        racenum=0
        for rb in range(len(race_3f4_list)):
            racenum+=1
            if int(race_3f4_list[rb][0])!=end_of_daylist_3f4:
                raise Exception("指定日以外のデータが抽出されました 抽出箇所を見直してください")
            atari1=race_3f4_list[rb][27]
            atari2=race_3f4_list[rb][28]
            if np.isnan(atari1)==False and atari1!="":
                placenum=int(race_3f4_list[rb][1])
                #racenum=int(race_3f4_list[rb][2])
                endtime=str(race_3f4_list[rb][3])
                racetime=datetime.datetime.strptime(endtime,"%H%M")
                racetime_delta=racetime-racestarttime #timedelta型
                racetime_delta_int=int(racetime_delta/datetime.timedelta(minutes=1))
                #xlist.append((placenum-1)*12+racenum) #数固定
                xlist.append(rb+1) #数変動
                xlist_2.append(racetime_delta_int)
                ylist.append(int(atari1))
            if np.isnan(atari2)==False and atari2!="":
                placenum=int(race_3f4_list[rb][1])
                #racenum=int(race_3f4_list[rb][2])
                endtime=str(race_3f4_list[rb][3])
                racetime=datetime.datetime.strptime(endtime,"%H%M")
                racetime_delta=racetime-racestarttime #timedelta型
                racetime_delta_int=int(racetime_delta/datetime.timedelta(minutes=1))
                #xlist.append((placenum-1)*12+racenum) #数固定
                xlist.append(rb+1) #数変動
                xlist_2.append(racetime_delta_int)
                ylist.append(int(atari2))
        if xlist!=[]:  
            fig=px.scatter(x=xlist,y=ylist,template="seaborn")
            fig.update_layout(title_text="三連複・払戻金 レース順散布図 "+str(end_of_daylist_3f4)+"<br> 的中数 "+str(len(xlist))+"/"+str(racenum)+" R 的中率"+str(round(len(xlist)/racenum*100,1))+"%",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
            g1.plotly_chart(fig, use_container_width=True) 
            fig=px.scatter(x=xlist_2,y=ylist,template="seaborn")
            fig.update_layout(title_text="三連複・払戻金 時間軸散布図 "+str(end_of_daylist_3f4)+"<br> 的中数 "+str(len(xlist_2))+"/"+str(racenum)+" R 的中率"+str(round(len(xlist_2)/racenum*100,1))+"%",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
            fig.update_layout(xaxis=dict(
                tickmode="array",
                tickvals=[0,30,60,90,120,150,180,210,240,270,300,330,360,390,420,450,480,510,540,570,600,630,660,690,720,750,780,810],
                ticktext=["8:30","9:00","9:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30",\
                "16:00","16:30","17:00","17:30","18:00","18:30","19:00","19:30","20:00","20:30","21:00","21:30","22:00"],
            ))
            g2.plotly_chart(fig, use_container_width=True) 
    if fuk3_4_df.empty==False:
        fuk3_4_df=fuk3_4_df.sort_values(by=["OPDT","RCOURSECD","RNO"])
        race_3f4_list=fuk3_4_df.values.tolist()
        #xlist=[] #場、レースごと
        xlist_2=[] #時間ごと
        ylist=[]
        racenum=0
        for rb in range(len(race_3f4_list)):
            racenum+=1
            atari1=race_3f4_list[rb][27]
            atari2=race_3f4_list[rb][28]
            if np.isnan(atari1)==False and atari1!="":
                placenum=int(race_3f4_list[rb][1])
                #racenum=int(race_3f4_list[rb][2])
                endtime=str(race_3f4_list[rb][3])
                racetime=datetime.datetime.strptime(endtime,"%H%M")
                racetime_delta=racetime-racestarttime #timedelta型
                racetime_delta_int=int(racetime_delta/datetime.timedelta(minutes=1))
                #xlist.append((placenum-1)*12+racenum) #数固定
                #xlist.append(rb+1) #数変動
                xlist_2.append(racetime_delta_int)
                ylist.append(int(atari1))
            if np.isnan(atari2)==False and atari2!="":
                placenum=int(race_3f4_list[rb][1])
                #racenum=int(race_3f4_list[rb][2])
                endtime=str(race_3f4_list[rb][3])
                racetime=datetime.datetime.strptime(endtime,"%H%M")
                racetime_delta=racetime-racestarttime #timedelta型
                racetime_delta_int=int(racetime_delta/datetime.timedelta(minutes=1))
                #xlist.append((placenum-1)*12+racenum) #数固定
                #xlist.append(rb+1) #数変動
                xlist_2.append(racetime_delta_int)
                ylist.append(int(atari2))
        if xlist_2!=[]:  
            fig=px.scatter(x=xlist_2,y=ylist,template="seaborn")
            if start_of_daylist_3f4!=end_of_daylist_3f4:
                fig.update_layout(title_text="三連複・的中舟券 散布図 "+str(start_of_daylist_3f4)+"-"+str(end_of_daylist_3f4)+"<br> 的中数 "+str(len(xlist_2))+"/"+str(racenum)+" R 的中率"+str(round(len(xlist_2)/racenum*100,1))+"%",title_x=0,margin=dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
            else:
                fig.update_layout(title_text="三連複・的中舟券 散布図 "+str(start_of_daylist_3f4)+"<br> 的中数 "+str(len(xlist_2))+"/"+str(racenum)+" R 的中率"+str(round(len(xlist_2)/racenum*100,1))+"%",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
            fig.update_layout(xaxis=dict(
                tickmode="array",
                tickvals=[0,30,60,90,120,150,180,210,240,270,300,330,360,390,420,450,480,510,540,570,600,630,660,690,720,750,780,810],
                ticktext=["8:30","9:00","9:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30",\
                "16:00","16:30","17:00","17:30","18:00","18:30","19:00","19:30","20:00","20:30","21:00","21:30","22:00"],
            ))
            g3.plotly_chart(fig, use_container_width=True) 
            


