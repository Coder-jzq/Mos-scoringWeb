import json
import numpy as np
from scipy.linalg import solve
from scipy.stats import t
# 计算mos分数
def calc_mos(data):
    '''
    计算MOS，data为MxN的列表，M个句子，N个试听人，内容为每个试听的得分
    :param data:
    :return:
    '''

    data = data.astype(np.float64)
    mu = np.mean(data)
    var_uw = (np.std(data, axis=1) ** 2).mean()
    var_su = (np.std(data, axis=0) ** 2).mean()
    mos_data = data.flatten()
    mos_data = mos_data[~np.isnan(mos_data)]
    var_swu = mos_data.std() ** 2

    x = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 1]])
    y = np.array([var_uw, var_su, var_swu])
    [var_s, var_w, var_u] = solve(x, y)
    M = min(data.shape)
    N = min(data.shape)
    var_mu = var_s / M + var_w / N + var_u / (M * N)
    df = min(M, N) - 1  # 可以不减1
    t_interval = t.ppf(0.95, df, loc=0, scale=1)  # t分布的95%置信区间临界值
    interval = t_interval * np.sqrt(var_mu)
    print('MOS的95%置信区间为：{} +—{}'.format(round(float(mu), 3), round(interval, 3)))
    return 'MOS的95%置信区间为：{} +—{}'.format(round(float(mu), 3), round(interval, 3))


# 存储打分人姓名
names = ['xx', 'xx', 'xxx', 'xx', 'xx', 'xx', 'xx',  'xx', 'xx', 'xx', 'xx']


"""
    我们要遍历每个人的打分， 把相同模型的  (每个人对不同话语的评分)：   [模型, 人, 话语分数]
"""

mos_list_n = []
mos_list_e = []

for name in names: # 遍历每个人的名字

    # 读取 JSON 文件，指定编码格式为 utf-8
    with open(name + '.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 打印读取的数据
    # print(data)

    # 获取一个人的[每句话，每个模型]的流畅度分数
    list_n = []
    # 获取一个人的[每句话，每个模型]的重音感知分数
    list_e = []
    # 遍历每句话
    for item in data:
        # 遍历每个 句话每个模型的 分数
        u_t = item['tableData']
        u_list_n = []
        u_list_e = []

        for model in u_t:
            # 添加到列表里
            u_list_n.append(model['scores1'])
            u_list_e.append(model['scores2'])


        list_n.append(u_list_n)
        list_e.append(u_list_e)


    # 行列 转换  (可以转换为  一个人对（模型，每句话）)
    list_n = np.array(list_n)
    list_e = np.array(list_e)
    list_n_t = list_n.T
    list_e_t = list_e.T


    # 添加进去(结构[人,模型, 句子])
    mos_list_n.append(list_n_t)
    mos_list_e.append(list_e_t)

mos_list_n = np.stack(mos_list_n)
mos_list_e = np.stack(mos_list_e)

# 转置为 (模型，人，句子)的维度
mos_list_n = np.transpose(mos_list_n, (1, 0, 2))  # 将第1个维度与第2个维度交换位置
mos_list_e = np.transpose(mos_list_e, (1, 0, 2))  # 将第1个维度与第2个维度交换位置


# 计算mos分数
print("----------------------------------------n-dmos----------------------------------------")
for i in range(mos_list_n.shape[0]):
    calc_mos(mos_list_n[i])
print("----------------------------------------e-dmos----------------------------------------")
for i in range(mos_list_e.shape[0]):
    calc_mos(mos_list_e[i])