# coding: UTF-8

from time import time
from pandas.io import excel
import streamlit as st
import sys
import datetime
import os
import glob
import re
import pandas as pd
import numpy as np
#import matplotlib
#matplotlib.use("Agg")
#import matplotlib.pyplot as plt
#from matplotlib.backends.backend_agg import RendererAgg
#from matplotlib.figure import Figure
#import plotly.graph_objects as go
#import plotly.express as px
#import seaborn as sns
#import statsmodels
#from statsmodels.nonparametric.smoothers_lowess import lowess

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

##_lock = RendererAgg.lock #グラフ高速化
##plt.style.use('default')
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
    selectboxplace,whitespace=st.columns((1,2))
    with selectboxplace:
        default_value=day_list_3f4_str.index(day_list_3f4_str[-1])
        selected_data=st.selectbox('表示する日付',day_list_3f4_str,index=default_value)

    for i in range(len(day_list_3f4_str)):
        if selected_data==day_list_3f4_str[i]:
            want_opdt=day_list_3f4[i]

    try:
        fuk3_4_df_want=fuk3_4_df.query("OPDT==@want_opdt")
    except:
        fuk3_4_df_want=fuk3_4_df[fuk3_4_df['OPDT']==want_opdt]
    fuk3_4_df_show=fuk3_4_df_want

    #指定日全場全レースの的中テーブル
    tableshowarea1,amari1=st.columns((1,0.01))
    print_list=["OPDT","RCOURSECD","RNO","締切時刻","勝式","投票方式","合成オッズ","合成オッズ2","該当数",\
        "組番１","組番１オッズ","組番１人気","組番２","組番２オッズ","組番２人気","組番３","組番３オッズ","組番３人気","組番４","組番４オッズ","組番４人気",\
        "返還艇","的中１","払戻金１","的中２","払戻金２","結果","払戻１","払戻２"]
    color_list=["組番１オッズ","組番１人気","組番２オッズ","組番２人気","組番３オッズ","組番３人気","組番４オッズ","組番４人気","払戻１","払戻２"]
    color_list=["11","12","14","15","17","18","20","21","28","29"]
    with tableshowarea1, _lock:
        fuk3_4_df_show=fuk3_4_df_show[print_list].copy() #SettingWithCopyWarning避け
        fuk3_4_df_show.loc[fuk3_4_df_show["組番１オッズ"]=="欠場","組番１オッズ"]=-1
        fuk3_4_df_show.loc[fuk3_4_df_show["組番２オッズ"]=="欠場","組番２オッズ"]=-1
        fuk3_4_df_show.loc[fuk3_4_df_show["組番３オッズ"]=="欠場","組番３オッズ"]=-1
        fuk3_4_df_show.loc[fuk3_4_df_show["組番４オッズ"]=="欠場","組番４オッズ"]=-1
        fuk3_4_df_show.loc[fuk3_4_df_show["的中２"]==" ","的中２"]=np.nan
        fuk3_4_df_show.loc[fuk3_4_df_show["払戻金２"]==" ","払戻金２"]=np.nan
        fuk3_4_df_show=fuk3_4_df_show.fillna(0)
        fuk3_4_df_show.loc[fuk3_4_df_show["返還艇"]==0,"返還艇"]=" "
        fuk3_4_df_show.loc[fuk3_4_df_show["結果"]==0,"結果"]=" "
        fuk3_4_df_show.loc[fuk3_4_df_show["的中２"]==0,"的中２"]=" "
        fuk3_4_df_show.loc[fuk3_4_df_show["払戻金２"]==0,"払戻金２"]=" "
        titletext="三連複４点 "+str(want_opdt)[:4]+"年"+str(int(str(want_opdt)[4:6]))+"月"+str(int(str(want_opdt)[6:]))+"日"
        st.subheader(titletext)
        has_data=len(fuk3_4_df_show)
        if has_data > 0:
            #fuk3_4_df_show.style.set_precision(0)
            fuk3_4_df_show.columns=["1","2","3","4","5","6","7","8","9","10",\
                "11","12","13","14","15","16","17","18","19","20",\
                "21","22","23","24","25","26","27","28","29"]
            # st.dataframe(fuk3_4_df_show.style.background_gradient(cmap="Blues",vmin=.0,subset=color_list)\
            #     .highlight_min(subset=color_list, color="white")\
            #     .format({"合成オッズ": lambda x: "{:.1f}".format(abs(x))})
            #     .format({"合成オッズ2": lambda x: "{:.1f}".format(abs(x))})
            #     .format({"組番１オッズ": lambda x: "{:.1f}".format(abs(x))})
            #     .format({"組番２オッズ": lambda x: "{:.1f}".format(abs(x))})
            #     .format({"組番３オッズ": lambda x: "{:.1f}".format(abs(x))})
            #     .format({"組番４オッズ": lambda x: "{:.1f}".format(abs(x))})
            #     .set_precision(0),height=500)
            st.dataframe(fuk3_4_df_show.style.background_gradient(cmap="Blues",vmin=.0,subset=color_list)\
                .highlight_min(subset=color_list, color="white")\
                .format({"7": lambda x: "{:.1f}".format(abs(x))})
                .format({"8": lambda x: "{:.1f}".format(abs(x))})
                .format({"11": lambda x: "{:.1f}".format(abs(x))})
                .format({"14": lambda x: "{:.1f}".format(abs(x))})
                .format({"17": lambda x: "{:.1f}".format(abs(x))})
                .format({"20": lambda x: "{:.1f}".format(abs(x))})
                .set_precision(0),height=500)
        else:
            st.error("指定日のデータが存在しません")
            st.stop()

    #レース時間帯別テーブル
    tableshowarea2,amari1=st.columns((1,0.01))
    pd.options.display.precision=0
    racetime_df=pd.DataFrame()
    for k in range(1,25):
        time_list=[]
        from830to900=np.nan
        from900to930=np.nan
        from930to1000=np.nan
        from1000to1030=np.nan
        from1030to1100=np.nan
        from1100to1130=np.nan
        from1130to1200=np.nan
        from1200to1230=np.nan
        from1230to1300=np.nan
        from1300to1330=np.nan
        from1330to1400=np.nan
        from1400to1430=np.nan
        from1430to1500=np.nan
        from1500to1530=np.nan
        from1530to1600=np.nan
        from1600to1630=np.nan
        from1630to1700=np.nan
        from1700to1730=np.nan
        from1730to1800=np.nan
        from1800to1830=np.nan
        from1830to1900=np.nan
        from1900to1930=np.nan
        from1930to2000=np.nan
        from2000to2030=np.nan
        from2030to2100=np.nan
        from2100to2130=np.nan
        from2130to2200=np.nan
        if k<10:
            time_list.append("0"+str(k)+"#")
        else:
            time_list.append(str(k)+"#")
        try:
            fuk3_4_df_wantrpc=fuk3_4_df_want.query("RCOURSECD==@k")
        except:
            fuk3_4_df_wantrpc=fuk3_4_df_want[fuk3_4_df_want['RCOURSECD']==k]
        if fuk3_4_df_wantrpc.empty==False:
            fuk3_4_df_wantrpc_list=fuk3_4_df_wantrpc.values.tolist()
            r1_smkr=fuk3_4_df_wantrpc_list[0][3]
            try:
                r1_smkr=int(r1_smkr)
                if r1_smkr<=1000:
                    time_list.append("A") #モーニング
                elif r1_smkr>=1700:
                    time_list.append("E") #ミッドナイト
                elif r1_smkr>=1430:
                    time_list.append("D") #ナイター
            except:
                time_list.append("Z") #判定エラー
            
            if len(time_list)<2:
                r12_smkr=fuk3_4_df_wantrpc_list[-1][3]
                try:
                    r12_smkr=int(r12_smkr)
                    if r12_smkr<=1700:
                        time_list.append("B") #デイタイム
                    else:
                        time_list.append("C") #サマー
                except:
                    time_list.append("Z") #判定エラー
                
            for l in range(len(fuk3_4_df_wantrpc_list)):
                smkr_time=fuk3_4_df_wantrpc_list[l][3]
                atari_money=fuk3_4_df_wantrpc_list[l][27]
                if np.isnan(atari_money):
                    atari_money=0.0
                else:
                    atari_money=float(atari_money)
                try:
                    smkr_time=int(smkr_time)
                    if smkr_time<900:
                        from830to900+=atari_money
                        if np.isnan(from830to900):
                            from830to900=atari_money
                    elif smkr_time<930:
                        from900to930+=atari_money
                        if np.isnan(from900to930):
                            from900to930=atari_money
                    elif smkr_time<1000:
                        from930to1000+=atari_money
                        if np.isnan(from930to1000):
                            from930to1000=atari_money
                    elif smkr_time<1030:
                        from1000to1030+=atari_money
                        if np.isnan(from1000to1030):
                            from1000to1030=atari_money
                    elif smkr_time<1100:
                        from1030to1100+=atari_money
                        if np.isnan(from1030to1100):
                            from1030to1100=atari_money
                    elif smkr_time<1130:
                        from1100to1130+=atari_money
                        if np.isnan(from1100to1130):
                            from1100to1130=atari_money
                    elif smkr_time<1200:
                        from1130to1200+=atari_money
                        if np.isnan(from1130to1200):
                            from1130to1200=atari_money
                    elif smkr_time<1230:
                        from1200to1230+=atari_money
                        if np.isnan(from1200to1230):
                            from1200to1230=atari_money
                    elif smkr_time<1300:
                        from1230to1300+=atari_money
                        if np.isnan(from1230to1300):
                            from1230to1300=atari_money
                    elif smkr_time<1330:
                        from1300to1330+=atari_money
                        if np.isnan(from1300to1330):
                            from1300to1330=atari_money
                    elif smkr_time<1400:
                        from1330to1400+=atari_money
                        if np.isnan(from1330to1400):
                            from1330to1400=atari_money
                    elif smkr_time<1430:
                        from1400to1430+=atari_money
                        if np.isnan(from1400to1430):
                            from1400to1430=atari_money
                    elif smkr_time<1500:
                        from1430to1500+=atari_money
                        if np.isnan(from1430to1500):
                            from1430to1500=atari_money
                    elif smkr_time<1530:
                        from1500to1530+=atari_money
                        if np.isnan(from1500to1530):
                            from1500to1530=atari_money
                    elif smkr_time<1600:
                        from1530to1600+=atari_money
                        if np.isnan(from1530to1600):
                            from1530to1600=atari_money
                    elif smkr_time<1630:
                        from1600to1630+=atari_money
                        if np.isnan(from1600to1630):
                            from1600to1630=atari_money
                    elif smkr_time<1700:
                        from1630to1700+=atari_money
                        if np.isnan(from1630to1700):
                            from1630to1700=atari_money
                    elif smkr_time<1730:
                        from1700to1730+=atari_money
                        if np.isnan(from1700to1730):
                            from1700to1730=atari_money
                    elif smkr_time<1800:
                        from1730to1800+=atari_money
                        if np.isnan(from1730to1800):
                            from1730to1800=atari_money
                    elif smkr_time<1830:
                        from1800to1830+=atari_money
                        if np.isnan(from1800to1830):
                            from1800to1830=atari_money
                    elif smkr_time<1900:
                        from1830to1900+=atari_money
                        if np.isnan(from1830to1900):
                            from1830to1900=atari_money
                    elif smkr_time<1930:
                        from1900to1930+=atari_money
                        if np.isnan(from1900to1930):
                            from1900to1930=atari_money
                    elif smkr_time<2000:
                        from1930to2000+=atari_money
                        if np.isnan(from1930to2000):
                            from1930to2000=atari_money
                    elif smkr_time<2030:
                        from2000to2030+=atari_money
                        if np.isnan(from2000to2030):
                            from2000to2030=atari_money
                    elif smkr_time<2100:
                        from2030to2100+=atari_money
                        if np.isnan(from2030to2100):
                            from2030to2100=atari_money
                    elif smkr_time<2130:
                        from2100to2130+=atari_money
                        if np.isnan(from2100to2130):
                            from2100to2130=atari_money
                    elif smkr_time<2200:
                        from2130to2200+=atari_money
                        if np.isnan(from2130to2200):
                            from2130to2200=atari_money
                except:
                    pass
        else:
            time_list.append(" ")
        time_list.extend([from830to900,from900to930,from930to1000,from1000to1030,from1030to1100,from1100to1130,from1130to1200,\
            from1200to1230,from1230to1300,from1300to1330,from1330to1400,from1400to1430,from1430to1500,from1500to1530,from1530to1600,\
            from1600to1630,from1630to1700,from1700to1730,from1730to1800,from1800to1830,from1830to1900,from1900to1930,from1930to2000,\
            from2000to2030,from2030to2100,from2100to2130,from2130to2200])
        for m in range(3,len(time_list)-1):
            if np.isnan(time_list[m]) and np.isnan(time_list[m-1])==False and np.isnan(time_list[m+1])==False:
                time_list[m]=0
        racetime_df=pd.concat([racetime_df,pd.DataFrame(time_list)],axis=1)
    racetime_df=racetime_df.T
    racetime_df.reset_index(drop=True,inplace=True)
    racetime_df=racetime_df.fillna(-1)
    racetime_df.columns=["場","種別","8:30~","9:00~","9:30~","10:00~","10:30~","11:00~","11:30~",\
        "12:00~","12:30~","13:00~","13:30~","14:00~","14:30~","15:00~","15:30~","16:00~","16:30~",\
        "17:00~","17:30~","18:00~","18:30~","19:00~","19:30~","20:00~","20:30~","21:00~","21:30~"]
    color_list=["8:30~","9:00~","9:30~","10:00~","10:30~","11:00~","11:30~",\
        "12:00~","12:30~","13:00~","13:30~","14:00~","14:30~","15:00~","15:30~","16:00~","16:30~",\
        "17:00~","17:30~","18:00~","18:30~","19:00~","19:30~","20:00~","20:30~","21:00~","21:30~"]
    #print(racetime_df)

    def shadow_negative(val): #-1を入れたnan列を見た目だけ非表示
        try:
            if val < 0:
                return 'color: {0}'.format('white')
            else:
                pass
        except:
            return 'color: {0}'.format('black')

    with tableshowarea2, _lock:
        titletext="レース時間帯別的中状況"
        st.subheader(titletext)
        has_data=len(racetime_df)
        if has_data > 0:
            st.dataframe(racetime_df.style.background_gradient(cmap="Blues",axis=None,)\
                .highlight_min(subset=color_list,color="white")
                .applymap(shadow_negative))
        else:
            st.error("指定日のデータが存在しません")
            st.stop()        

    #三連複４点テーブル
    
    # print_list_num=[47,48,49,50,51,52,53,54,55,56,\
    #     57,58,59,60,61,62,63,64,65,66,67,68,\
    #     69,70,71,72,73,74,75]
    # fuk3_4_df_show=fuk3_4_df_show[print_list]
    # fuk3_4_df_show=fuk3_4_df_show.fillna(" ")
    # fuk3_4_df_color=[]
    # karikari_list=[]
    # for l in range(len(print_list)):
    #     kari_list=fuk3_4_df.iloc[:,print_list_num[l]:print_list_num[l]+1].values.tolist()
    #     for la in range(len(kari_list)):
    #         karikari_list+=kari_list[la]
    #     fuk3_4_df_color.append(karikari_list)
    
    # fig=go.Figure(
    #     data=[go.Table(
    #         columnwidth=[25,30,10,20,20,30,20,20,10,\
    #             15,15,10,15,15,10,15,15,10,15,15,10,\
    #             10,15,15,15,15,15,15,15],
    #         header=dict(
    #             values=list(fuk3_4_df_show.columns),
    #             font=dict(size=12,color="white"),
    #             fill_color="#264653",
    #             line_color="rgba(255,255,255,0.2)",
    #             align=["left","center"],
    #             height=20
    #         ),
    #         cells=dict(
    #             values=[fuk3_4_df_show[K].tolist() for K in fuk3_4_df_show.columns],
    #             font=dict(size=12),
    #             fill_color=fuk3_4_df_color,
    #             align=["left","center"],
    #             line_color="rgba(255,255,255,0.2)",
    #             height=20
    #         )
    #     )]
    # )
    # if end_of_daylist_3f4==start_of_daylist_3f4:
    #     titletext="三連複４点 "+str(start_of_daylist_3f4)[:4]+"年"+str(int(str(start_of_daylist_3f4)[4:6]))+"月"+str(int(str(start_of_daylist_3f4)[6:]))+"日"
    # else:
    #     titletext="三連複４点 "+str(start_of_daylist_3f4)[:4]+"年"+str(int(str(start_of_daylist_3f4)[4:6]))+"月"+str(int(str(start_of_daylist_3f4)[6:]))+"日〜"+str(end_of_daylist_3f4)[:4]+"年"+str(int(str(end_of_daylist_3f4)[4:6]))+"月"+str(int(str(end_of_daylist_3f4)[6:]))+"日"
    # fig.update_layout(title_text=titletext,\
    #     title_font_color="#264653",\
    #     title_x=0,\
    #     margin=dict(l=0,r=10,b=10,t=30),\
    #     height=480)
        
    # tableshowarea1.plotly_chart(fig,use_container_width=True)

    #tableshowarea2,amari2=st.columns((1,0.01))

    #集計_三連複４点テーブル
    # fuk3_4_month_df_show=fuk3_4_month_df[["開催日","開催場数","レース数","総レース数","モーニング","デイ","サマー","ナイター","ミッドナイト",\
    #     "的中件数1","小計金額1","平均値1","的中件数2","小計金額2","平均値2","的中件数3","小計金額3","平均値3","的中件数4","小計金額4","平均値4",\
    #     "的中件数","的中率","日合計1","日合計2","平均値"]]
    # fuk3_4_month_df_show=fuk3_4_month_df_show.fillna(" ")
    # fig=go.Figure(
    #     data=[go.Table(
    #         columnwidth=[20,15,15,10,10,10,10,10,10,\
    #             10,10,10,10,10,10,10,10,10,10,10,10,\
    #             10,10,10,10,10],
    #         header=dict(
    #             values=list(fuk3_4_month_df_show.columns),
    #             font=dict(size=12,color="white"),
    #             fill_color="#264653",
    #             line_color="rgba(255,255,255,0.2)",
    #             align=["left","center"],
    #             height=20
    #         ),
    #         cells=dict(
    #             values=[fuk3_4_month_df_show[K].tolist() for K in fuk3_4_month_df_show.columns],
    #             font=dict(size=12),
    #             align=["left","center"],
    #             line_color="rgba(255,255,255,0.2)",
    #             height=20
    #         )
    #     )]
    # )
    # titletext="集計_三連複４点"
    # fig.update_layout(title_text=titletext,\
    #     title_font_color="#264653",\
    #     title_x=0,\
    #     margin=dict(l=0,r=10,b=10,t=30),\
    #     height=480)
            
    # tableshowarea2.plotly_chart(fig,use_container_width=True)

    #グラフ
    # g1,g2,g3=st.columns((1,1,1))

    # if fuk3_4_df_want.empty==False:
    #     race_3f4_list=fuk3_4_df_want.values.tolist()
    #     xlist=[] #場、レースごと
    #     xlist_2=[] #時間ごと
    #     ylist=[]
    #     racenum=0
    #     for rb in range(len(race_3f4_list)):
    #         racenum+=1
    #         #if int(race_3f4_list[rb][0])!=end_of_daylist_3f4:
    #         #    raise Exception("指定日以外のデータが抽出されました 抽出箇所を見直してください")
    #         atari1=race_3f4_list[rb][27]
    #         atari2=race_3f4_list[rb][28]
    #         if np.isnan(atari1)==False and atari1!="":
    #             placenum=int(race_3f4_list[rb][1])
    #             #racenum=int(race_3f4_list[rb][2])
    #             endtime=str(race_3f4_list[rb][3])
    #             racetime=datetime.datetime.strptime(endtime,"%H%M")
    #             racetime_delta=racetime-racestarttime #timedelta型
    #             racetime_delta_int=int(racetime_delta/datetime.timedelta(minutes=1))
    #             #xlist.append((placenum-1)*12+racenum) #数固定
    #             xlist.append(rb+1) #数変動
    #             xlist_2.append(racetime_delta_int)
    #             ylist.append(int(atari1))
    #         if np.isnan(atari2)==False and atari2!="":
    #             placenum=int(race_3f4_list[rb][1])
    #             #racenum=int(race_3f4_list[rb][2])
    #             endtime=str(race_3f4_list[rb][3])
    #             racetime=datetime.datetime.strptime(endtime,"%H%M")
    #             racetime_delta=racetime-racestarttime #timedelta型
    #             racetime_delta_int=int(racetime_delta/datetime.timedelta(minutes=1))
    #             #xlist.append((placenum-1)*12+racenum) #数固定
    #             xlist.append(rb+1) #数変動
    #             xlist_2.append(racetime_delta_int)
    #             ylist.append(int(atari2))
    #     if xlist!=[]:  
    #         fig=px.scatter(x=xlist,y=ylist,template="seaborn")
    #         fig.update_layout(title_text="三連複・払戻金 レース順散布図 "+str(end_of_daylist_3f4)+"<br> 的中数 "+str(len(xlist))+"/"+str(racenum)+" R 的中率"+str(round(len(xlist)/racenum*100,1))+"%",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
    #         g1.plotly_chart(fig, use_container_width=True) 
    #         fig=px.scatter(x=xlist_2,y=ylist,template="seaborn")
    #         fig.update_layout(title_text="三連複・払戻金 時間軸散布図 "+str(end_of_daylist_3f4)+"<br> 的中数 "+str(len(xlist_2))+"/"+str(racenum)+" R 的中率"+str(round(len(xlist_2)/racenum*100,1))+"%",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
    #         fig.update_layout(xaxis=dict(
    #             tickmode="array",
    #             tickvals=[0,30,60,90,120,150,180,210,240,270,300,330,360,390,420,450,480,510,540,570,600,630,660,690,720,750,780,810],
    #             ticktext=["8:30","9:00","9:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30",\
    #             "16:00","16:30","17:00","17:30","18:00","18:30","19:00","19:30","20:00","20:30","21:00","21:30","22:00"],
    #         ))
    #         g2.plotly_chart(fig, use_container_width=True) 
    # if fuk3_4_df.empty==False:
    #     fuk3_4_df=fuk3_4_df.sort_values(by=["OPDT","RCOURSECD","RNO"])
    #     race_3f4_list=fuk3_4_df.values.tolist()
    #     #xlist=[] #場、レースごと
    #     xlist_2=[] #時間ごと
    #     ylist=[]
    #     racenum=0
    #     for rb in range(len(race_3f4_list)):
    #         racenum+=1
    #         atari1=race_3f4_list[rb][27]
    #         atari2=race_3f4_list[rb][28]
    #         if np.isnan(atari1)==False and atari1!="":
    #             placenum=int(race_3f4_list[rb][1])
    #             #racenum=int(race_3f4_list[rb][2])
    #             endtime=str(race_3f4_list[rb][3])
    #             racetime=datetime.datetime.strptime(endtime,"%H%M")
    #             racetime_delta=racetime-racestarttime #timedelta型
    #             racetime_delta_int=int(racetime_delta/datetime.timedelta(minutes=1))
    #             #xlist.append((placenum-1)*12+racenum) #数固定
    #             #xlist.append(rb+1) #数変動
    #             xlist_2.append(racetime_delta_int)
    #             ylist.append(int(atari1))
    #         if np.isnan(atari2)==False and atari2!="":
    #             placenum=int(race_3f4_list[rb][1])
    #             #racenum=int(race_3f4_list[rb][2])
    #             endtime=str(race_3f4_list[rb][3])
    #             racetime=datetime.datetime.strptime(endtime,"%H%M")
    #             racetime_delta=racetime-racestarttime #timedelta型
    #             racetime_delta_int=int(racetime_delta/datetime.timedelta(minutes=1))
    #             #xlist.append((placenum-1)*12+racenum) #数固定
    #             #xlist.append(rb+1) #数変動
    #             xlist_2.append(racetime_delta_int)
    #             ylist.append(int(atari2))
    #     if xlist_2!=[]:  
    #         fig=px.scatter(x=xlist_2,y=ylist,template="seaborn")
    #         if start_of_daylist_3f4!=end_of_daylist_3f4:
    #             fig.update_layout(title_text="三連複・的中舟券 散布図 "+str(start_of_daylist_3f4)+"-"+str(end_of_daylist_3f4)+"<br> 的中数 "+str(len(xlist_2))+"/"+str(racenum)+" R 的中率"+str(round(len(xlist_2)/racenum*100,1))+"%",title_x=0,margin=dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
    #         else:
    #             fig.update_layout(title_text="三連複・的中舟券 散布図 "+str(start_of_daylist_3f4)+"<br> 的中数 "+str(len(xlist_2))+"/"+str(racenum)+" R 的中率"+str(round(len(xlist_2)/racenum*100,1))+"%",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
    #         fig.update_layout(xaxis=dict(
    #             tickmode="array",
    #             tickvals=[0,30,60,90,120,150,180,210,240,270,300,330,360,390,420,450,480,510,540,570,600,630,660,690,720,750,780,810],
    #             ticktext=["8:30","9:00","9:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00","14:30","15:00","15:30",\
    #             "16:00","16:30","17:00","17:30","18:00","18:30","19:00","19:30","20:00","20:30","21:00","21:30","22:00"],
    #         ))
    #         g3.plotly_chart(fig, use_container_width=True) 
