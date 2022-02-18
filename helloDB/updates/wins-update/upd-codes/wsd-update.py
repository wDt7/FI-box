import data_organize as do
import pandas as pd
import numpy as np
from sqlalchemy.types import String, Float, Integer,DECIMAL,VARCHAR
from sqlalchemy import DateTime
import datetime as dt

from WindPy import w

from iFinDPy import THS_iFinDLogin, THS_DS


def hs300():
    # * weekly update
    name = 'hs300Div'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df = w.wsd("000300.SH", "dividendyield2", \
        last_date, today_date, usedf=True)

    df.columns = ['股息率']
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date < today_date.date())]
    columns_type=[Float(),
                    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df, name , dtypelist

def bond_index():
    # * weekly update
    name = 'bond_idx'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df = w.wsd("CBA05821.CS,CBA05831.CS,CBA05841.CS,CBA05851.CS,CBA02711.CS,CBA02721.CS,CBA02731.CS,CBA02741.CS,CBA02751.CS,CBA05801.CS,CBA02701.CS,CBA01901.CS,CBA03801.CS", "pct_chg", last_date, today_date, "",usedf=True)
    if df.shape[1] == 1:
        return [],name,[]
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date < today_date.date())]
    columns_type = [Float(),Float(),Float(),Float(), Float(),Float(),
            Float(),Float(),Float(),Float(), Float(),Float(),Float(),          
                    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    # do.upload_data(df,name,dtypelist)
    return df , name , dtypelist
    
def bond_dura():
    # * weekly update
    name = 'bond_dura'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df = w.wsd("CBA05821.CS,CBA05831.CS,CBA05841.CS,CBA05851.CS,CBA02711.CS,CBA02721.CS,CBA02731.CS,CBA02741.CS,CBA02751.CS,CBA05801.CS,CBA02701.CS,CBA01901.CS,CBA03801.CS", "duration", last_date, today_date, "",usedf=True)
    if df.shape[1] == 1:
        return [],name,[]
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date < today_date.date())]
    columns_type = [Float(),Float(),Float(),Float(), Float(),Float(),
            Float(),Float(),Float(),Float(), Float(),Float(),Float(),          
                    DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    # do.upload_data(df,name,dtypelist)
    return df , name , dtypelist

def organs_nav():
    # * weekly update
    
    name = 'organs_nav'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    err,df=w.edb("M0265776,M0265774,M0265775,M0265773,M0265777",\
         last_date, today_date,usedf=True)
    if df.shape[1] == 1:
        return [],name,[]
    # df.columns = ['证券','基金','保险','商业银行','信托']
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date < today_date.date())].dropna()
    columns_type =[DECIMAL(10,4) for _ in range(df.shape[1]-1)]+[DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    return df , name , dtypelist

def fund_nav():
    # * weekly update
    
    name = 'fund_nav1'
    last_date = do.get_latest_date(name).strftime(format='%Y-%m-%d')
    today_date = dt.datetime.now().date().strftime(format='%Y-%m-%d')
    print('表{}的最近更新日期为{}'.format(name,last_date))

    nav = do.get_data(name)
    code_list = nav.columns[:-1]

    d = THS_DS(','.join(code_list),'ths_adjustment_nvg_rate_fund',\
        '','',last_date,today_date)

    df = d.data; df.index= df.time
    tmp = pd.DataFrame(index = df.time.unique(),columns = code_list)
    for c in tmp.columns:
        tmp[c] = df.loc[df.thscode==c,'ths_adjustment_nvg_rate_fund']
    tmp['date'] = tmp.index
    tmp = tmp.iloc[1:,:]
    df = tmp.loc[(tmp.date> last_date) & (tmp.date < today_date)].dropna()

    # tmp = tmp.loc[tmp.index<today_date]
    columns_type =[DECIMAL(10,6) for _ in range(df.shape[1]-1)]+[DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))

    # do.upload_data(df, name, dtypelist, 'append')
    return df , name , dtypelist



def gk_yield():
    # TODO
    zj_issue = do.get_data('zj_issue_amt')
    zj_issue.index = zj_issue.date
    gk_list = zj_issue.loc[(zj_issue.term==10)&
        (zj_issue['issuer']=='国家开发银行'),'windcode'
        ].unique().tolist()

    def namelist2str_zj(l,rtnlist=False):
        # name_list to name_string
        strr = '' ; listt = []
        for i in range(len(l)):
            name = l[i]
            if 'z' in name[:-3] or 'Z' in name[:-3] or 'H' in name[:-3]:
                continue
            strr = strr + name + ','
            listt.append(name)
        return listt if rtnlist else strr

    name = 'gk10_yield'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now().date().strftime(format='%Y-%m-%d')
    print('表{}的最近更新日期为{}'.format(name,last_date))

    _,df = w.wsd(namelist2str_zj(gk_list),\
         "ytm_b", last_date, today_date, 
         "returnType=1", usedf=True)
    df['date'] = df.index
    data = do.get_data(name); data.index = data.date

    d = data.append(df.loc[df.date>last_date])
    d.index = d.date

    d = d.loc[d.date<dt.datetime.now().date()]

    columns_type =[DECIMAL(10,6) for _ in range(d.shape[1]-1)]+[DateTime()]
    dtypelist = dict(zip(d.columns,columns_type))
    dtypelist['date'] = DateTime()

    do.upload_data(d,name,dtypelist,'replace')
    print('成功更新表',name, '至', do.get_latest_date(name))
    
def gk_index():
    # * weekly update
    # 国开财富指数 用于计算spearman rank corr
    name = 'gkIndex'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    _,df = w.wsd("CBA02511.CS,CBA02521.CS,CBA02531.CS,CBA02541.CS,CBA02551.CS,CBA02561.CS,CBA00101.CS", \
        "pct_chg", last_date, today_date, "",usedf=True)
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date < today_date.date())].dropna()
    
    columns_type =[DECIMAL(10,6) for _ in range(df.shape[1]-1)]+[DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    # do.upload_data(df,name,dtypelist,'append')
    return df, name , dtypelist

def indice():
    # Yang monthly 
    # excel热力图
    # edb
    name = 'bond_indices'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    _,df = w.edb("M0051553,M0340363,M0340367,M0265754,M0051568,M0051567,M0265766,M0265767,M0265768,M0265769",\
         last_date, today_date, usedf=True)
    df.columns=['中债总指数','1-5年政金债指数','7-10年政金债指数',\
        '中债信用总指数','中债短融总指数','中债中票总指数','中债企业债AAA指数',\
        '中债企业债AA+指数','中债企业债AA指数','中债企业债AA-指数']
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date < today_date.date())].dropna()

    columns_type =[DECIMAL(10,6) for _ in range(df.shape[1]-1)]+[DateTime()]
    dtypelist = dict(zip(df.columns,columns_type))
    # do.upload_data(df, name,dtypelist,'append')
    return df, name , dtypelist

def gz_idx():
    # gz_index 回测用
    name = 'gz_idx'
    last_date = do.get_latest_date(name)
    today_date = dt.datetime.now()
    print('表{}的最近更新日期为{}'.format(name,last_date))

    _,df = w.wsd("CBA00651.CS,CBA00621.CS", "close",
         last_date, today_date, "", usedf=True)
    df.columns =  ['gz10','gz3']
    df['date'] = df.index
    df = df.loc[(df.date > last_date) & (df.date < today_date.date())].dropna()
    cols_typ = [Float() for _ in range(df.shape[1]-1 )] + [DateTime()]
    dtypelist = dict(zip(df.columns, cols_typ))

    return df, name , dtypelist



def main():
    w.start()
    thsLogin = THS_iFinDLogin("tpy1369","510083")
    
    l = [#hs300(),
        bond_index(), bond_dura(), organs_nav(),\
        gk_index(),#fund_nav(),
        indice(), gz_idx()]
    for a,b,c in l:
        do.upload_data(a,b,c,'append')
        print('成功更新表',b, '至', do.get_latest_date(b))

    gk_yield()

if __name__ == '__main__':
    main()
