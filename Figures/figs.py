
import data_organize as do
import numpy as np
import pandas as pd
import matplotlib.ticker as ticker
import datetime as dt

import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.family']=['STKaiti']
plt.rcParams['axes.unicode_minus'] = False


from fig_func import credit_change
from fig_func import credit_curve
from fig_func import rate_change


#基础的图像设置：
set_style_A={'grid.linestyle': '--',
     'axes.spines.left': True,
     'axes.spines.bottom': True,
     'axes.spines.right': True,
     'axes.spines.top': True}
sns.set_style(set_style_A)

plt.rcParams['axes.grid'] = False
plt.rcParams['axes.grid.axis'] = 'x'
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['lines.linewidth'] = 2.5
plt.rcParams['lines.linestyle'] = '-'

from rate import ti
import talib as ta



def cash_fig():
    cash_amt_prc = do.get_data('cash_amt_prc'); cash_amt_prc.index=cash_amt_prc.date
    df = do.get_data('policy_rate','2018-01-01',)
    df.index = df.date
    
    plt.style.use({'font.size' : 12}) 
    fig,ax = plt.subplots(ncols=2,nrows=8,figsize=(6*2,4*8), dpi=300)
    
    # * P0,0 OMO & DR007
    df['逆回购利率：7天'].fillna(method='ffill')['2020':].plot(ax=ax[0,0])
    cash_amt_prc.R007['2020':].plot(ax=ax[0,0],color='#f0833a',lw=1)
    ax[0,0].set_ylabel('%')
    ax[0,0].legend(loc=9,frameon=False,ncol=2)
    do.set_axes_rotation(ax[0,0],)
    ax[0,0].set_title('OMO与R007')
    
    # * P0,1 MLF & 1Y-CD
    interbank_deposit = do.get_data('interbank_deposit','2020-01-01')
    interbank_deposit.index = interbank_deposit.date
    ax[0,1].plot(interbank_deposit[['存单_股份行_1y']],'#3778bf',label="1年股份行存单利率")
    # ax[0,1].scatter(interbank_deposit.index,interbank_deposit['MLF：1y'],\
    #     label='MLF利率：1年', marker='o',color = '#f0833a',s=10)
    interbank_deposit['MLF：1y'].fillna(method='ffill').\
        plot(ax = ax[0,1],ls='--',color = '#f0833a', lw=1.5)
    ax[0,1].set_ylim([1.5,3.75])
    ax[0,1].legend(ncol=2,loc=9,frameon=False,)
    ax[0,1].set_title('MLF与同业存单')
    ax[0,1].set_ylabel('(%)',fontsize=10)
    ax[0,1].set_xlabel('')
    
    # * P1,0
    cash_amt_prc[['R001','R007']].dropna()['2019':].plot(ax=ax[1,0],\
        color=['#3778bf','#f0833a'])
    cash_amt_prc[['R021']].dropna()['2019':].plot(ax=ax[1,0],\
        color=['grey'],lw=1) 
    ax[1,0].set_xlabel('')
    ax[1,0].set_title('质押式回购资金利率')
    ax[1,0].legend(loc=9,ncol=3,frameon=False)
    l = do.set_axes_rotation(ax[1,0])
    ax[1,0].set_ylabel('(%)',fontsize=10)

    # * P1,1
    cash_amt_prc[['DR001','GC001']]['2019':].dropna().\
        plot(ax=ax[1,1],ylim=(0,7),color=['#3778bf','#f0833a','grey'])
    # ax_ = ax[1,1].twinx()
    # cash_amt_prc[['DR001']]['2019':].plot(ax=ax_,color='grey',lw=1,ylim=(0,4))
    # ax_.legend(loc=1,ncol=1,frameon=False)
    ax[1,1].set_xlabel('')
    ax[1,1].set_title('隔夜资金利率')
    ax[1,1].legend(loc=9,ncol=2,frameon=False)
    l = do.set_axes_rotation(ax[1,1])
    ax[1,1].set_ylabel('(%)',fontsize=10)

    # * P2,0
    cash_amt_prc[['DR007','GC007']]['2019':].dropna().plot(ax=ax[2,0])
    # ax_ = ax[2,0].twinx()
    # cash_amt_prc[['DR007']]['2019':].plot(ax=ax_,color='grey',lw=1,ylim=(0,4))
    # ax_.legend(loc=1,ncol=1,frameon=False)
    ax[2,0].set_title('7天资金利率')
    ax[2,0].set_xlabel('')
    ax[2,0].legend(loc=9,ncol=2,frameon=False)
    l = do.set_axes_rotation(ax[2,0])
    ax[2,0].set_ylabel('(%)',fontsize=10)

    # * P2,1
    repo_vol = do.get_data('repo_volume'); repo_vol.index=repo_vol.date
    repo_vol['成交量:银行间质押式回购'] = repo_vol[
        ['成交量:R001', '成交量:R007', '成交量:R014', '成交量:R021', '成交量:R1M',
       '成交量:R2M', '成交量:R3M', '成交量:R4M', '成交量:R6M', '成交量:R9M', '成交量:R1Y']
    ].sum(axis=1)
    ax[2,1].fill_between(repo_vol.date['2019':], 0, repo_vol['成交量:银行间质押式回购']['2019':]/10000, \
        label = '成交量(左:万亿)',color='lightgrey',alpha=1)
    ax[2,1].set_ylim([0,6])
    ax_=ax[2,1].twinx()
    (repo_vol['加权利率:R001']['2019':]).plot(ax=ax_,ylim=(0.6,8),label='R001')
    ax[2,1].set_title('隔夜回购利率与成交量')
    ax[2,1].legend(loc=2, frameon=False)
    ax_.legend(loc=1, frameon=False)
    l = do.set_axes_rotation(ax[2,1])
    ax[2,1].set_ylabel('万亿',fontsize=10)
    ax_.set_ylabel('(%)',fontsize=10)
    # repo_vol[['加权利率:R001','成交量:银行间质押式回购','成交量:R001']].to_excel('data.xlsx')

    # * P3,0 R-DR
    cash_amt_prc['R007-DR007'] = (cash_amt_prc['R007']-cash_amt_prc['DR007'])*100
    ax[3,0].fill_between(cash_amt_prc.date['2015':], 0, cash_amt_prc['R007-DR007']['2015':], \
        label = 'R007-DR007(左,BP)',color='lightgrey',alpha=1)
    ax[3,0].set_ylim([-50,200])
    ax[3,0].set_title('R007-DR007')
    ax[3,0].legend(loc=2,frameon=False)
    l = do.set_axes_rotation(ax[3,0],rotation=0)
    ax[3,0].set_ylabel('(BP)',fontsize=10)

    # * P3,1
    # ax[3,1].plot(cash_amt_prc['date']['2015':],cash_amt_prc[['R007','GC007']]['2015':],alpha=0.8)
    cash_amt_prc[['R007','GC007']]['2015':].plot(alpha=0.8,ax=ax[3,1])
    ax[3,1].set_xlabel('')
    ax[3,1].set_title('银行间与交易所资金利率')
    ax[3,1].legend(['R007','GC007'],loc=9,ncol=2,frameon=False)
    l = do.set_axes_rotation(ax[3,1],rotation=0)
    ax[3,1].set_ylabel('(%)',fontsize=10)

    # * P4,0
    # repo_vol = do.get_data('repo_volume'); repo_vol.index=repo_vol.date
    repo_vol[['隔夜回购占比','七天回购占比']]=\
        repo_vol[['成交量:R001','成交量:R007']].div(\
            repo_vol[['成交量:银行间质押式回购']].sum(axis=1),axis=0)
    ax[4,0].fill_between(repo_vol.date['2015':], 0, repo_vol['隔夜回购占比']['2015':], \
        label = '隔夜回购占比(R001)',color='lightgrey',alpha=1)
    ax[4,0].fill_between(repo_vol.date['2015':], 0, repo_vol['七天回购占比']['2015':], \
        label = '七天回购占比(R007)',color='orange',alpha=1)
    ax[4,0].legend(ncol=2,loc=0,frameon=False)
    ax[4,0].set_title('隔夜与七天')

    # * P4,1
    irs = do.get_data('spreads');irs.index=irs.date
    irs[['IRS_1y_FR007', 'IRS_5y_FR007','IRS_5y_shibor3m']]['2015':].dropna().plot(ax=ax[4,1],\
        ylim=(0,7),color=['#3778bf','#f0833a','grey'])
    ax[4,1].set_xlabel('')
    ax[4,1].set_title('IRS')
    ax[4,1].legend(['IRS:1年(FR007)','IRS:5年(FR007)','IRS:5年(3M SHIBOR)'],\
        ncol=2,loc=9,frameon=False)
    l = do.set_axes_rotation(ax[4,1],rotation=0)
    ax[4,1].set_ylabel('(%)',fontsize=10)

    # * P5,0
    irs['cd:6M-R007'] = (irs['cd_AAA_6m']-cash_amt_prc['R007'])*100
    irs['R007'] = cash_amt_prc['R007']
    ax[5,0].fill_between(irs.date['2015':],0,irs['cd:6M-R007']['2015':],\
        label='同业存单:6个月:AAA-R007',color='lightgrey',alpha=1)
    ax_=ax[5,0].twinx()
    irs[['R007','cd_AAA_6m']]['2015':].plot(ax=ax_)
    ax[5,0].set_title('6M存单-R007')
    # ax[5,0].set_xticklabels(ax[5,0].get_xticklabels(), rotation=30)
    ax[5,0].legend(loc=2,frameon=False)
    ax_.legend(['R007','同业存单:6个月:AAA'],loc=1,ncol=1,frameon=False)
    ax[5,0].set_ylim([-300,300])
    ax_.set_ylim([0,8])
    ax[5,0].set_ylabel('(BP)',fontsize=10)
    ax_.set_ylabel('(%)',fontsize=10)

    # * P5,1
    irs['1年'] = irs['中短票_AA+_1y']-cash_amt_prc['R007']
    irs['3年'] = irs['中短票_AA+_3y']-cash_amt_prc['R007']
    irs['5年'] = irs['中短票_AA+_5y']-cash_amt_prc['R007']
    irs[['1年', '3年','5年']]['2015':].plot(ax=ax[5,1],\
        color=['#3778bf','#f0833a','grey'],ylim=(-3,4))
    ax[5,1].set_xlabel('')
    ax[5,1].set_title('中短票:AA+-R007')
    ax[5,1].legend(ncol=3,loc=9,frameon=False)
    ax[5,1].axhline(y=0,lw=1,color='black',ls='--')
    l = do.set_axes_rotation(ax[5,1],rotation=0)
    ax[5,1].set_ylabel('(%)',fontsize=10)

    # * P6,0
    irs['国开债:10年-R007'] = (irs['国开10年']-cash_amt_prc['R007'])
    irs['地方债:3年:AAA-R007'] = (irs['地方债_AAA_3y']-cash_amt_prc['R007'])
    irs = irs[['国开债:10年-R007','地方债:3年:AAA-R007']]
    irs[['国开债:10年-R007','地方债:3年:AAA-R007']]['2015':].plot(ax=ax[6,0],\
        ylim=(-3,3),color=['#3778bf','#f0833a'])
    ax[6,0].set_xlabel('')
    ax[6,0].set_title('国开10年与地方债3年-R007')
    ax[6,0].legend(ncol=2,loc=9 ,frameon=False)
    ax[6,0].axhline(y=0,lw=1,color='black',ls='--')
    l = do.set_axes_rotation(ax[6,0],rotation=0)
    ax[6,0].set_ylabel('(%)',fontsize=10)

    fig.delaxes(ax[6,1])

    # * P7,0
    df = do.get_data('cash_cost')
    df.index = df.date

    df = df.loc[df.date>='2019-07']
    df['R007-DR007'] = df['R007']-df['DR007']
    df = df.loc[df['R007-DR007']<=2] # 去除异常值

    ax[7,0].fill_between(df.date, 0, df['R007-DR007'].rolling(1 ).mean()*100, \
            label = 'R007-DR007',alpha=1,color='lightgrey')
    do.set_axes_rotation(ax[7,0],45)

    ax_=ax[7,0].twinx()
    ax_.plot(df.date,df['R007'],lw=1,label='R007',color='black'); 
    ax_.plot(df.date,df['DR007'],lw=1,label='DR007',color='#f0833a')
    ax_.set_title('R007-DR007',fontsize=14)
    ax[7,0].legend(loc='upper left',frameon=False,fontsize=12)
    ax[7,0].set_ylabel('BP')
    ax_.set_ylabel('%')
    ax_.legend(ncol=2,loc='upper right',frameon=False,fontsize=12)
    
    # * P7,1 
    df = do.get_data('fig_liquidity_premium') ; df.index = df.date
    df = df.fillna(method='ffill')
    df[['shibor_3m', 'IRS：FR007：1y']]['2020':].plot(ax=ax[7,1])
    df[['MLF：1年']]['2020':].plot(c='red', ls='--',ax=ax[7,1])
    ax[7,1].legend(ncol=3,loc='upper right',frameon=False,fontsize=10)
    ax[7,1].set_title('三个月shibor与利率互换')
    
    plt.suptitle('流动性指标',fontsize=24,y=1.01)
    plt.tight_layout()

    return fig

def rate_level_fig(hb_base,end_day):
    df = do.get_data('rates');df.index = df.date

    plt.style.use({'font.size' : 12}) 
    fig,ax = plt.subplots(ncols=2,nrows=10,figsize=(6*2,4*10), dpi=300)
    
    # * P0.0 & P0.1 
    # 收益率曲线- 现值 vs 20年底 vs 2007以来分位数
    ## 选取对比日期
    today = end_day; base = df['2021':'2021'].index[-1]
    # 国债
    name = '国债'
    m = ['3月', '6月', '1年', '3年', '5年', \
        '7年', '10年', '20年', '30年']
    l = [name+x for x in m]
    d = pd.DataFrame(columns=[0,1,2,3,6,9,12,24,36])
    d.loc[today] = df.loc[today,l].tolist()
    d.loc[base.date()] = df.loc[base,l].tolist()
    d.loc['25分位数'] = [np.quantile(df[x]['2015':],0.25) for x in l]
    d.loc['75分位数'] = [np.quantile(df[x]['2015':],0.75) for x in l]
    d.loc['中位数'] = [np.quantile(df[x]['2015':],0.5) for x in l]
    #plot 
    d.loc[today].plot(ax=ax[0,0],label='现值('+today.strftime('%Y%m%d')+')',\
        marker='o',color='#3778bf')
    d.loc[base.date()].plot(ax=ax[0,0],color='#f0833a',label='2021年底',marker='s')
    d.loc['25分位数'].plot(ax=ax[0,0],ls='--',color='lightgrey',alpha=1)
    d.loc['75分位数'].plot(ax=ax[0,0],ls='--',color='lightgrey',alpha=1)
    d.loc['中位数'].plot(ax=ax[0,0],color='orange',alpha=0.3)
    ax[0,0].set_ylim([1.5,4.5])
    ax[0,0].set_xticks([0,3,6,9,12,24,36])
    ax[0,0].set_xticklabels(['3M','3Y','5Y','7Y','10Y','20Y','30Y'])
    ax[0,0].legend(ncol=2,loc='best',frameon=False,fontsize=10)
    ax[0,0].set_title(name+'到期收益率曲线(2015以来)')
    ax[0,0].set_ylabel('(%)',fontsize=10)
    # 国开
    name = '国开'
    m = ['3月', '6月', '1年', '3年', '5年', \
        '7年', '10年', '20年', '30年']
    l = [name+x for x in m]
    d = pd.DataFrame(columns=[0,1,2,3,6,9,12,24,36])
    d.loc[today] = df.loc[today,l].tolist()
    d.loc[base.date()] = df.loc[base,l].tolist()
    d.loc['25分位数'] = [np.quantile(df[x]['2015':],0.25) for x in l]
    d.loc['75分位数'] = [np.quantile(df[x]['2015':],0.75) for x in l]
    d.loc['中位数'] = [np.quantile(df[x]['2015':],0.5) for x in l]
    #plot
    d.loc[today].plot(ax=ax[0,1],label='现值('+today.strftime('%Y%m%d')+')',\
        marker='o',color='#3778bf')
    d.loc[base.date()].plot(ax=ax[0,1],color='#f0833a',label='2021年底',marker='s')
    d.loc['25分位数'].plot(ax=ax[0,1],ls='--',color='lightgrey',alpha=1)
    d.loc['75分位数'].plot(ax=ax[0,1],ls='--',color='lightgrey',alpha=1)
    d.loc['中位数'].plot(ax=ax[0,1],color='orange',alpha=0.3)
    ax[0,1].set_ylim([1.5,5.5])
    ax[0,1].set_xticks([0,3,6,9,12,24,36])
    ax[0,1].set_xticklabels(['3M','3Y','5Y','7Y','10Y','20Y','30Y'])
    ax[0,1].legend(ncol=2,loc='best',frameon=False,fontsize=10)
    ax[0,1].set_title(name+'到期收益率曲线(2015以来)')
    ax[0,1].set_ylabel('(%)',fontsize=10)

    # * P1.0 & P1.1 国债10&1y
    #10y
    year=10
    a = df[['国债'+str(year)+'年']  ]['2007':]
    q25 = np.percentile(a.values, 25,interpolation='linear')
    q75 = np.percentile(a.values, 75,interpolation='linear')
    med = np.median(a.values)
    a['2015':].plot(ax=ax[1,0],label='国债'+str(year)+'年')
    a.iloc[:,0].rolling(750).quantile(0.75)['2015':].plot(ax=ax[1,0],label='25/75分位数',\
        ls='--',lw='0.8')
    a.iloc[:,0].rolling(750).quantile(0.5)['2015':].plot(ax=ax[1,0],label='中位数',\
        ls='--',lw='0.8')
    # ax[1,0].axhline(y=q25,ls='--',color='lightgrey',label='25/75分位数')
    # ax[1,0].axhline(y=med,ls='-',color='orange',label='中位数')
    # ax[1,0].axhline(y=q75,ls='--',color='lightgrey',label='25/75分位数')
    a.iloc[:,0].rolling(750).quantile(0.25)['2015':].plot(ax=ax[1,0],\
        ls='--',lw='0.8',label='')
    ax[1,0].set_xlabel('')
    ax[1,0].set_ylim([2,5])
    ax[1,0].set_title('国债'+str(year)+'年')
    ax[1,0].set_ylabel('(%)',fontsize=10)
    l=do.set_axes_rotation(ax[1,0],0)
    ax[1,0].legend(ncol=3,frameon=False,loc=9,fontsize=10)
    # 1y
    year=1
    a = df[['国债'+str(year)+'年']  ]['2007':]
    q25 = np.percentile(a.values, 25,interpolation='linear')
    q75 = np.percentile(a.values, 75,interpolation='linear')
    med = np.median(a.values)

    a.iloc[750:,0]['2015':].plot(ax=ax[1,1],label='国债'+str(year)+'年')
    a.iloc[:,0].rolling(750).quantile(0.75)['2015':].plot(ax=ax[1,1],label='25/75分位数',\
        ls='--',lw='0.8')
    a.iloc[:,0].rolling(750).quantile(0.5)['2015':].plot(ax=ax[1,1],label='中位数',\
        ls='--',lw='0.8')
    # ax[1,1].axhline(y=q25,ls='--',color='lightgrey',label='25/75分位数')
    # ax[1,1].axhline(y=med,ls='-',color='orange',label='中位数')
    ax[1,1].set_xlabel('')
    ax[1,1].legend(ncol=3,frameon=False,loc=9,fontsize=10)
    a.iloc[:,0].rolling(750).quantile(0.25)['2015':].plot(ax=ax[1,1],label='',\
        ls='--',lw='0.8')
    # ax[1,1].axhline(y=q75,ls='--',color='lightgrey',label='25/75分位数')
    ax[1,1].set_ylim([0,5])
    ax[1,1].set_title('国债'+str(year)+'年')
    ax[1,1].set_ylabel('(%)',fontsize=10)
    l=do.set_axes_rotation(ax[1,1],0)

    # * P2.0 & P2.1 国开10&1y
    #10y
    year=10
    a = df[['国开'+str(year)+'年']  ]['2007':]
    q25 = np.percentile(a.values, 25,interpolation='linear')
    q75 = np.percentile(a.values, 75,interpolation='linear')
    med = np.median(a.values)

    a.iloc[750:,0]['2015':].plot(ax=ax[2,0],label='国开'+str(year)+'年')
    a.iloc[:,0].rolling(750).quantile(0.75)['2015':].plot(ax=ax[2,0],label='25/75分位数',\
        ls='--',lw='0.8')
    a.iloc[:,0].rolling(750).quantile(0.5)['2015':].plot(ax=ax[2,0],label='中位数',\
        ls='--',lw='0.8')
    # ax[2,0].axhline(y=q25,ls='--',color='lightgrey',label='25/75分位数')
    # ax[2,0].axhline(y=med,ls='-',color='orange',label='中位数')
    ax[2,0].set_xlabel('')
    ax[2,0].legend(ncol=3,frameon=False,loc=9,fontsize=10)
    a.iloc[:,0].rolling(750).quantile(0.25)['2015':].plot(ax=ax[2,0],label='',\
        ls='--',lw='0.8')
    # ax[2,0].axhline(y=q75,ls='--',color='lightgrey',label='25/75分位数')
    ax[2,0].set_ylim([2.5,6.5])
    ax[2,0].set_title('国开'+str(year)+'年')
    ax[2,0].set_ylabel('(%)',fontsize=10)
    l=do.set_axes_rotation(ax[2,0],0)
    # 1y
    year=1
    a = df[['国开'+str(year)+'年']  ]['2007':]
    q25 = np.percentile(a.values, 25,interpolation='linear')
    q75 = np.percentile(a.values, 75,interpolation='linear')
    med = np.median(a.values)

    a.iloc[750:,0]['2015':].plot(ax=ax[2,1],label='国开'+str(year)+'年')
    a.iloc[:,0].rolling(750).quantile(0.75)['2015':].plot(ax=ax[2,1],label='25/75分位数',\
        ls='--',lw='0.8')
    a.iloc[:,0].rolling(750).quantile(0.5)['2015':].plot(ax=ax[2,1],label='中位数',\
        ls='--',lw='0.8')
    # ax[2,1].axhline(y=q25,ls='--',color='lightgrey',label='25/75分位数')
    # ax[2,1].axhline(y=med,ls='-',color='orange',label='中位数')
    ax[2,1].set_xlabel('')
    ax[2,1].legend(ncol=3,frameon=False,loc=9,fontsize=10)
    a.iloc[:,0].rolling(750).quantile(0.25)['2015':].plot(ax=ax[2,1],label='',\
        ls='--',lw='0.8')
    # ax[2,1].axhline(y=q75,ls='--',color='lightgrey',label='25/75分位数')
    ax[2,1].set_ylim([0,6.5])
    ax[2,1].set_title('国开'+str(year)+'年')
    ax[2,1].set_ylabel('(%)',fontsize=10)
    l=do.set_axes_rotation(ax[2,1],0)

    # * P3.0 P3.1 国债/国开bp变动
    year_base = df['2022'].index[0]
    end = end_day 
    from fig_func import rate_change
    ax[3,0] = rate_change(ax[3,0], year_base, end , 'gz')
    ax[3,1] = rate_change(ax[3,1], year_base, end , 'gk')
    
    # * P4.0 P4.1 国债/国开bp变动 ———— (月度)
    # base = df.loc[(end_day-relativedelta(months=1)).strftime('%Y-%m')].index[0]
    # base = df.loc[(end_day-relativedelta(months=0)).strftime('%Y-%m')].index[0]
    
    end = end_day #df['2021'].index[-1]
    ax[4,0] = rate_change(ax[4,0], hb_base, end , 'gz')
    ax[4,1] = rate_change(ax[4,1], hb_base, end , 'gk')

    # * P4.0地方债-国债
    df['地方债-国债'] = (df['地方5年']-df['国债5年'])*100
    ax[5,0].fill_between(df.date['2015':],0,df['地方债-国债']['2015':],\
        label='地方债-国债(左:BP)',color='lightgrey',alpha=1)
    ax_=ax[5,0].twinx()
    df[['地方5年','国债5年']]['2015':].plot(ax=ax_,color=['#3778bf','#f0833a'])
    ax_.set_yticks(np.arange(1,6))
    ax[5,0].set_yticks(range(0,100,20))
    ax[5,0].legend(loc=2,frameon=False,fontsize=10)
    ax_.legend(['地方债:5年:AAA','国债:5年'],\
        loc=1,frameon=False,fontsize=10)
    ax[5,0].set_title('地方债-国债(5Y)')
    ax[5,0].set_ylim([0,90])
    ax_.set_ylim([1.5,5.5])
    ax[5,0].set_ylabel('(BP)',fontsize=10)
    ax_.set_ylabel('(%)',fontsize=10)

    # * P5.1国开债-国债
    df['国开债-国债'] = (df['国开10年']-df['国债10年'])*100
    ax[5,1].fill_between(df.date['2015':],0,df['国开债-国债']['2015':],\
        label='国开债-国债(左:BP)',color='lightgrey',alpha=1)
    ax_= ax[5,1].twinx()
    df[['国开10年','国债10年']]['2015':].plot(ax=ax_,\
        color=[ '#3778bf','#f0833a'])
    ax[5,1].set_title('国开债-国债(10Y)')
    ax[5,1].legend(loc=2,frameon=False,fontsize=10)
    ax_.legend(['国开债:10年','国债:10年'],\
        loc=1,frameon=False,fontsize=10)
    ax[5,1].set_ylim([0,160])
    ax_.set_ylim([2,6.5])
    ax[5,1].set_ylabel('(BP)',fontsize=10)
    ax_.set_ylabel('(%)',fontsize=10)

    # * P6.0存单-Dr007
    cash = do.get_data('cash_cost');cash.index = cash.date
    df['存单-DR007'] = (df['cd_3m_aaa+']-cash['DR007'])*100
    df['DR007'] = cash['DR007']
    ax[6,0].fill_between(df.date['2015':],0,df['存单-DR007']['2015':],\
        label='存单-DR007(左:BP)',color='lightgrey',alpha=1)
    ax_= ax[6,0].twinx()
    df[['cd_3m_aaa+','DR007']]['2015':].plot(ax=ax_,color=['#f0833a','#3778bf'])
    ax[6,0].set_title('存单与DR007')
    ax[6,0].legend(loc=2,frameon=False,fontsize=10)
    ax_.legend(['同业存单:3个月:AAA+','DR007'],\
        loc=1,ncol=2,frameon=False,fontsize=10)
    ax[6,0].set_ylim([-100,250])
    ax_.set_ylim([1.0,5.5])
    ax[6,0].set_ylabel('(BP)',fontsize=10)
    ax_.set_ylabel('(%)',fontsize=10)

    # * P6.1中票
    # df[['中票_AAA_1y','中票_AAA_5y','中票_AA+_1y','中票_AA+_5y']]['2010':].\
    df[['中票_AAA_5y','中票_AA+_5y','中票_AA_5y']]['2015':].\
        plot(ax=ax[6,1],color = ["#3778bf","lightgrey","#f0833a"])
    ax[6,1].axhline(y=np.median(df['中票_AAA_5y']['2015':]),ls='--',color='grey',label='5Y:AAA:中位数')
    ax[6,1].axhline(y=np.median(df['中票_AA+_5y']['2015':]),ls='--',color='brown',label='5Y:AA+:中位数')
    ax[6,1].axhline(y=np.median(df['中票_AA_5y']['2015':]),ls='--',color='black',label='5Y:AA:中位数')
    ax[6,1].set_xlabel('')
    ax[6,1].set_title('5Y中票收益率')
    ax[6,1].legend(ncol=3,loc=9,fontsize=10,frameon=False)
    ax[6,1].set_ylim([1,8])
    ax[6,1].set_ylabel('(%)',fontsize=10)
    l=do.set_axes_rotation(ax[6,1],0)
    
    # * P7.0 7.1 城投AAA收益变动
    ax[7,0] = credit_change(ax[7,0], 'AAA', hb_base,end_day)
    ax[7,1] = credit_change(ax[7,1], 'AA', hb_base,end_day)
    # * 
    ax[8,0] = credit_curve(ax[8,0], 'AAA', end_day)
    ax[8,1] = credit_curve(ax[8,1], 'AA' , end_day)
    
    ax[9,0] = credit_change(ax[9,0], 'AAA', year_base,end_day)
    ax[9,1] = credit_change(ax[9,1], 'AA', year_base,end_day)
    ax[9,0].set_title('城投_AAA_收益率变动')
    ax[9,1].set_title('城投_AA_收益率变动')

    fig.suptitle('市场利率水平',fontsize=24,y=1.01)
    fig.tight_layout()

    return fig

def rate_diff_fig():
    rates = do.get_data('rates'); rates.index = rates.date

    plt.style.use({'font.size' : 12}) 
    fig,ax = plt.subplots(ncols=2,nrows=12,figsize=(6*2,4*12), dpi=300)

    # * P0.0 期限利差1
    rates0 = rates.loc[rates['date'] >= '2019-01-01']
    margin1 = rates0['国债10年']-rates0['国债7年']
    margin2 = rates0['国开10年']-rates0['国开7年']
    df = pd.DataFrame([margin1,margin2])
    df.index = ['国债10Y-7Y','国开10Y-7Y']
    df  = df.T
    ax[0,0].plot(rates0['date'],margin1*100,'#3778bf',label="国债10Y-7Y")
    ax[0,0].plot(rates0['date'],margin2*100,'#f0833a',label='国开10Y-7Y')
    ax[0,0].set_title('期限利差1')
    ax[0,0].set_ylim([-30,30])
    ax[0,0].set_ylabel('(BP)',fontsize=10)
    ax[0,0].legend(ncol=3,loc=9,fontsize=10,frameon=False)
    l = do.set_axes_rotation(ax[0,0])

    # * P0.1 期限利差2
    rates0 = rates.loc[rates['date'] >= '2019-01-01']
    margin3 = rates0['国债30年']-rates0['国债10年']
    margin4 = rates0['国债10年']-rates0['国债1年']
    margin5 = rates0['国债3年']-rates0['国债1年']
    df = pd.DataFrame([margin3,margin4,margin5])
    df.index = ['国债30Y-10Y','国开10Y-1Y','国开3Y-1Y']
    df  = df.T
    ax[0,1].plot(rates0['date'],margin3*100,'#3778bf',label="国债30Y-10Y")
    ax[0,1].plot(rates0['date'],margin4*100,'#f0833a',label='国开10Y-1Y')
    ax[0,1].plot(rates0['date'],margin5*100,'gray',label='国开3Y-1Y')
    ax[0,1].set_title('期限利差2')
    ax[0,1].set_ylabel('(BP)',fontsize=10)
    ax[0,1].set_ylim([-50,200])
    ax[0,1].legend(ncol=3,loc=9,fontsize=10,frameon=False)
    l = do.set_axes_rotation(ax[0,1])

    # * P1.0 隐含税率
    rates0 = rates.loc[rates['date'] >= '2019-01-01']
    tax_rate = 1 - rates0['国债10年']/rates0['国开10年']
    ax[1,0].plot(rates0['date'],tax_rate,'#3778bf',label="隐含税率(%)")
    ax[1,0].set_title('十年国开与国债的隐含税率', )
    ax[1,0].set_ylim([0.05,0.20])
    ax[1,0].legend(ncol=3,loc=9,fontsize=10,frameon=False)
    l = do.set_axes_rotation(ax[1,0])

    # * P1.1 国开与非国开的利差
    rates0 = rates.loc[rates['date'] >= '2019-01-01']
    margin6 = rates0['农发10年']-rates0['国开10年']
    margin7 = rates0['口行10年']-rates0['国开10年']
    margin8 = rates0['国开10年']-rates0['国债10年']
    df = pd.DataFrame([margin6,margin7,margin8])*100
    df.index = ['农发-国开','口行-国开','国开-国债']
    df  = df.T    
    df.plot(ax=ax[1,1],color=['#3778bf','#f0833a','gray'])
    ax[1,1].set_title('十年国开与非国开的利差')
    ax[1,1].set_ylabel('(BP)',fontsize=10)
    ax[1,1].set_ylim([-10, 65])
    ax[1,1].legend(ncol=3,loc=9,fontsize=10,frameon=False)
    l = do.set_axes_rotation(ax[1,1])

    # * P2.0 国债期限利差
    rates1 = rates.loc[rates['date'] >= '2015-01-01']
    #计算利差
    margin1 = rates1['国债10年']-rates1['国债1年']
    margin2 = rates1['国债10年']-rates1['国债3年']
    margin3 = rates1['国债3年']-rates1['国债1年']
    df = pd.DataFrame([margin1,margin2,margin3])
    df.index = ['10Y-1Y','10Y-3Y','3Y-1Y']
    df  = df.T    
    df.plot(ax=ax[2,0], color = ['#3778bf','#f0833a','gray'])
    ax[2,0].set_title('国债期限利差', )
    ax[2,0].set_ylabel('(%)',fontsize=10)
    ax[2,0].set_ylim([-0.5,2])
    ax[2,0].legend(ncol=3,loc=9,fontsize=10,frameon=False)

    # * P2.1 国债、国开债10年-1年
    rates2 = rates.loc[rates['date'] >= '2015-01-01']
    margin4 = rates2['国债10年']-rates2['国债1年']
    margin5 = rates2['国开10年']-rates2['国开1年']
    df = pd.DataFrame([margin4,margin5])
    df.index = ['国债10Y-1Y','国开10Y-1Y']
    df  = df.T  
    ax[2,1].plot(rates2['date'],margin4,'#3778bf',label="国债10Y-1Y")
    ax[2,1].plot(rates2['date'],margin5,'#f0833a',label='国开10Y-1Y')
    ax[2,1].set_title('国债、国开债10年-1年' )
    ax[2,1].set_ylabel('(%)',fontsize=10)
    ax[2,1].set_ylim([-1,3])
    ax[2,1].legend(ncol=3,loc=9,fontsize=10,frameon=False)

    # * P3.0 国债1年收益率与10年-1年利差
    rates3 = rates.loc[rates['date'] >= '2015-01-01']
    margin6 = rates3['国债10年']-rates3['国债1年']
    ax[3,0].grid(ls='--')
    ax[3,0].set_axisbelow(True)
    ax[3,0].scatter(rates3['国债1年'][:-1],margin6[:-1], marker='o', facecolors='none', edgecolors='#3778bf')
    ax[3,0].scatter(rates3['国债1年'][-1],margin6[-1], marker='o', facecolors='none', edgecolors='#f0833a')
    ax[3,0].set_title('国债1年收益率与10年-1年利差(2015以来)' )
    ax[3,0].annotate('当前值',xy=(rates3['国债1年'][-1],margin6[-1]),xytext=(rates3['国债1年'][-1],margin6[-1]-1),color="k",weight="bold",alpha=0.9,arrowprops=dict(arrowstyle="-",connectionstyle="arc3",color="k",alpha=0.9),bbox={'facecolor': 'lightsteelblue', 'edgecolor':'k','alpha': 0.9,'pad':2},fontsize=10)
    ax[3,0].set_ylabel('利差(%)',fontsize=10)
    ax[3,0].set_xlabel('到期收益率(%)',fontsize=10)

    # * P3.1 国债10年收益率与10年-1年利差
    rates3 = rates.loc[rates['date'] >= '2015-01-01']
    margin7 = rates3['国债30年']-rates3['国债10年']
    ax[3,1].grid(ls='--')
    ax[3,1].set_axisbelow(True)
    ax[3,1].scatter(rates3['国债10年'][:-1],margin7[:-1], marker='o',facecolors='none', edgecolors='#3778bf')
    ax[3,1].scatter(rates3['国债10年'][-1],margin7[-1], marker='o',facecolors='none', edgecolors='#f0833a')
    ax[3,1].set_title('国债10年收益率与30年-10年利差(2015以来)' )
    ax[3,1].annotate('当前值',xy=(rates3['国债10年'][-1],margin7[-1]),xytext=(rates3['国债10年'][-1],margin7[-1]-0.1),color="k",weight="bold",alpha=0.9,arrowprops=dict(arrowstyle="-",connectionstyle="arc3",color="k",alpha=0.9),bbox={'facecolor': 'lightsteelblue', 'edgecolor':'k','alpha': 0.9,'pad':2},fontsize=10)
    ax[3,1].set_ylabel('利差(%)',fontsize=10)
    ax[3,1].set_xlabel('到期收益率(%)',fontsize=10)

    # * P4.0 国债2*5Y-(1Y+10Y)
    rates4 = rates.loc[rates['date'] >= '2015-01-01']
    gz = rates4['国债5年']*2 - ( rates4['国债1年'] + rates4['国债10年'])
    ax[4,0].plot(rates4['date'],gz,'#3778bf',label="2*5Y-(1Y+10Y)")
    ax[4,0].set_title('国债2*5Y-(1Y+10Y)')
    ax[4,0].set_ylim([-0.5,1])
    ax[4,0].legend(ncol=3,loc=9,fontsize=10,frameon=False)
    ax[4,0].set_ylabel('(%)',fontsize=10)

    # * P4.1 国开债2*5Y-(1Y+10Y)
    rates4 = rates.loc[rates['date'] >= '2015-01-01']
    gkz = rates4['国开5年']*2 - ( rates4['国开1年'] + rates4['国开10年'])
    ax[4,1].plot(rates4['date'],gkz,'#3778bf',label="2*5Y-(1Y+10Y)")
    ax[4,1].set_title('国开债2*5Y-(1Y+10Y)', )
    ax[4,1].set_ylim([-0.5,1.5])
    ax[4,1].legend(ncol=3,loc=9,fontsize=10,frameon=False)
    ax[4,1].set_ylabel('（%）',fontsize=10)

    # * P5.0 10年期国债与国开债-国债利差
    rates1 = rates.loc[rates['date'] >= '2015-01-01']
    margin1 = rates1['国开10年']-rates1['国债10年']
    ax[5,0].grid(ls='--')
    ax[5,0].set_axisbelow(True)
    ax[5,0].scatter(rates1['国债10年'][:-1],margin1[:-1], marker='o',facecolors='none', edgecolors='#3778bf')
    ax[5,0].scatter(rates1['国债10年'][-1],margin1[-1], marker='o',facecolors='none', edgecolors='#f0833a')
    ax[5,0].set_title('10年期国债与国开债-国债利差(2015以来)', )
    ax[5,0].annotate('当前值',xy=(rates1['国债10年'][-1],margin1[-1]),xytext=(rates1['国债10年'][-1],margin1[-1]+0.5),color="k",weight="bold",alpha=0.9,arrowprops=dict(arrowstyle="-",connectionstyle="arc3",color="k",alpha=0.9),bbox={'facecolor': 'lightsteelblue', 'edgecolor':'k','alpha': 0.9,'pad':2},fontsize=10)
    ax[5,0].set_ylabel('利差(%)',fontsize=10)
    ax[5,0].set_xlabel('到期收益率(%)',fontsize=10)

    # * P5.1 国开债-国债关键期限利差
    rates1 = rates.loc[rates['date'] >= '2009-01-05']
    rates1.index = rates1['date']
    keymargin1 = rates1[['国债6月', '国债1年', '国债3年','国债5年', '国债7年', '国债10年']]
    keymargin1.columns = ['6M', '1Y', '3Y','5Y', '7Y', '10Y']
    keymargin2 = rates1[['国开6月', '国开1年', '国开3年','国开5年', '国开7年', '国开10年']]
    keymargin2.columns = ['6M', '1Y', '3Y','5Y', '7Y', '10Y']
    keymargin = pd.concat([keymargin1[-1:],keymargin2[-1:]],axis=0)
    keymargin.index = ['国债', '国开债']
    keymargin= pd.DataFrame(keymargin.values.T, index=keymargin.columns, columns=keymargin.index)
    keymargin['国开债-国债'] = (keymargin['国开债'] - keymargin['国债'])*100
    
    ax[5,1].plot(keymargin.index,keymargin['国债'],'#3778bf',label="国债")
    ax[5,1].plot(keymargin.index,keymargin['国开债'],'#f0833a',label='国开债')
    ax[5,1].set_ylim([1.5,4])
    ax[5,1].legend(ncol=3,loc=2,fontsize=10,frameon=False)
    ax[5,1].set_ylabel('(%)',fontsize=10)
    ax_=ax[5,1].twinx()
    ax_.bar(keymargin.index,keymargin['国开债-国债'], width=0.7, color='gray',alpha = 0.2,label='国开债-国债')
    ax_.set_ylim([0,50])
    ax_.legend(ncol=3,loc=1,fontsize=10,frameon=False)
    ax_.set_ylabel('(BP)',fontsize=10)
    ax_.set_title('国开债-国债关键期限利差', )

    # * 6.0 农发、口行-国开利差:10年
    rates2 = rates.loc[rates['date'] >= '2015-01-01']
    rates2.index = rates2['date']
    rates2 = rates2[['国开10年', '农发10年', '口行10年']]
    rates2['农发-国开'] = (rates2['农发10年'] - rates2['国开10年'])*100

    rates2['口行-国开'] = (rates2['口行10年'] - rates2['国开10年'])*100

    ax[6,0].plot(rates2.index,rates2['国开10年'],'#3778bf',label="国开10年",linewidth=1)
    ax[6,0].plot(rates2.index,rates2['农发10年'],'#f0833a',label='农发10年',linewidth=1)
    ax[6,0].plot(rates2.index,rates2['口行10年'],'gray',label='口行10年',linewidth=1)
    ax[6,0].set_ylim([2.5,6])
    ax[6,0].legend(ncol=1,loc=2,fontsize=10,frameon=False)
    ax[6,0].set_ylabel('(%)',fontsize=10)
    ax_=ax[6,0].twinx()
    ax_.bar(rates2.index,rates2['农发-国开'], width=1, color='#f0833a',alpha = 0.2,label='农发-国开')
    ax_.bar(rates2.index,rates2['口行-国开'], width=1, color='gray',alpha = 0.2,label='口行-国开')
    ax_.set_ylim([0,40])
    ax_.legend(ncol=1,loc=1,fontsize=10,frameon=False)
    ax_.set_ylabel('(BP)',fontsize=10)
    ax_.set_title('农发、口行-国开利差:10年', )

    # * 6.1 国开债新老券利差
    from fig_func import gk_new_old
    ax[6,1] = gk_new_old(ax[6,1])
    ax[6,1].set_title('国开债新老券利差')

    # * 7.0 信用利差水平
    rates1 = rates[['中票_AAA_1y', '中票_AAA_3y', '中票_AAA_5y','中票_AA+_1y', '中票_AA+_3y', '中票_AA+_5y','中票_AA_1y', '中票_AA_3y', '中票_AA_5y','中票_AA-_1y', '中票_AA-_3y', '中票_AA-_5y']]
    rates1 = rates1.loc[rates1.index >= '2015-01-05']
    credit1  = rates1[-1:]
    credit2 = rates1.describe()[4:7]
    credit3 = rates1.loc[rates1.index == '2020-12-31']
    credit = pd.concat([credit1,credit2,credit3],axis=0)
    credit.index = [['现值','25分位数','中位数','75分位数','2020年底']]
    #转置
    credit= pd.DataFrame(credit.values.T, index=credit.columns, columns=credit.index)
    
    ax[7,0].plot(credit[['现值']],'#3778bf',label="现值")
    ax[7,0].plot(credit[['25分位数']],'#f0833a',label='25分位数')
    ax[7,0].plot(credit[['中位数']],'gray',label='中位数')
    ax[7,0].plot(credit[['75分位数']],'tomato',label='75分位数')
    ax[7,0].plot(credit[['2020年底']],'yellow',label='2020年底')
    ax[7,0].set_ylabel('(%)',fontsize=10)
    ax[7,0].set_title('信用利差水平', )
    ax[7,0].legend(ncol=3,loc=9,fontsize=10,frameon=False)
    l = do.set_axes_rotation(ax[7,0],rotation = 45)

    # * 7.1 分评级信用利差
    rates1 = rates[['中票_AAA_1y', '中票_AAA_3y', '中票_AAA_5y',\
        '中票_AA+_1y', '中票_AA+_3y', '中票_AA+_5y','中票_AA_1y',\
        '中票_AA_3y', '中票_AA_5y','中票_AA-_1y', '中票_AA-_3y', '中票_AA-_5y',\
        '国开1年','国开5年']]
    rates1 = rates1.loc[rates1.index >= '2015-01-05'] * 100
    
    # ax[7,1].plot(rates1.index,rates1['中票_AAA_1y']-rates1['国开1年'],\
        # '#3778bf',label="AAA1年")
    ax[7,1].plot(rates1.index,rates1['中票_AAA_5y']-rates1['国开5年'],\
        '#3778bf',label='AAA5年')
    # ax[7,1].plot(rates1.index,rates1['中票_AA+_1y']-rates1['国开1年'],\
        # 'gray',label='AA+1年')
    ax[7,1].plot(rates1.index,rates1['中票_AA+_5y']-rates1['国开5年'],\
        '#f0833a',label='AA+5年')
    # ax[7,1].plot(rates1.index,rates1['中票_AA_1y']-rates1['国开1年'],\
        # 'gray',label='AA1年')
    ax[7,1].plot(rates1.index,rates1['中票_AA_5y']-rates1['国开5年'],\
        'gray',label='AA5年')
    ax[7,1].set_title('分评级信用利差', )
    # ax[7,1].set_ylim([1.5,6.5])
    ax[7,1].legend(ncol=3,loc=9,fontsize=10,frameon=False)

    # * 8.0 中美利差:10年
    rates_us = do.get_data('rates_us');rates_us.index=rates_us.date
    rates1 = rates.loc[rates['date'] >= '2015-01-04']
    rates1.index = rates1['date']
    rates_us1 = rates_us.loc[rates_us['date'] >= '2015-01-04']
    rates_us1.index = rates_us1['date']
    rates_us1 = rates_us1.dropna()
    #计算利差
    margin1 = (rates1['国债10年']-rates_us1['美债10年']) * 100
    df = pd.DataFrame([rates1['国债10年'],rates_us1['美债10年'],margin1])
    df.index = ['国债10年','美债10年','中美利差10年']
    df  = df.T

    ax[8,0].plot(rates_us1['date'],rates_us1['美债10年'],'#f0833a',label='美债10年')
    ax[8,0].plot(rates1['date'],rates1['国债10年'],'#3778bf',label="国债10年")
    ax[8,0].set_ylabel('（%）',fontsize=10)
    ax[8,0].set_ylim([0,6])
    ax[8,0].legend(ncol=3,loc=2,fontsize=10,frameon=False)
    ax_=ax[8,0].twinx()
    ax_.bar(margin1.index,margin1, width=1, color='gray',alpha = 0.2,label='中美利差10年')
    ax_.set_ylim([0,300])
    ax_.legend(ncol=1,loc=1,fontsize=10,frameon=False)
    ax_.set_ylabel('（BP）',fontsize=10)
    ax_.set_title('中美利差:10年', )

    # * 8.1 中美利差:2年
    rates1 = rates.loc[rates['date'] >= '2015-01-04']
    rates1.index = rates1['date']
    rates_us1 = rates_us.loc[rates_us['date'] >= '2015-01-04']
    rates_us1.index = rates_us1['date']
    rates_us1 = rates_us1.dropna()
    #计算利差
    margin2 = (rates1['国债2年']-rates_us1['美债2年']) * 100
    df = pd.DataFrame([rates1['国债2年'],rates_us1['美债2年'],margin2])
    df.index = ['国债2年','美债2年','中美利差2年']
    df  = df.T

    ax[8,1].plot(rates_us1['date'],rates_us1['美债2年'],'#f0833a',label='美债2年')
    ax[8,1].plot(rates1['date'],rates1['国债2年'],'#3778bf',label="国债2年")
    ax[8,1].set_ylabel('（%）',fontsize=10)
    ax[8,1].set_ylim([0,5])
    ax[8,1].legend(ncol=3,loc=2,fontsize=10,frameon=False)
    ax_=ax[8,1].twinx()
    ax_.bar(margin2.index,margin2, width=1, color='gray',alpha = 0.2,label='中美利差2年')
    ax_.set_ylim([-50,500])
    ax_.legend(ncol=1,loc=1,fontsize=10,frameon=False)
    ax_.set_ylabel('（BP）',fontsize=10)
    ax_.set_title('中美利差:2年', )

    # * 9.0 中美利差:1年
    rates1 = rates.loc[rates['date'] >= '2015-01-04']
    rates1.index = rates1['date']
    rates_us1 = rates_us.loc[rates_us['date'] >= '2015-01-04']
    rates_us1.index = rates_us1['date']
    rates_us1 = rates_us1.dropna()
    #计算利差
    margin3 = (rates1['国债1年']-rates_us1['美债1年']) * 100
    df = pd.DataFrame([rates1['国债1年'],rates_us1['美债1年'],margin3])
    df.index = ['国债1年','美债1年','中美利差1年']
    df  = df.T

    ax[9,0].plot(rates_us1['date'],rates_us1['美债1年'],'#f0833a',label='美债1年')
    ax[9,0].plot(rates1['date'],rates1['国债1年'],'#3778bf',label="国债1年")
    ax[9,0].set_ylabel('（%）',fontsize=10)
    ax[9,0].set_ylim([-0.5,5])
    ax[9,0].legend(ncol=3,loc=2,fontsize=10,frameon=False)
    ax_=ax[9,0].twinx()
    ax_.bar(margin3.index,margin3, width=1, color='gray',alpha = 0.2,label='中美利差1年')
    ax_.set_ylim([-50,500])
    ax_.legend(ncol=1,loc=1,fontsize=10,frameon=False)
    ax_.set_ylabel('（BP）',fontsize=10)
    ax_.set_title('中美利差:1年', )

    # * 9.1 中美利差与人民币汇率
    rates_us = do.get_data('rates_us');rates_us.index=rates_us.date
    rates2 = rates.loc[rates['date'] >= '2015-01-04']
    rates2.index = rates2['date']
    rates_us2 = rates_us.loc[rates_us['date'] >= '2015-01-04']
    rates_us2.index = rates_us2['date']
    rates_us2 = rates_us2.dropna()
    #计算利差
    margin4 = ((rates2['国债10年']-rates_us2['美债10年']) * 100).dropna()
    df = pd.DataFrame([rates_us2['美元兑人民币'],margin4])
    df.index = ["美元兑人民币","中美利差10年"]
    df = df.T

    ax[9,1].plot(rates_us2['date'],rates_us2['美元兑人民币'],'#3778bf',label="美元兑人民币")
    ax[9,1].set_ylim([5,8])
    ax[9,1].legend(ncol=3,loc=2,fontsize=10,frameon=False)
    ax_=ax[9,1].twinx()
    ax_.plot(margin4.index,margin4,'#f0833a',label="中美利差10年")
    ax_.set_ylabel('（BP）',fontsize=10)
    ax_.set_title('中美利差与人民币汇率', )
    ax_.set_ylim([0,300])
    ax_.legend(ncol=1,loc=1,fontsize=10,frameon=False)

    # * 10.0 中美市场利差
    cash_cost = do.get_data('cash_cost');cash_cost.index = cash_cost.date
    rates1 = rates.loc[rates['date'] >= '2015-01-01']
    rates1.index = rates1['date']
    rates_us1 = rates_us.loc[rates_us['date'] >= '2015-01-01']
    rates_us1.index = rates_us1['date']
    cash_cost1 = cash_cost.loc[cash_cost['date'] >= '2015-01-01']
    cash_cost1.index = cash_cost1['date']
    #计算利差
    margin5 = (cash_cost1['shibor_3m']-rates_us1['libor_3m']) * 100
    df = pd.DataFrame([rates_us1['libor_3m'],cash_cost1['shibor_3m'],margin5])
    df.index = ["美元libor3个月",'人民币shibor3个月','中美利差1年']
    df  = df.T

    ax[10,0].plot(rates_us1['date'],rates_us1['libor_3m'],'#3778bf',label="美元libor3个月")
    ax[10,0].plot(cash_cost1['date'],cash_cost1['shibor_3m'],'#f0833a',label='人民币shibor3个月')
    ax[10,0].set_ylim([0,8])
    ax[10,0].legend(ncol=3,loc=2,fontsize=10,frameon=False)
    ax[10,0].set_ylabel('（%）',fontsize=10)
    ax_=ax[10,0].twinx()
    ax_.bar(margin5.index,margin5, width=1, color='gray',alpha = 0.2,label='中美利差1年')
    ax_.set_ylabel('（BP）',fontsize=10)
    ax_.set_ylim([0,700])
    ax_.legend(ncol=1,loc=1,fontsize=10,frameon=False)
    ax_.set_title('中美市场利差', )

    # * 10.1 美债期限利差
    rates_us1 = rates_us.loc[rates_us['date'] >= '2015-01-04']
    rates_us1.index = rates_us1['date']
    rates_us1 = rates_us1.dropna()
    margin6 = (rates_us1['美债10年']-rates_us1['美债2年']) * 100    
    df = pd.DataFrame([rates_us1['美债10年'],rates_us1['美债2年'],margin6])
    df.index = ["美债10年",'美债2年','美债10-2年']
    df  = df.T

    ax[10,1].plot(rates_us1['date'],rates_us1['美债10年'],'#3778bf',label="美债10年")
    ax[10,1].plot(rates_us1['date'],rates_us1['美债2年'],'#f0833a',label="美债2年")
    ax[10,1].set_ylim([0,4.5])
    ax[10,1].legend(ncol=3,loc=2,fontsize=10,frameon=False)
    ax[10,1].set_ylabel('（%）',fontsize=10)
    ax_=ax[10,1].twinx()
    ax_.bar(margin6.index,margin6, width=1, color='gray',alpha = 0.2,label='美债10-2年')
    ax_.set_ylabel('（BP）',fontsize=10)
    ax_.set_ylim([0,400])
    ax_.legend(ncol=1,loc=1,fontsize=10,frameon=False)
    ax[10,1].set_title('美债期限利差', )

    # * 11.0 国债期限利差 30-10/10-1
    gz_term_spread = pd.DataFrame()
    gz_term_spread['国债30-10'] = rates['国债30年'] - rates['国债10年']
    gz_term_spread['国债10-1'] = rates['国债10年'] - rates['国债1年']
    
    gz_term_spread['2015':].plot(ax=ax[11,0])
    ax[11,0].legend(ncol=2,loc='upper center',fontsize=10,frameon=False)
    ax[11,0].set_title('国债期限利差')
    ax[11,0].set_xlabel('')
    
    # * 11.1 国开期限利差 10-1/3-1
    gk_term_spread = pd.DataFrame()
    gk_term_spread['国开10-1'] = rates['国开10年'] - rates['国开1年']
    gk_term_spread['国开3-1'] = rates['国开3年'] - rates['国开1年']
    
    gk_term_spread['2015':].plot(ax=ax[11,1])
    ax[11,1].legend(ncol=2,loc='upper center',fontsize=10,frameon=False)
    ax[11,1].set_title('国开债期限利差')
    ax[11,1].set_xlabel('')
    
    plt.suptitle('利差情况',fontsize=24,y=1.01)
    fig.tight_layout()
    
    
    return fig

def fig_fcts():
    rates = do.get_data('rates'); rates.index = rates.date
    dur = do.get_data('fund_duration'); dur.index = dur.date; 
    dur.drop('date',axis=1, inplace=True)
    
    from signals.senti import cal_senti_indices
    df_senti = do.get_data('factor_senti'); df_senti.index = df_senti.date
    _days  = do.get_ex_days()
    _days = df_senti.index & _days
    
    df_senti_score_5 = cal_senti_indices(
        df_senti.loc[_days].fillna(method='ffill'), 5)
    df_senti_score_20 = cal_senti_indices(
        df_senti.loc[_days].fillna(method='ffill'), 20)
    
    from signals.senti import cal_liquid_indice
    df_lqd = do.get_data('factor_lqd'); df_lqd.index = df_lqd.date
    df_lqd_score_5 = cal_liquid_indice(df_lqd.loc[_days], 5)
    df_lqd_score_20 = cal_liquid_indice(df_lqd.loc[_days], 20)
    
    # @@ ploting
    plt.style.use({'font.size' : 12}) 
    fig,ax = plt.subplots(ncols=2,nrows=10,figsize=(6*2,4*10), dpi=300)
    
    df_senti_score_5['交易动能得分']['2021-09':].plot.area(
        ax=ax[0,0],stacked=False,title='交易动能得分(级别：周)')
    ax[0,0].grid(linestyle = '--',linewidth =1, color= 'gray',alpha = 0.4,axis='x') 
    df_lqd_score_5['资金面得分']['2021-09':].plot.area(
        ax=ax[0,1],stacked=False,title='资金面得分(级别：周)')
    ax[0,1].grid(linestyle = '--',linewidth =1, color= 'gray',alpha = 0.4,axis='x') 
    
    import talib as ta
    ta.MA(df_senti['gz30'].dropna(),20).plot(ax=ax[1,0],label='gz30Y_turn')
    ta.MA(df_senti['gz30'].dropna(),20)['2021':].plot(ax=ax[1,1],label='gz30Y_turn')
    ta.MA(df_senti['gk10_top3'].dropna(),20).plot(ax=ax[2,0],label='gk10Y_turn')
    ta.MA(df_senti['gk10_top3'].dropna(),5)['2021':].plot(ax=ax[2,1],label='gk10Y_turn')
    ax[1,0].legend(loc='upper left',frameon=False);ax[1,1].legend(loc='upper left',frameon=False)
    ax[2,0].legend(loc='upper left',frameon=False);ax[2,1].legend(loc='upper left',frameon=False)

    # lev
    # TODO 月度修改
    ax[3,0].plot(df_lqd.lev['2022-03'].tolist(),label='3月')
    ax[3,0].plot(df_lqd.lev['2022-04'].tolist(),label='4月')
    ax[3,0].plot(df_lqd.lev['2022-05'].tolist(),label='5月')
    df_lqd.lev['2021-09':].rolling(5).mean().plot(
        ax=ax[3,1],title='银行间杠杆率(MA5)')
    
    ## duration
    dur.median(axis=1)['2021':].plot(ax=ax[4,0],
                                      alpha=0.6,label='久期')
    do.LLT(dur.median(axis=1),10)['2021':].plot(ax=ax[4,0],title='基金久期中位数(10日平滑)')
    
    do.LLT(dur[dur>0].diff(1).std(axis=1),10)['2021-01':].plot(ax=ax[4,1],\
        title='基金久期分歧指数(10日平滑)')
    
    do.LLT(dur.quantile(0.9,axis=1),10)['2021'].plot(ax=ax[5,0])
    do.LLT(dur.quantile(0.5,axis=1),10)['2021'].plot(ax=ax[5,0])
    do.LLT(dur.quantile(0.1,axis=1),10)['2021'].plot(ax=ax[5,0])
    

    ((dur >= dur.rolling(250).quantile(0.90)).sum(axis=1)/dur.count(axis=1))['2021':].\
        plot(label='久期90%分位数以上产品占比',ax=ax[5,1])
    
    ax[3,0].legend(loc='upper center',ncol=3, frameon=False)
    ax[5,0].legend(['90%','50%','10%',],loc='best',ncol=3,frameon=False)
    ax[5,1].legend(loc='best',ncol=1, frameon=False)
    ax[3,0].set_title('银行间杠杆率近3月对比')
    ax[3,0].set_xlabel('交易日')
    
    ax[1,0].set_title('30Y国债换手率(20-30Y),MA20');ax[1,0].set_ylabel('%')
    ax[2,0].set_title('10Y国开换手率(top3活跃券),MA20');ax[2,0].set_ylabel('%')
    ax[1,1].set_title('30Y国债换手,MA20')
    ax[2,1].set_title('10Y国开换手,MA5')
    
    ax_ = ax[1,0].twinx()
    rates.loc[df_senti[['gz30']].dropna().rolling(20).mean().index[0]:
              ,['国债30年']].plot(
                  ax=ax_,color='red',alpha=0.6,ylabel='%')
    ax_.legend(loc='upper right',frameon=False)
    ax_ = ax[1,1].twinx()
    rates.loc[df_senti[['gz30']].dropna().rolling(20).mean()['2021'].index[0]:
              ,['国债30年']].plot(
                  ax=ax_,color='red',alpha=0.6,ylabel='%',ls='--')
    ax_.legend(loc='upper right',frameon=False)
    
    ax_ = ax[2,0].twinx()
    rates.loc[df_senti[['gk10_top3']].dropna().rolling(20).mean().index[0]:
              ,['国开10年']].plot(
                  ax=ax_,color='red',alpha=0.6,ylabel='%')
    ax_.legend(loc='upper right',frameon=False)
    ax_ = ax[2,1].twinx()
    rates.loc[df_senti[['gk10_top3']].dropna().rolling(5).mean()['2021'].index[0]:
              ,['国债10年']].plot(
                  ax=ax_,color='red',alpha=0.6,ylabel='%',ls='--')
    ax_.legend(loc='upper right',frameon=False)
    
    ax[5,0].set_title('市场基金久期分位数')
    ax[5,1].set_title('极端久期基金数量占比')
    
    ## spr corr
    ax[6,0].bar(df_senti.corr5['2021-09':].index,df_senti.corr5['2021-09':])
    ax[6,0].set_title('国开债期限偏好指数(周)',fontsize=16)
    do.set_axes_rotation(ax[6,0],30)
    ax[6,1].bar(df_senti.corr20['2021-09':].index,df_senti.corr20['2021-09':])
    ax[6,1].set_title('国开债期限偏好指数(月)',fontsize=16)
    do.set_axes_rotation(ax[6,1],30)
    
    # net dur
    from fig_func import jjgs_net_buy
    ax[8,0] = jjgs_net_buy(ax[8,0], kind = 'all' , rol=5,
                           se=do.LLT(df_senti['net_dur_all'],5)['2021':])
    ax[7,1] = jjgs_net_buy(ax[7,1], kind = 'cre' , rol=10,
                           se=do.LLT(df_senti['net_dur'],10)['2021':])
    ax[7,0] = jjgs_net_buy(ax[7,0], kind = 'cre' , rol=1,
                           se=df_senti['net_dur']['2021':])
                           
    fig.delaxes(ax[8,1])
    
    ## 月度动能
    df_senti_score_20['交易动能得分']['2021-09':].plot.area(
        ax=ax[9,0],stacked=False,title='交易动能得分(级别：月)')
    ax[9,0].grid(linestyle = '--',linewidth =1, color= 'gray',alpha = 0.4,axis='x') 
    df_lqd_score_20['资金面得分']['2021-09':].plot.area(
        ax=ax[9,1],stacked=False,title='资金面得分(级别：月)')
    ax[9,1].grid(linestyle = '--',linewidth =1, color= 'gray',alpha = 0.4,axis='x') 
    
    fig.suptitle('微观指标',fontsize=24,y=1.01)
    fig.tight_layout()
    
    
    return fig
  
def fig_cb():
    
    ## CB
    
    fig, ax = plt.subplots(nrows=2,ncols=2,figsize = (12,4*2), dpi=100)
    
    df_cb = do.get_data('Factor_cb'); df_cb.index= df_cb.date
    ax[0,0].plot(df_cb.loc['2021':,'bmk'])
    ax[0,0].set_title('可转债市场-等权指数')
    ax[0,1].plot(df_cb.loc['2021':,'amt'])
    ax[0,1].set_title('市场总成交额')
    ax[1,0].plot(df_cb.loc['2021':,'convp'])
    ax[1,0].set_title('市场百元溢价率')
    ax[1,1].plot(df_cb.loc['2021':,'convp_big'], label='大品种')
    ax[1,1].plot(df_cb.loc['2021':,'convp_small'], label='小品种')
    ax[1,1].legend(frameon=False)
    ax[1,1].set_title('市场百元溢价率（大品种/小品种）')
    
    do.set_axes_rotation(ax[0,0],30)
    do.set_axes_rotation(ax[0,1],30)
    do.set_axes_rotation(ax[1,1],30)
    do.set_axes_rotation(ax[1,0],30)
    
    fig.suptitle('可转债市场', fontsize=24)
    fig.tight_layout()
    
    return fig
   
def fig_strat():
    
    from rate.sigs_strat import rsj_strat, kdj_strat
    from rate.sigs_strat_inday import strat_factor_q
    import rate.factor_model.models as mdl
    
    df_5m = do.get_data('t10_5m'); df_5m.index = df_5m.date
    rsj = ti.get_rsj(df_5m)['rsj']; 
    df = do.get_data('t10_1d'); df.index = df.date
    
    fig, ax = plt.subplots(nrows=4,ncols=2,figsize = (12,4*4), dpi=300)
    ## RSJ-strat1
    rsj6 = rsj.rolling(6).mean()
    rsj16 = rsj.rolling(16).mean()
    rsj6['2022':].plot(label = 'RSJ-MA6',ax=ax[0,0])
    rsj16['2022':].plot(label = 'RSJ-MA16',ax=ax[0,0])
    ax[0,0].axhline(y=rsj6.quantile(0.84),ls='--',c='r'); 
    ax[0,0].axhline(y=rsj6.quantile(0.23),ls='--',c='r')
    ax[0,0].legend(fontsize=12,loc='upper right')
    ax[0,0].set_title('RSJ双均线复合策略',fontsize=16)
    ## strat1-signal
    s = rsj_strat(6,16, 0.23, 0.84, pltt = 0, stop_type = 0, rtn_df=1);
    idxs_1 = s.loc[(s.typ_==1)&(s.typ_.shift(1)!=1)]['2022'].index
    idxs_2 = s.loc[(s.typ_==-1)&(s.typ_.shift(1)!=-1)]['2022'].index
    df.close['2022'].plot(ax=ax[0,1],alpha=0.8)
    ax[0,1].scatter(idxs_1 , df.loc[idxs_1,'close'], c='r',marker='^',s=60)
    ax[0,1].scatter(idxs_2 , df.loc[idxs_2,'close'], c='green',marker='v',s=60)
    ax[0,1].set_title('RSJ双均线复合策略: 多空信号情况',fontsize=16)
    
    ## RSJ-strat2
    f = ta.EMA(rsj, 7)
    date = f['2022'].index.strftime('%m-%d')
    ax[1,0].bar(date, f['2022':],label='RSJ - EMA7')
    ax[1,0].set_xticks([date[i] for i in range(0,len(date),8)])
    ax[1,0].axhline(y=f.quantile(0.2),c='red')
    ax[1,0].axhline(y=f.quantile(0.8),c='green')
    ax[1,0].set_title('RSJ反转策略')
    ax[1,0].legend(fontsize=12,loc='upper right')
    do.set_axes_rotation(ax[1,0] , 30)
    ## strat2-signal
    # s = strat_factor_q(df=df,f=f,up=0.2,up_out=0.8,pltt=0)
    s = mdl.get_ensemble_strat('rsj_7', -1 ,start='2018',_q=0.5)[0]
    s['typ_'] = s['typ_'].fillna(method='ffill')
    idxs_1 = s.loc[(s.typ_==1)&(s.typ_.shift(1)!=1)]['2022'].index
    idxs_2 = s.loc[(s.typ_==-1)&(s.typ_.shift(1)!=-1)]['2022'].index
    df.close['2022'].plot(ax=ax[1,1],alpha=0.8)
    ax[1,1].scatter(idxs_1 , df.loc[idxs_1,'close'], c='r',marker='^',s=60)
    ax[1,1].scatter(idxs_2 , df.loc[idxs_2,'close'], c='green',marker='v',s=60)
    ax[1,1].set_title('RSJ反转策略: 多空信号情况',fontsize=16)
    
    ##KDJ-strat
    s_kdj = kdj_strat(9,3, 0.2, 0.8, stop_type = 1, rtn_df=1);
    ## KDJ-strat
    k = s_kdj['k']*100; d = s_kdj['d']*100
    k['2022':].plot(label = 'K',ax=ax[2,0])
    d['2022':].plot(label = 'D',ax=ax[2,0])
    ax[2,0].axhline(y=20,ls='--',c='r'); ax[2,0].axhline(y=80,ls='--',c='r')
    ax[2,0].legend(fontsize=12,loc='lower left')
    ax[2,0].set_title('KDJ策略 (参数:9,3,3)',fontsize=16)
    ## kdj-signal
    s = s_kdj.fillna(method='ffill')
    idxs_1 = s.loc[(s.typ_==1)&(s.typ_.shift(1)!=1)]['2022'].index
    idxs_2 = s.loc[(s.typ_==-1)&(s.typ_.shift(1)!=-1)]['2022'].index
    df.close['2022'].plot(ax=ax[2,1],alpha=0.8)
    ax[2,1].scatter(idxs_1 , df.loc[idxs_1,'close'], c='r',marker='^',s=60)
    ax[2,1].scatter(idxs_2 , df.loc[idxs_2,'close'], c='green',marker='v',s=60)
    ax[2,1].set_title('KDJ策略: 多空信号情况',fontsize=16)
    
    
    ##reverse-strat
    s = mdl.strat_reverse()
    ## typ-of-strat
    s.typ_mean['2022':].plot(label = '',ax=ax[3,0])
    ax[3,0].axhline(y=0.5,ls='--',c='r'); ax[3,0].axhline(y=-0.5,ls='--',c='green')
    # ax[3,0].legend(fontsize=12,loc='lower left')
    ax[3,0].set_title('CTA反转多因子策略(加权信号)',fontsize=16)
    ## kdj-signal
    s = s.fillna(method='ffill')
    idxs_1 = s.loc[(s.typ_==1)&(s.typ_.shift(1)!=1)]['2022'].index
    idxs_2 = s.loc[(s.typ_==-1)&(s.typ_.shift(1)!=-1)]['2022'].index
    df.close['2022'].plot(ax=ax[3,1],alpha=0.8)
    ax[3,1].scatter(idxs_1 , df.loc[idxs_1,'close'], c='r',marker='^',s=60)
    ax[3,1].scatter(idxs_2 , df.loc[idxs_2,'close'], c='green',marker='v',s=60)
    ax[3,1].set_title('CTA反转多因子策略: 多空信号情况',fontsize=16)
    
    
    
    ax[0,0].set_xlabel('');ax[0,1].set_xlabel('')
    ax[1,0].set_xlabel('');ax[1,1].set_xlabel('')
    ax[2,0].set_xlabel('');ax[2,1].set_xlabel('')
    ax[3,0].set_xlabel('');ax[3,1].set_xlabel('')
    
    fig.suptitle('交易策略', fontsize=24)
    fig.tight_layout()
    
    return fig
     

def get_micro_pdf():
    
    from matplotlib.backends.backend_pdf import PdfPages
    pdf_micro = PdfPages('/Users/wdt/Desktop/tpy/报告输出/研究图表/微观指标与策略.pdf')
    for pic in [fig_fcts(),fig_strat(),fig_cb()]:
        pdf_micro.savefig(pic,bbox_inches='tight')
        plt.close()
    pdf_micro.close()
    
    return 
    
    
    
if __name__ == '__main__':
    print('正在打印')
    
    # 设置市场利率水平的结束日
    hb_base = dt.datetime(2021,9,2)
    end_day = dt.datetime(2021,10,9)
    
    cash = cash_fig()
    cash.savefig('流动性指标.pd_micro',dpi=300,bbox_inches='tight')

    ratelevel= rate_level_fig(hb_base,end_day)
    ratelevel.savefig('市场利率水平.pdf',dpi=300,bbox_inches='tight')

    ratediff = rate_diff_fig()
    ratediff.savefig('利差水平.pdf',dpi=300,bbox_inches='tight')

    # signals = fig_fcts()
    # signals.savefig('补充.pdf',dpi=300,bbox_inches='tight')
    get_micro_pdf()


