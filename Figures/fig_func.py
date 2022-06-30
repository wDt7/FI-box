import numpy as np
import pandas as pd
import data_organize as do
import matplotlib.pyplot as plt
import datetime as dt
from dateutil.relativedelta import relativedelta


def gk_new_old(axes):
    # 国开10新老债利差 近n对 
    #!需要手动调整
    data = do.get_data('gk10_yield')
    data.index = data.date
    
    (data['220205.IB'] - data['220210.IB'])\
        [:].plot(ax=axes,
            ls='--',label = '220205-220210')
    
    (data['210215.IB'] - data['220205.IB'])\
        [:'2022-04'].plot(ax=axes,
            ls='--',label = '210215-220205')
        
    (data['210210.IB'] - data['210215.IB'])\
        [:'2022-01'].plot(ax=axes,
            ls='--',label = '210210-210215')   
          
    axes.legend(fontsize=10,ncol=1,frameon=False,loc='best')
    return axes

def rate_change(axes, base , end ,kind='gz'):
    # * 利率变动的bar图
    # * gz/gk（可选）；base 可设置
    ## gz
    df = do.get_data('rates'); df.index=df.date
    if kind == 'gz':
        name = '国债'
    else:
        name = '国开'
    m = [ '6月', '1年', '3年', '5年','7年', '10年']
    l = [name+x for x in m]
    d = pd.DataFrame([],columns=range(6))
    d.loc[base] = df.loc[base,l].tolist()
    d.loc[end] = df.loc[end,l].tolist()
    d.loc['期间变动(BP)'] =( d.loc[end]-d.loc[base] )*100
    ## plott
    t=axes.bar(d.columns, d.loc['期间变动(BP)'],color='lightgrey',width=0.45)
    axes.bar_label(t,label_type='edge')
    ax_=axes.twinx()
    d.loc[end].plot(ax=ax_,marker='o',color='#3778bf')
    d.loc[base].plot(ax=ax_,marker='o',color='#f0833a')
    axes.set_xticks(d.columns)
    # d.columns = ['6M','1Y','3Y','5Y','7Y','10Y']
    axes.set_xticklabels(['6M','1Y','3Y','5Y','7Y','10Y'],rotation=0)
    axes.set_title(name+'收益率变动')
    ax_.legend([end.date(),base.date()],loc='lower right',\
        ncol=2,fontsize=10,frameon=False,)
    ax_.set_ylabel('(%)',fontsize=10)
    axes.set_ylabel('期间变动(BP)',fontsize=10)
    axes.set_ylim([d.loc['期间变动(BP)'].min()-6,
                      d.loc['期间变动(BP)'].max()+6])
    
    return axes
    
def credit_change(axes, grade ,base,end_day):
    df = do.get_data('rates'); df.index=df.date
    
    # * 信用bp变动
    end = end_day #df['2021'].index[-1]
    ## gz
    name = '城投'+'_'+ grade +'_' 
    m = [  '1y', '3y', '5y','7y', ]
    l = [name+x for x in m]
    d = pd.DataFrame([],columns=range(4))
    d.loc[base] = df.loc[base,l].tolist()
    d.loc[end] = df.loc[end,l].tolist()
    d.loc['期间变动(BP)'] =( d.loc[end]-d.loc[base] )*100
    ## plott
    t=axes.bar(d.columns , d.loc['期间变动(BP)'],color='lightgrey',width=0.5)
    axes.bar_label(t,label_type='edge')
    ax_=axes.twinx()
    d.loc[end].plot(ax=ax_,marker='o',color='#3778bf')
    d.loc[base].plot(ax=ax_,marker='o',color='#f0833a')
    axes.set_xticks(d.columns)
    axes.set_xticklabels(m,rotation=0)
    axes.set_title(name+'收益率变动（月度）')
    ax_.legend([end.date(),base.date()],
               loc='best',\
        ncol=1,fontsize=10,frameon=False,)
    ax_.set_ylabel('(%)',fontsize=10)
    axes.set_ylabel('期间变动(BP)',fontsize=10)
    axes.set_ylim([d.loc['期间变动(BP)'].min()-5,d.loc['期间变动(BP)'].max()+5])
    return axes

def credit_curve(axes, grade,end_day):
    df = do.get_data('rates'); df.index=df.date
    
    # * 信用债收益率曲线变动
    ## 选取对比日期
    today = end_day; base = df['2021':'2021'].index[-1]
    # 城投债
    name = '城投'+'_'+ grade +'_' 

    m = [  '1y', '3y', '5y','7y', ]

    l = [name+x for x in m]
    d = pd.DataFrame(columns=[0,1,2,4])
    d.loc[today] = df.loc[today,l].tolist()
    d.loc[base.date()] = df.loc[base,l].tolist()
    d.loc['25分位数'] = [np.quantile(df[x]['2015':],0.25) for x in l]
    d.loc['75分位数'] = [np.quantile(df[x]['2015':],0.75) for x in l]
    d.loc['中位数'] = [np.quantile(df[x]['2015':],0.5) for x in l]
    #plot 
    d.loc[today].plot(ax=axes,
        label='现值('+today.strftime('%Y%m%d')+')',\
        marker='o',color='#3778bf')
    d.loc[base.date()].plot(ax=axes,
                color='#f0833a',label='2021年底',marker='s')
    d.loc['25分位数'].plot(ax=axes,ls='--',color='lightgrey',alpha=1)
    d.loc['75分位数'].plot(ax=axes,ls='--',color='lightgrey',alpha=1)
    d.loc['中位数'].plot(ax=axes,color='orange',alpha=0.3)
    # ax.set_ylim([1.5,4.5])
    axes.set_xticks([0,1,2,4])
    axes.set_xticklabels(m)
    axes.legend(ncol=2,loc='best',frameon=False,fontsize=10)
    axes.set_title(name+'到期收益率曲线(2015以来)')
    axes.set_ylabel('(%)',fontsize=10)
    return axes
    
def jjgs_net_buy(axes, kind = 'cre',rol = 5,se=None):
    # 基金公司及产品 交易久期 
    # 可选择 信用/全品种 
    start = '2021'
    
    if se is None:
        rates = do.get_data('rates'); rates.index = rates.date
        data = do.get_data('Net_buy_bond')
        data.index = data.date
        term_list = data['期限'].unique()
        
        name = '基金公司及产品' 
        # name = '理财子公司及理财类产品'
        # name = '农村金融机构'
        df_jj = data.loc[data['机构名称']==name]
        df_jj = df_jj.loc[df_jj.date!='2020-10-20']
        df_jj = df_jj.fillna(0)
        
        stat = pd.DataFrame(index = df_jj.index.unique(),
                        columns=term_list)
        for idx in stat.index:
            stat.loc[idx] = df_jj.loc[idx,kind_list].sum(axis=1).tolist()
        stat = stat.loc[stat['合计']!=0]
        stat['factor'] = stat.rolling(rol).mean().dot([1,3,5,7,10,0,0,0,0,0])
        stat['r'] = (-1)*rates['国债10年']
        
    else:
        rates = do.get_data('rates'); rates.index = rates.date
        stat = pd.DataFrame([])
        stat['factor'] = se
        stat['r'] = (-1)*rates['国债10年']
        
    
    if kind == 'cre':   
        kind_list = ['中期票据','短期/超短期融资券','企业债']
        lab = '信用品种净买入按期限加权：MA{}'.format(rol)
    elif kind == 'all':
        kind_list = ['中期票据','短期/超短期融资券','企业债','同业存单',
                     '国债-新债', '国债-老债', 
                     '政策性金融债-新债', '政策性金融债-老债']
        lab = '全品种净买入按期限加权：MA{}'.format(rol)
    elif kind == 'rate':
        kind_list = ['国债-新债', '国债-老债', 
                     '政策性金融债-新债', '政策性金融债-老债']
        lab = '利率品种净买入按期限加权：MA{}'.format(rol)
    
    
    stat.factor[start:].plot(ax=axes,
        label=lab)
    axes.legend(loc='upper left',frameon=False)
    ax_=axes.twinx()
    stat.r[start:].plot(c='r',label='国债10年(逆序)',ax=ax_,ls='--')
    ax_.legend(loc = 'lower right',frameon=False)
    axes.set_title('基金公司交易久期(基于净买卖数据)',fontsize=16)
    
    return axes



if __name__ == '__main__':
    fig,ax = plt.subplots(nrows=1,ncols=1)
    ax = gk_new_old(ax)
    fig



def new_gk_old():
    # 国开新老债自动识别
    # 有问题 暂存
    gk10_yield = do.get_data('gk10_yield')
    gk10_yield.index = gk10_yield['date']
    gk10_yield = gk10_yield.loc[(gk10_yield.index >= '20180102')]
    
    #提取成交量数据
    df = pd.read_excel('/Users/wdt/Desktop/tpy/Signals/个券成交量/zj_all.xlsx',\
        index_col = 0)
    
    #提取10年国开债
    list = []
    for i in gk10_yield.columns[:-1]:
        a = df.loc[df.index == i]
        list.append(a)
        df_v = pd.concat(list,axis=0)
        df_v = df_v.fillna(0)
        df_v = df_v.T
        df_v = df_v.sort_index()
        df_v = df_v.loc[(df_v.index >= '20180102')]
        
    #判断活跃券
    list = []
    for i in range(len(df_v)):
        a = df_v.iloc[i,].values.tolist()
        a = df_v.columns[a.index(max(a))]
        list.append(a)
    df_bond = pd.DataFrame(list, columns=['活跃券'])
    df_bond.index = df_v.index
        
    #活跃券利率
    list1 = []
    for i in range(len(df_bond)):        
        a = gk10_yield[df_bond['活跃券'][i]][i]
        list1.append(a)       
    df_rate_new = pd.DataFrame(list1, columns=['rate_new'])
    df_rate_new.index = df_bond.index
        
    #判断老券
    df_bond['老券'] = ''
    df_bond['老券'][0] = '110226.IB'
    for i in range(len(df_bond)-1):
        if df_bond['活跃券'][i] == df_bond['活跃券'][i+1]:
            df_bond['老券'][i+1] = df_bond['老券'][i]
        else:
            df_bond['老券'][i+1] = df_bond['活跃券'][i]
            
    #老券利率
    list2 = []
    for i in range(len(df_bond)):        
        b = gk10_yield[df_bond['老券'][i]][i]
        list2.append(b)       
    df_rate_old = pd.DataFrame(list2, columns=['rate_old'])
    df_rate_old.index = df_bond.index
        
    #国开债新老券利差
    df_rate_spread = (df_rate_old['rate_old'] - df_rate_new['rate_new'])*100
          
    return df_rate_new, df_rate_old, df_rate_spread, df_bond


