# -*- coding: utf-8 -*- 

##############################################
# 计算如何给小孩子们发红包的程序~
##############################################

# 条件：
# 1. 小孩的个数 children_count 为变量
# 2. 小孩的平均金额为定值（例如50）
# 3. 每一个红包的纸币张数必须完全相等
# 4. 每一个红包的金额尽可能的平均分布
# 功能：
# 1. 输入小孩的个数，得到所需纸币数量最少的红包纸币方案的列表
# 2. 计算出在聚会次数不一定时，我过年时需要去银行取的各种纸币的最大张数~

Enum_Money_1 = 1
Enum_Money_5 = 5
Enum_Money_10 = 10
Enum_Money_20 = 20
Enum_Money_50 = 50
Enum_Money_100 = 100
Money_All = [
	Enum_Money_1, 
	Enum_Money_5, 
	Enum_Money_10,
	Enum_Money_20,
	Enum_Money_50,
	Enum_Money_100,
];
Money_All_R = Money_All[::-1]

g_pocket_min = 10
g_pocket_max = 100

# 允许的误差值
g_money_error = 3;

# 计算红包方案的递归函数
def _GetCountListRecur( money_left, cur_count_left, cur_loop_idx):
	'''
	@param money: 钱的总数
	@param count: 张数
	@return: [[], ] 解决方案列表，为空表示无解

	算法：
	从大钱到小钱，依次遍历其所有可能的张数（小钱的最大张数由循环内的大钱的张数决定）；
	如果找到一个数目恰好可以的，那么加入解决方案列表。
	'''
	if cur_count_left == 0 and money_left == 0:
		return [[], ]
	elif cur_loop_idx == len(Money_All_R)-1:
		if abs(money_left - cur_count_left * Money_All_R[cur_loop_idx]) <= g_money_error:
			return [[cur_count_left, ], ]
		else:
			return []

	result_list = []

	money_type = Money_All_R[cur_loop_idx]
	max_count = money_left // money_type
	for guess_count in range(min(max_count, cur_count_left)+1):
		next_money_left = money_left - money_type * guess_count;
		next_count_left = cur_count_left - guess_count;
		for next_result in _GetCountListRecur(next_money_left, next_count_left, cur_loop_idx+1):
			result_list.append([guess_count, ] + next_result)

	return result_list;

# 计算所有红包方案的列表
def GetCountList( moneyTotal, countTotal ):
	return _GetCountListRecur( moneyTotal, countTotal, 0)

# 根据小孩个数，计算每人应得的红包里的金额
def GetMoneyDistri( peopleCount ):
	res = range( g_pocket_min, g_pocket_max, (g_pocket_max-g_pocket_min)/peopleCount) + [g_pocket_max,]
	return [int(round(i)) for i in res]

# 对于若干个小孩子，计算最少需要的纸币张数
def GetPocketOfPeopleCount( peopleCount ):
	money_distri = GetMoneyDistri(peopleCount)
	moneyTotal = sum(money_distri)
	guess_count = 0;
	while guess_count <= moneyTotal:
		guess_count += 1
		pocket_list_all = []
		for money in money_distri:
			pocket_list = GetCountList(money, guess_count)
			if len(pocket_list) == 0:
				pocket_list_all = []
				break
			else:
				pocket_list_all.append(pocket_list[0])
		if len(pocket_list_all) != 0:
			for money, pocket in zip(money_distri, pocket_list_all):
				print money, pocket
			return# guess_count, pocket_list_all

print GetPocketOfPeopleCount(8)