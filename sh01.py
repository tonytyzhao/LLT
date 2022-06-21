import baostock as bs
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math


def GetSh01Data():
    # 登陆系统
    lg = bs.login()
    rs = bs.query_history_k_data_plus("sh.000001", "close", start_date='2012-10-26', end_date='2013-04-09', frequency="d")

    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    
    result = pd.DataFrame(data_list, columns=rs.fields)
    result['close']=result['close'].astype(float)
    bs.logout()
    return result

def price(x):
    return result.at[x, 'close']

result = GetSh01Data()
N = len(result)
llt = np.zeros((N,1), dtype = float) 
llt[0][0] = price(0)
llt[1][0] = price(1)
alpha = 0.05

def DrawPd(data_frame):
    data_frame.plot()
    plt.show()

def e(x):
    return llt[x][0]

if __name__ == '__main__':
    for t in range(2,N):
        p_t = (alpha - math.pow(alpha,2)/4)*price(t)
        p_t_sub_1 = (math.pow(alpha,2)/2)*price(t-1)
        p_t_sub_2 = (alpha - 3*math.pow(alpha,2)/4)*price(t-2)
        e_t_sub_1 = 2*(1-alpha)*e(t-1)
        e_t_sub_2 = math.pow((1-alpha),2)*e(t-2)
        llt[t][0] = p_t + p_t_sub_1 - p_t_sub_2 + e_t_sub_1 - e_t_sub_2

    llt = pd.DataFrame(llt)
    # print(llt)
    # print(result)
    df_inner = pd.concat([result,llt],axis=1,join='inner')
    df_inner.columns = ['close','llt']
    print(df_inner)
    DrawPd(df_inner)
    print()