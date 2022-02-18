
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
import pymysql
from sqlalchemy.types import String, Float, Integer,VARCHAR
from sqlalchemy import DateTime
import data_organize as do

from WindPy import w



def net_bond_daily_volume():
    # 具体个券每日成交量
    print('正在更新gz_all')
    def namelist2str_gz(l):
        # name_list to name_string
        strr = ''
        for i in range(len(l)):
            name = l[i]
            if 'x' in name or 'X' in name or 'IB' not in name:
                continue
            strr = strr + name + ','
        return strr
    def namelist2str_zj(l):
        # name_list to name_string
        strr = ''
        for i in range(len(l)):
            name = l[i]
            if 'z' in name or 'Z' in name or 'H' in name:
                continue
            strr = strr + name + ','
        return strr
    def get_gz_issue():
        gz_issue = do.get_data('gz_issue_amt')
        gz_issue.index = gz_issue.date
        for j in range(gz_issue.shape[0]):
            idx = gz_issue.index[j] ; n = gz_issue.iloc[j,1] # windcode
            t = gz_issue.iloc[j,3]# term
            if ('x' in n) or ('X' in n):
                continue
            gz_issue.loc[(gz_issue.date==idx)&(gz_issue.windcode==n) \
                ,'到期日'] = idx.date() + dt.timedelta(days=365 * t)
        for j in range(gz_issue.shape[0]):
            idx = gz_issue.index[j] ; n = gz_issue.iloc[j,1] # windcode
            t = gz_issue.iloc[j,3]# term
            if 'x' not in n and 'X' not in n:
                continue
            if 'x' in n :
                idxx = n.index('x')
            else:
                idxx = n.index('X')
            main_name = n[:idxx] + n[-3:]
            gz_issue.loc[(gz_issue.date==idx)&(gz_issue.windcode==n) \
                ,'到期日'] = gz_issue.loc[(gz_issue.windcode==main_name) \
                ,'到期日'][0]
        ii=[]
        for i in range(gz_issue.shape[0]):
            if gz_issue.iloc[i,1][-3:]=='.IB':
                ii.append(i)
        gz_issue = gz_issue.iloc[ii]
        return gz_issue
    def get_zj_issue():
        zj_issue = do.get_data('zj_issue_amt')
        zj_issue.index = zj_issue.date
        for j in range(zj_issue.shape[0]):
            idx = zj_issue.index[j] ; n = zj_issue.iloc[j,1]
            t = zj_issue.iloc[j,3]
            if (('z' in n[:-3]) | ('Z' in n[:-3]) | ('H' in n[:-3])) :
                continue
            zj_issue.loc[(zj_issue.date==idx)&(zj_issue.windcode==n) \
                ,'到期日'] = idx.date() + dt.timedelta(days=365 * t)
            
        for j in range(zj_issue.shape[0]):
            idx = zj_issue.index[j] ; n = zj_issue.iloc[j,1] # windcode
            t = zj_issue.iloc[j,3] # term
            if (('z' not in n[:-3]) & ('Z' not in n[:-3])) :
                continue
            if 'z' in n :
                idxx = n.index('z')
            elif 'Z' in n:
                idxx = n.index('Z')
            elif 'H' in n:
                idxx = n.index('H')
            main_name = n[:idxx] + n[-3:]
            zj_issue.loc[(zj_issue.date==idx)&(zj_issue.windcode==n) \
                ,'到期日'] = zj_issue.loc[(zj_issue.windcode==main_name) \
                ,'到期日'][0]
        jj=[]
        for i in range(zj_issue.shape[0]):
            if zj_issue.iloc[i,1][-3:]=='.IB':
                jj.append(i)
        zj_issue = zj_issue.iloc[jj]
        return zj_issue
    gz_issue = get_gz_issue()
    zj_issue = get_zj_issue()

    gz_all = pd.read_excel('Z:\\Users\\wdt\\Desktop\\tpy\\我的工作区\\q-市场动能\\指标细节\\个券成交量\\gz_all.xlsx',index_col=0)
    last_date = dt.datetime.strptime(gz_all.columns.max(),'%Y%m%d')
    today_date = dt.datetime.now()

    # * get all-year-gz namelist
    # gz_issuee = gz_issue.loc[gz_issue.term == 30]
    gz_names = gz_issue.windcode.tolist(); gz_name_list = []
    for i in range(len(gz_names)):
        name = gz_names[i]
        if 'x' in name or 'X' in name or 'IB' not in name:
            continue
        gz_name_list.append(name)
    # * get from wind
    d = pd.DataFrame([],index = gz_name_list)
    for date in do.get_data('rates')['date']:
        if date <= last_date:
            continue
        print(date)
        names=gz_issue.loc[(gz_issue.index<=date)&(gz_issue['到期日']>date.date()),'windcode'].tolist()
        names_str = namelist2str_gz(names)

        da = date.date().strftime(format='%Y%m%d')
        err, df= w.wss(names_str, "volume",\
            "tradeDate={};cycle=D".format(int(da)),\
                usedf=True)
        df.columns=[da]
        d[da] = df
    d[gz_all.columns] = gz_all
    d.to_excel('Z:\\Users\\wdt\\Desktop\\tpy\\我的工作区\\q-市场动能\\指标细节\\个券成交量\\gz_all.xlsx')
    
    #######################
    print('正在更新zj_all')
    zj_all = pd.read_excel('Z:\\Users\\wdt\\Desktop\\tpy\\我的工作区\\q-市场动能\\指标细节\\个券成交量\\zj_all.xlsx',index_col=0)
    last_date = dt.datetime.strptime(zj_all.columns.max(),'%Y%m%d')
    today_date = dt.datetime.now()
    # * get all-year-zj namelist
    zj_names = zj_issue.windcode.tolist(); zj_name_list = []
    for i in range(len(zj_names)):
        name = zj_names[i]
        if 'Z' in name[:-3] or 'z' in name[:-3] or 'H' in name[:-3]:
            continue
        zj_name_list.append(name)
    # * get from wind
    d = pd.DataFrame([],index = zj_name_list)
    for date in do.get_data('rates')['date']:
        if date <= last_date:
            continue
        print(date)
        names=zj_issue.loc[(zj_issue.index<=date)&(zj_issue['到期日']>date.date()),'windcode'].tolist()
        names_str = namelist2str_zj(names)

        da = date.date().strftime(format='%Y%m%d')
        err, df= w.wss(names_str, "volume",\
            "tradeDate={};cycle=D".format(int(da)),\
                usedf=True)
        df.columns=[da]
        d[da] = df
    d[zj_all.columns] = zj_all
    d.to_excel('Z:\\Users\\wdt\\Desktop\\tpy\\我的工作区\\q-市场动能\\指标细节\\个券成交量\\zj_all.xlsx')


if __name__=='__main__':
    w.start()

    net_bond_daily_volume()

