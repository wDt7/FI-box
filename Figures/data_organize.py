import re
import sys
import datetime as dt
import pandas as pd
import numpy as np
import  pymysql
from sqlalchemy import create_engine
import os
import matplotlib.pyplot as plt
plt.style.use({'figure.figsize':(10, 4)})
# plt.style.use("seaborn") 
plt.rcParams['font.family']=['STKaiti']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['axes.grid'] = False

# path = input('输入存放数据库信息的地址')
for p in sys.path:
    
    if 'wdt' in p:
        path = '/Users/wdt/db.txt'
    
    if 'Figures' in p :
        path = os.path.abspath(p +'/db.txt')


def get_db_conn(io = path):
    '''
    path:::存有数据库账号信息的txt
    '''
    
    with open(io, 'r') as f1:
        config = f1.readlines()
    for i in range(0, len(config)):
        config[i] = config[i].rstrip('\n')

    host = config[0]  
    username = config[1]  # 用户名 
    password = config[2]  # 密码
    schema = config[3]
    port = int(config[4])
    engine_txt = config[5]

    conn = pymysql.connect(	
        host = host,	
        user = username,	
        passwd = password,	
        db = schema,	
        port=port,	
        charset = 'utf8'	
    )	
    engine = create_engine(engine_txt)
    return conn, engine

def upload_data(df,name,dtypelist,method="append"):
    """输入要上传的df/表名/方法"""

    conn, engine = get_db_conn(path)

    df.to_sql(name=name,con = engine,schema='finance',\
        if_exists = method ,index=False,dtype = dtypelist)
    return 

# 设定需要上传的时间段
def get_un_upload_timerange(table_name):
    conn, engine = get_db_conn(path)

    excu="select * from "
    table_name=table_name
    dff = pd.read_sql(excu+table_name,conn)
    t=dff.sort_values("date",ascending=False).head(1)["date"].values[0]
    start_time=np.datetime_as_string(t, unit='D')
    rpt_date=dt.datetime.now().strftime('%Y-%m-%d')#设定报告期，读取报告写作日时间
    conn.close()
    return start_time,rpt_date

def get_data(table_name, start=0 ,end ='2099-05-29'):
    """获取表名"""
    conn, engine = get_db_conn(path)
    excu="select * from "
    table_name=table_name

    excu_date = " where date >= '{}' and date <= '{}';".format(start , end)
    if start == 0:
        excu_date = ''
    dff = pd.read_sql(excu+table_name+excu_date,conn)
    return dff

def get_all_table_name():
    # 获取数据库所有表名
    conn, engine = get_db_conn(path)

    cursor = conn.cursor()
    cursor.execute('select table_name from information_schema.tables where table_schema="finance" ')
    A = cursor.fetchall()
    return A

def set_data_index(df):
    df.index=df["date"]
    return df


# for table_name in refresh_table_list:
#     start_time,rpt_date=get_un_upload_timerange(table_name)
#     df=read_data_from_wind(wind_code,start_time,rpt_date)
#     upload_data(df,table_name,"append")

def daily_uplpad_table_names():
    df=get_data("resoure_table")
    daily_uplpad_table_names=df[df["daily_upload_by_wind"]==1]["table_name"].tolist()
    return daily_uplpad_table_names

def get_latest_date(table_name):
    conn, engine = get_db_conn(path)
    excu="select max(date) from "
    table_name=table_name
    return pd.read_sql(excu+table_name ,conn).iloc[-1,-1]

def get_date(dir):
    """从文件名中提取日期"""
    ### e.g.成交统计2021年5月21日.xlsx ###
    x= int(re.findall(r'\d+', dir)[0])
    y= int(re.findall(r'\d+', dir)[1])
    z= int(re.findall(r'\d+', dir)[2])
    date = dt.datetime(int(x),int(y),int(z))

    return date

def set_axes_rotation(axes,rotation = 30):
    for label in axes.get_xticklabels():
        label.set_rotation(rotation)
        label.set_horizontalalignment('center')
    return axes.get_xticklabels()

def savefig(fig, name):
    fig.savefig(name+'.jpg',dpi=300,bbox_inches='tight')
    
    
def rolling_corr(se1 , se2 , n):
    df = pd.concat([se1,se2] , axis=1).dropna()
    # 滚动相关性  
    tmp = df.rolling(n).corr()
    tmp = tmp[tmp<0.99].iloc[:,0].dropna()
    idxs=[]
    for idx in tmp.index :
        idxs.append(idx[0])
    tmp.index = idxs    
    return tmp

def color_list():
    return ["#3778bf","lightsteelblue","lightgray","peachpuff","#f0833a"]


def LLT(f, period):
    d = period; f= f.dropna()
    LLT = f[d:].tolist()[:2]
    
    alpha = 2/(d+1)
    for i in range(len(f)-2-d):
        pricet_2 = (f[i:i+d])[-1]
        pricet_1 = (f[i+1:i+1+d])[-1]
        pricet = (f[i+2:i+2+d])[-1]
        LLTt_2 = LLT[i]
        LLTt_1 = LLT[i+1]
        LLTt = (alpha-(alpha**2)/4)*pricet + (alpha**2)/2*pricet_1 - (alpha-3/4*(alpha**2))*pricet_2+ 2*(1-alpha)*LLTt_1 - ((1-alpha)**2)*LLTt_2
        LLT.append(LLTt)
        #print(i)
    LLTSeries = pd.Series(LLT[:],index = f.index[d:])

    return LLTSeries

def get_ex_days(start='1998-05-29' ,end ='2099-05-29'):
    df = get_data('gz_idx')
    
    return df.loc[(df.date >= start)&(df.date<=end),'date'].tolist()
