import pandas as pd
import numpy as np
import data_organize as do
import matplotlib.pyplot as plt
%matplotlib inline
plt.style.use({'figure.figsize':(10, 4)})



def Factor_lqd():
    ##* lqd
    name = 'factor_lqd'
    print(name+'最后更新于', do.get_latest_date(name).date())
    from signals.senti import lqd_to_db
    lqd_to_db()
    print(name+'已更新至', do.get_latest_date(name).date())
    
    ##* dur
    name = 'fund_duration'
    print(name+'最后更新于', do.get_latest_date(name).date())
    from signals.duration import update_dur
    update_dur(end_day='2022-02-15')
    print(name+'已更新至', do.get_latest_date(name).date())
    ##* senti
    name = 'factor_senti'
    print(name+'最后更新于', do.get_latest_date(name).date())
    from signals.senti import senti_to_db
    senti_to_db()
    print(name+'已更新至', do.get_latest_date(name).date())
    
    

    

def Factor_cb():
    
    import convBond.cb_mkt_convprem as cb_mkt
    import convBond.cb_strat as cbs
    from convBond.db_process import obj_cb
    obj = obj_cb()
    
    # * 等权指数bmk
    bmk = cbs.frameStrategy(obj, start='2017/12/29',
            selMethod = cbs._Var_byd_Thre('amt',0), 
            roundMethod='daily').NAV
    cbs.strategyEvaluation(bmk)
    # * 市场百元溢价率
    convp = cb_mkt.cal_convp_index(obj ,start='2017-12-29',dropW=True)
    convp['y']['2021':].plot()
    # * amt
    amt = (obj.DB['amt'].sum(axis=1)/100000000)['2021':]
    (obj.DB['amt'].sum(axis=1)/100000000)['2021':].plot()

    df= pd.concat([bmk, convp['y'], amt,], axis=1)
    cols = ['bmk', 'convp', 'amt',]
    df.columns = cols
    from sqlalchemy.types import Float, DateTime
    df['date'] = df.index

    cols_typ = [Float() for _ in range(len(cols))] + [DateTime()]
    dtypelist = dict(zip(df.columns, cols_typ))

    do.upload_data(df, 'Factor_cb', dtypelist, method='replace')
  
