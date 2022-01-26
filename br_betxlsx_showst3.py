# coding: UTF-8

from select import select
from time import time
from tkinter import Widget
from turtle import width
from pandas.io import excel
import streamlit as st
import sys
import datetime
import re
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.figure import Figure
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import altair as alt
pd.set_option('display.max_columns', 50)
pd.set_option('display.max_rows', 240)
pd.options.display.precision = 0

folder="csvdata"
month_regex=re.compile(r'(\d){6}')
yesterday=datetime.date.today()-datetime.timedelta(days=1)
if len(sys.argv)>1:
    order_list=sys.argv[1:]
    for aa in range(len(order_list)):
        if order_list[aa]=="help":
            print("'BET_latest.xlsx'がcsvdataフォルダ以外にある場合はフォルダ名を頭に'folder='をつけて入力してください files→folder=files")
            sys.exit()
        elif order_list[aa].startswith("folder="):
            folder=order_list[aa][7:]
        else:
            print("'BET_latest.xlsx'がcsvdataフォルダ以外にある場合はフォルダ名を頭に'folder='をつけて入力してください files→folder=files")
            sys.exit()
else:
    print("csvdataフォルダを参照します")

racestarttime=datetime.datetime.strptime("0830","%H%M")
#wantdata=datetime.datetime.strftime(yesterday,"%Y%m")
#want_to_get_month=wantdata
#month_want=int(wantdata[4:])
print("'BET_latest.xlsx'を検索中……")
if folder!="":
    fileplace=folder+"/BET_latest.xlsx"
else:
    fileplace="BET_latest.xlsx"

_lock = RendererAgg.lock #グラフ高速化
plt.style.use('default')
#ページ名
st.set_page_config(page_title='月間データ',layout='wide')

@st.cache(allow_output_mutation=True)
def get_BET_latest_xlsx(fileplace):
    print("'BET_latest.xlsx'を読み込み中……")
    try:
        trioAB_df=pd.read_excel(fileplace,sheet_name="三連単AB",index_col=0)
        fuk3_4_df=pd.read_excel(fileplace,sheet_name="三連複４点",index_col=0)
        fuk3_8_df=pd.read_excel(fileplace,sheet_name="三連複８点",index_col=0)
    except FileNotFoundError:
        raise Exception("'BET_latest.xlsx'が存在しません")
    try:
        trioAB_month_df=pd.read_excel(fileplace,sheet_name="集計_三連単AB",index_col=0)
        fuk3_4_month_df=pd.read_excel(fileplace,sheet_name="集計_三連複４点",index_col=0)
        fuk3_8_month_df=pd.read_excel(fileplace,sheet_name="集計_三連複８点",index_col=0)
    except ValueError:
        raise Exception("集計テーブルが存在しません")
    return trioAB_df,fuk3_4_df,fuk3_8_df,trioAB_month_df,fuk3_4_month_df,fuk3_8_month_df

df_tuple=get_BET_latest_xlsx(fileplace)
trioAB_df=df_tuple[0]
fuk3_4_df=df_tuple[1]
fuk3_8_df=df_tuple[2]
trioAB_month_df=df_tuple[3]
fuk3_4_month_df=df_tuple[4]
fuk3_8_month_df=df_tuple[5]

#含まれる日付抽出
trioAB_list=trioAB_df.values.tolist()
fuk3_4_list=fuk3_4_df.values.tolist()
fuk3_8_list=fuk3_8_df.values.tolist()
start_of_daylist_3tAB=int(trioAB_list[0][0])
start_of_daylist_3f4=int(fuk3_4_list[0][0])
start_of_daylist_3f8=int(fuk3_8_list[0][0])
end_of_daylist_3tAB=int(trioAB_list[0][0])
end_of_daylist_3f4=int(fuk3_4_list[0][0])
end_of_daylist_3f8=int(fuk3_8_list[0][0])
day_list_3tAB=[]
day_list_3f4=[]
day_list_3f8=[]
for i in range(len(trioAB_list)):
    if trioAB_list[i][0] not in day_list_3tAB:
        day_list_3tAB.append(trioAB_list[i][0])
    if int(trioAB_list[i][0])>end_of_daylist_3tAB:
        end_of_daylist_3tAB=int(trioAB_list[i][0])
    if int(trioAB_list[i][0])<start_of_daylist_3tAB:
        start_of_daylist_3tAB=int(trioAB_list[i][0])
for i in range(len(fuk3_4_list)):
    if fuk3_4_list[i][0] not in day_list_3f4:
        day_list_3f4.append(fuk3_4_list[i][0])
    if int(fuk3_4_list[i][0])>end_of_daylist_3f4:
        end_of_daylist_3f4=int(fuk3_4_list[i][0])
    if int(fuk3_4_list[i][0])<start_of_daylist_3f4:
        start_of_daylist_3f4=int(fuk3_4_list[i][0])
for i in range(len(fuk3_8_list)):
    if fuk3_8_list[i][0] not in day_list_3f8:
        day_list_3f8.append(fuk3_8_list[i][0])
    if int(fuk3_8_list[i][0])>end_of_daylist_3f8:
        end_of_daylist_3f8=int(fuk3_8_list[i][0])
    if int(fuk3_8_list[i][0])<start_of_daylist_3f8:
        start_of_daylist_3f8=int(fuk3_8_list[i][0])

day_list_3tAB_str=[]
day_list_3f4_str=[]
day_list_3f8_str=[]
for j in range(len(day_list_3tAB)):
    day_list_3tAB_str.append(str(day_list_3tAB[j])[:4]+"年"+str(int(str(day_list_3tAB[j])))[4:6]+"月"+str(int(str(day_list_3tAB[j])))[6:]+"日")
for j in range(len(day_list_3f4)):
    day_list_3f4_str.append(str(day_list_3f4[j])[:4]+"年"+str(int(str(day_list_3f4[j])))[4:6]+"月"+str(int(str(day_list_3f4[j])))[6:]+"日")
for j in range(len(day_list_3f8)):
    day_list_3f8_str.append(str(day_list_3f8[j])[:4]+"年"+str(int(str(day_list_3f8[j])))[4:6]+"月"+str(int(str(day_list_3f8[j])))[6:]+"日")

#サイトの中身
with st.spinner('読み込み中……'):
    with st.expander("このページについて",expanded=False):
        st.write("説明")

    #サイドバー
    st.sidebar.title("レースデータ検索")

    default_startvalue=day_list_3f4_str.index(day_list_3f4_str[0])
    default_endvalue=day_list_3f4_str.index(day_list_3f4_str[-1])
    selected_startday=st.sidebar.selectbox("開始日",day_list_3f4_str,index=default_startvalue)
    selected_endday=st.sidebar.selectbox("終了日",day_list_3f4_str,index=default_endvalue)

    bettype=st.sidebar.radio("投票種別",("三連単","三連複"))

    selected_rpc=st.sidebar.multiselect("場コード",\
        ["01#","02#","03#","04#","05#","06#","07#","08#","09#","10#","11#","12#",\
        "13#","14#","15#","16#","17#","18#","19#","20#","21#","22#","23#","24#"],
        default=["01#","02#","03#","04#","05#","06#","07#","08#","09#","10#","11#","12#",\
        "13#","14#","15#","16#","17#","18#","19#","20#","21#","22#","23#","24#"])

    selected_starttime,selected_endtime=st.sidebar.slider(label="締切時刻",
        min_value=datetime.datetime.strptime("0830","%H%M").time(),
        max_value=datetime.datetime.strptime("2200","%H%M").time(),
        value=(datetime.datetime.strptime("0830","%H%M").time(),datetime.datetime.strptime("2200","%H%M").time()))

    with st.sidebar.expander("レース",expanded=False):
        selected_rno=st.multiselect(" ",\
            ["1R","2R","3R","4R","5R","6R","7R","8R","9R","10R","11R","12R"],
            default=["1R","2R","3R","4R","5R","6R","7R","8R","9R","10R","11R","12R"])

    want_opdt=[]
    for i in range(len(day_list_3f4_str)):
        if day_list_3f4_str[i]==selected_startday:
            startdayplace=i
            for j in range(i,len(day_list_3f4_str)):
                if day_list_3f4_str[j]==selected_endday:
                    want_opdt.append(day_list_3f4[j])
                    enddayplace=j
                    break
                else:
                    want_opdt.append(day_list_3f4[j])
    selected_rpc_int=[]
    for i in range(len(selected_rpc)):
        selected_rpc_int.append(int(selected_rpc[i][:-1]))
    selected_rno_int=[]
    for i in range(len(selected_rno)):
        selected_rno_int.append(int(selected_rno[i][:-1]))

    today=datetime.date.today()
    selected_starttime=int(datetime.datetime.strftime(datetime.datetime.combine(today,selected_starttime),"%H%M"))
    selected_endtime=int(datetime.datetime.strftime(datetime.datetime.combine(today,selected_endtime),"%H%M"))

    if "enddayplace" not in locals() or want_opdt==[]:
        st.error("日付選択が間違っています")
        st.stop()
    if selected_rpc_int==[]:
        st.error("場を1つ以上選択してください")
        st.stop()
    if selected_rno_int==[]:
        st.error("レースを1つ以上選択してください")
        st.stop()

    if bettype=="三連単":
        selected_df=trioAB_df
    elif bettype=="三連複":
        selected_df=fuk3_4_df

    try:
        selected_df=selected_df.query("OPDT in @want_opdt")
    except:
        selected_df=selected_df[selected_df["OPDT"].isin(want_opdt)]
    try:
        selected_df=selected_df.query("RCOURSECD in @selected_rpc_int")
    except:
        selected_df=selected_df[selected_df["RCOURSECD"].isin(selected_rpc_int)]
    try:
        selected_df=selected_df.query("RNO in @selected_rno_int")
    except:
        selected_df=selected_df[selected_df["RNO"].isin(selected_rno_int)]
    try:
        selected_df=selected_df.query("selected_starttime<=締切時刻<=selected_endtime")
    except:
        selected_df=selected_df[(selected_df["締切時刻"]>=selected_starttime)&(selected_df["締切時刻"]<=selected_endtime)]

    if selected_df.empty:
        st.error("該当するデータがありません")
        st.stop()

    selected_df.loc[selected_df["的中２"]==" ","的中２"]=np.nan
    selected_df.loc[selected_df["払戻金２"]==" ","払戻金２"]=np.nan
    selected_df=selected_df.fillna(0)

    racenumplace,atarinumplace,atariperplace,returnmoneyplace=st.columns((1,1,1,1))
    racenum=len(selected_df.index)
    try:
        atari_df=selected_df.query("結果==的中")
    except:
        atari_df=selected_df[selected_df["結果"]=="的中"]
    atarinum=len(atari_df.index)
    atariper=str(round(atarinum/racenum*100,1))+"％"
    returnmoney=int(selected_df["払戻１"].sum()+selected_df["払戻２"].sum())
    with racenumplace:
        st.metric(label="レース数",value=str(racenum))
    with atarinumplace:
        st.metric(label="的中数",value=str(atarinum))
    with atariperplace:
        st.metric(label="的中率",value=atariper)
    with returnmoneyplace:
        st.metric(label="払戻金額",value=str(returnmoney))

    selected_df.loc[selected_df["返還艇"]==0,"返還艇"]=" "
    selected_df.loc[selected_df["結果"]==0,"結果"]=" "
    selected_df.loc[selected_df["的中２"]==0,"的中２"]=" "
    selected_df.loc[selected_df["払戻金２"]==0,"払戻金２"]=" "
    selected_df=selected_df.astype({"的中１":str,"払戻金１":str})

    selected_df.loc[selected_df["組番１オッズ"]=="欠場","組番１オッズ"]=-1
    selected_df.loc[selected_df["組番２オッズ"]=="欠場","組番２オッズ"]=-1
    selected_df.loc[selected_df["組番３オッズ"]=="欠場","組番３オッズ"]=-1
    selected_df.loc[selected_df["組番４オッズ"]=="欠場","組番４オッズ"]=-1
    if bettype=="三連単":
        selected_df.loc[selected_df["組番５オッズ"]=="欠場","組番５オッズ"]=-1
        selected_df.loc[selected_df["組番６オッズ"]=="欠場","組番６オッズ"]=-1
        selected_df.loc[selected_df["組番７オッズ"]=="欠場","組番７オッズ"]=-1
        selected_df.loc[selected_df["組番８オッズ"]=="欠場","組番８オッズ"]=-1
        print_list=["OPDT","RCOURSECD","RNO","締切時刻","勝式","投票方式",\
            "組番１","組番１オッズ","組番１人気","組番２","組番２オッズ","組番２人気","組番３","組番３オッズ","組番３人気","組番４","組番４オッズ","組番４人気",\
            "組番５","組番５オッズ","組番５人気","組番６","組番６オッズ","組番６人気","組番７","組番７オッズ","組番７人気","組番８","組番８オッズ","組番８人気",\
            "返還艇","的中１","払戻金１","的中２","払戻金２","結果","払戻１","払戻２"]
        selected_df=selected_df[print_list]
        selected_df.rename(columns={"OPDT":"開催日","RCOURSECD":"場コード","RNO":"レース"},inplace=True)
        st.dataframe(selected_df.style\
            .set_precision(0)\
            .format({"組番１オッズ": lambda x: "{:.1f}".format(abs(x))})\
            .format({"組番２オッズ": lambda x: "{:.1f}".format(abs(x))})\
            .format({"組番３オッズ": lambda x: "{:.1f}".format(abs(x))})\
            .format({"組番４オッズ": lambda x: "{:.1f}".format(abs(x))})\
            .format({"組番５オッズ": lambda x: "{:.1f}".format(abs(x))})\
            .format({"組番６オッズ": lambda x: "{:.1f}".format(abs(x))})\
            .format({"組番７オッズ": lambda x: "{:.1f}".format(abs(x))})\
            .format({"組番８オッズ": lambda x: "{:.1f}".format(abs(x))}),height=550)
    elif bettype=="三連複":
        print_list=["OPDT","RCOURSECD","RNO","締切時刻","勝式","投票方式",\
            "組番１","組番１オッズ","組番１人気","組番２","組番２オッズ","組番２人気","組番３","組番３オッズ","組番３人気","組番４","組番４オッズ","組番４人気",\
            "返還艇","的中１","払戻金１","的中２","払戻金２","結果","払戻１","払戻２"]
        selected_df=selected_df[print_list]
        selected_df.rename(columns={"OPDT":"開催日","RCOURSECD":"場コード","RNO":"レース"},inplace=True)
        st.dataframe(selected_df.style\
            .set_precision(0)\
            .format({"組番１オッズ": lambda x: "{:.1f}".format(abs(x))})\
            .format({"組番２オッズ": lambda x: "{:.1f}".format(abs(x))})\
            .format({"組番３オッズ": lambda x: "{:.1f}".format(abs(x))})\
            .format({"組番４オッズ": lambda x: "{:.1f}".format(abs(x))}),height=550)

    # selectboxplace,selectstatusstyleplace,selectscatterstyleplace=st.columns((1,1,1))
    # with selectboxplace:
    #     default_value=day_list_3f4_str.index(day_list_3f4_str[-1])
    #     selected_data=st.selectbox('表示する日付',day_list_3f4_str,index=default_value)

    # for i in range(len(day_list_3f4_str)):
    #     if selected_data==day_list_3f4_str[i]:
    #         want_opdt=day_list_3f4[i]
    # try:
    #     fuk3_4_df_want=fuk3_4_df.query("OPDT==@want_opdt")
    # except:
    #     fuk3_4_df_want=fuk3_4_df[fuk3_4_df['OPDT']==want_opdt]
    # fuk3_4_df_show=fuk3_4_df_want
    # try:
    #     trioAB_df_want=trioAB_df.query("OPDT==@want_opdt")
    # except:
    #     trioAB_df_want=trioAB_df[trioAB_df['OPDT']==want_opdt]
    # trioAB_df_show=trioAB_df_want

    # #指定日全場全レースの的中テーブル
    # tableshowarea1,amari1=st.columns((1,0.01))
    # print_list=["OPDT","RCOURSECD","RNO","締切時刻","勝式","投票方式",\
    #     "組番１","組番１オッズ","組番１人気","組番２","組番２オッズ","組番２人気","組番３","組番３オッズ","組番３人気","組番４","組番４オッズ","組番４人気",\
    #     "返還艇","的中１","払戻金１","的中２","払戻金２","結果","払戻１","払戻２"]
    # color_list=["組番１オッズ","組番２オッズ","組番３オッズ","組番４オッズ","払戻１","払戻２"]
    # #color_list=["11","14","17","20","28","29"]
    # with tableshowarea1, _lock:
    #     fuk3_4_df_show=fuk3_4_df_show[print_list].copy() #SettingWithCopyWarning避け
    #     fuk3_4_df_show.rename(columns={"OPDT":"開催日","RCOURSECD":"場コード","RNO":"レース"},inplace=True)
    #     fuk3_4_df_show.loc[fuk3_4_df_show["組番１オッズ"]=="欠場","組番１オッズ"]=-1
    #     fuk3_4_df_show.loc[fuk3_4_df_show["組番２オッズ"]=="欠場","組番２オッズ"]=-1
    #     fuk3_4_df_show.loc[fuk3_4_df_show["組番３オッズ"]=="欠場","組番３オッズ"]=-1
    #     fuk3_4_df_show.loc[fuk3_4_df_show["組番４オッズ"]=="欠場","組番４オッズ"]=-1
    #     fuk3_4_df_show.loc[fuk3_4_df_show["的中２"]==" ","的中２"]=np.nan
    #     fuk3_4_df_show.loc[fuk3_4_df_show["払戻金２"]==" ","払戻金２"]=np.nan
    #     fuk3_4_df_show=fuk3_4_df_show.fillna(0)
    #     fuk3_4_df_show.loc[fuk3_4_df_show["返還艇"]==0,"返還艇"]=" "
    #     fuk3_4_df_show.loc[fuk3_4_df_show["結果"]==0,"結果"]=" "
    #     fuk3_4_df_show.loc[fuk3_4_df_show["的中２"]==0,"的中２"]=" "
    #     fuk3_4_df_show.loc[fuk3_4_df_show["払戻金２"]==0,"払戻金２"]=" "
    #     fuk3_4_df_show=fuk3_4_df_show.astype({"的中１":str,"払戻金１":str})
    #     titletext="三連複４点 "+str(want_opdt)[:4]+"年"+str(int(str(want_opdt)[4:6]))+"月"+str(int(str(want_opdt)[6:]))+"日"
    #     st.subheader(titletext)
    #     has_data=len(fuk3_4_df_show)
    #     if has_data > 0:
    #         # try:
    #         #     fuk3_4_df_show_withatari=fuk3_4_df_show.query("結果==的中")
    #         # except:
    #         #     fuk3_4_df_show_withatari=fuk3_4_df_show[fuk3_4_df_show["結果"]=="的中"]
    #         # try:
    #         #     fuk3_4_df_show_withoutatari=fuk3_4_df_show.query("結果<>的中")
    #         # except:
    #         #     fuk3_4_df_show_withoutatari=fuk3_4_df_show[fuk3_4_df_show["結果"]!="的中"]
    #         def highlight_atari(col): #的中だけ青背景
    #             return ['background-color: #A7F1FF' if c == '的中' else '' for c in col.values]
    #         # fuk3_4_df_show.columns=["1","2","3","4","5","6","7","8","9","10",\
    #         #     "11","12","13","14","15","16","17","18","19","20",\
    #         #     "21","22","23","24","25","26","27","28","29"]
    #         #     .set_precision(0),height=500)
    #         #fuk3_4_df_print=fuk3_4_df_show_withatari.append(fuk3_4_df_show_withoutatari)
    #         #fuk3_4_df_print=fuk3_4_df_print.sort_values(by=["RCOURSECD","RNO"])
    #         st.dataframe(fuk3_4_df_show.style.background_gradient(cmap="Blues",vmin=.0,subset=color_list)\
    #             .highlight_min(subset=color_list, color="white")\
    #             .apply(highlight_atari,subset=["結果"])\
    #             .set_precision(0)
    #             .format({"組番１オッズ": lambda x: "{:.1f}".format(abs(x))})\
    #             .format({"組番２オッズ": lambda x: "{:.1f}".format(abs(x))})\
    #             .format({"組番３オッズ": lambda x: "{:.1f}".format(abs(x))})\
    #             .format({"組番４オッズ": lambda x: "{:.1f}".format(abs(x))})\
    #             ,height=500)
    #         # st.dataframe(fuk3_4_df_show.style.background_gradient(cmap="Blues",vmin=.0,subset=color_list)\
    #         #     .highlight_min(subset=color_list, color="white")\
    #         #     .format({"7": lambda x: "{:.1f}".format(abs(x))})
    #         #     .format({"8": lambda x: "{:.1f}".format(abs(x))})
    #         #     .format({"11": lambda x: "{:.1f}".format(abs(x))})
    #         #     .format({"14": lambda x: "{:.1f}".format(abs(x))})
    #         #     .format({"17": lambda x: "{:.1f}".format(abs(x))})
    #         #     .format({"20": lambda x: "{:.1f}".format(abs(x))})
    #         #     .set_precision(0),height=500)
    #     else:
    #         st.error("指定日のデータが存在しません")
    #         st.stop()