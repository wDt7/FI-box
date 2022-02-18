import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
import pymysql
from sqlalchemy.types import String, Float, Integer,VARCHAR
from sqlalchemy import DateTime
from sqlalchemy import create_engine
from sqlalchemy import exc
import os
import re
import data_organize as do
from WindPy import w

def cash_cost():
    name = 'cash_cost'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err, df=w.edb('M1006336,M1006337,M1004515,M0017142,M1001795',
               last_date,today_date,usedf=True)
    if df.shape[1] == 1:
        return [],name,[]
    df.columns = ['DR001','DR007','GC007','shibor_3m','R007']
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date < today_date.date())]


    columns_type=[Float(),Float(),Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def policy_rate():
    name = 'policy_rate'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err, df=w.edb('M0041371,M0041373,M0041377,M0329656,\
            M0329543,M0329544,M0329545',
               last_date,today_date,usedf=True)
    if df.shape[1] == 1:
        return [],name,[]
    df.columns = ['逆回购利率：7天', '逆回购利率：14天', '逆回购利率：28天',\
         '逆回购利率：63天', 'MLF：3m', 'MLF：6m',
         'MLF：1y']
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date < today_date.date())]

    columns_type=[Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def repo_volume():
    name = 'repo_volume'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err, df=w.edb('M1001794,M0330244,M0330245,M0330246,\
    M0330247,M0330248,M0330249,M0330250,\
    M0330251,M0330252,M0330253,M0330254,\
        M0041739',\
       last_date,today_date.strftime("%Y-%m-%d"),usedf=True)
    
    if df.shape[1] == 1:
        return [],name,[]

    df.columns = ['加权利率:R001','成交量:R001','成交量:R007','成交量:R014',
              '成交量:R021','成交量:R1M', '成交量:R2M','成交量:R3M', 
              '成交量:R4M', '成交量:R6M', '成交量:R9M','成交量:R1Y',\
                  '成交量:银行间质押式回购']
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date < today_date.date())]

    columns_type=[Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),Float(),Float(),Float(),
                  Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name , dtypelist

def interbank_deposit():
    name = 'interbank_deposit'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df = w.edb('M1006645,M0329545', last_date,today_date,usedf=True)
    if df.shape[1] == 1:
        return [],name,[]
    df.columns = ['存单_股份行_1y', 'MLF：1y']
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date < today_date.date())]

    columns_type=[Float(),Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name , dtypelist

def monthly_fig_bond_leverage():
    name = 'fig_bond_leverage'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err, df=w.edb('M0041754,M0041746',last_date,today_date,usedf = True)
    
    if df.shape[1] == 1:
        return [],name,[]
    
    df.columns =['银行间质押式回购余额', '中债托管余额']
    # df = df.dropna(axis = 0)
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date < today_date.date())]
    columns_type=[Float(),
                  Float(),
                  DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def daily_netfinancing_amt():
    name = 'net_financing_amt'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err, df= w.wset("bondissuanceandmaturity",\
            "startdate={};enddate={};frequency=day;\
            maingrade=all;zxgrade=all;datetype=startdate;type=default;\
            bondtype=default;bondid=1000008489000000,a101020100000000,\
            a101020200000000,a101020300000000,1000011872000000,a101020400000000,\
            a101020700000000,a101020800000000,a101020b00000000,a101020500000000,\
            1000013981000000,1000002993000000,1000004571000000,1000040753000000,\
            a101020a00000000,a101020600000000,1000016455000000,a101020900000000;\
            field=startdate,netfinancingamount".format\
                ((last_date.date().strftime('%Y-%m-%d')), \
                (today_date.date().strftime('%Y-%m-%d'))),\
            usedf=True)
    if df.shape[1] == 1:
        return [],name,[]
    
    df.columns =['date', 'netfinancingamount']
    df = df.loc[(df.date > last_date) & (df.date < today_date)]
    columns_type=[
                  DateTime(),Float()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist

def monthly_sq():
    name = 'sq_dps_amt'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err, df=w.edb("M0096412,M0341750,M0096433,M0329565,M0329612,M0096484,\
            M0096505,M0096547,M0096526,M0096307,M0329591,M0340603,\
            M0340624,M0340645,M0340666,M0340687,M0340708",\
                last_date,today_date,usedf = True)
    
    if df.shape[1] == 1:
        return [],name,[]
    
    # df = df.dropna(axis = 0)
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date < today_date.date())]
    columns_type = [Float(),Float(),Float(),Float(), Float(),Float(),
                Float(),Float(),Float(),Float(), Float(),Float(), 
                Float(),Float(),Float(),Float(), Float(),        
                    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name, dtypelist


def main():
    w.start()
    l = [cash_cost(), interbank_deposit(), repo_volume(), policy_rate(),
            monthly_fig_bond_leverage() , daily_netfinancing_amt(),
            monthly_sq()]
    
    conn , engine = do.get_db_conn()
    for a,b,c in l:
        if len(np.array(a)) == 0:
            print(b , '已是最新，无需更新')
            continue
        a.to_sql(name=b,con = engine,schema='finance',if_exists = 'append',index=False,dtype=c)
        print('成功更新表',b, '至', do.get_latest_date(b))

if __name__ == '__main__':
    main()
    
