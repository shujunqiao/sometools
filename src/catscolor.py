#coding=utf-8 
"""
*********************************************************************************
*						题目：一千个汉姆雷特的帽子									*
*	1000个汉姆雷特排成一列，所有人均带有一顶帽子，假定有100种颜色的帽子，所有人听力、视力	*
*	都非常好（可以看到前面所有人的帽子，可以听到后面所有人是声音），从队伍最后开始大声报一个	*
*	帽子的颜色，一直到队伍排头。每有1人报对自己帽子的颜色，则奖励他们 1$，可累计。			*
*	请你给他们一个策略使得他们能拿到最多的$。	（可使用任何语言来实现，可真机操作）			*
*********************************************************************************
*	情景1：可提供一个简单的策略（队伍最后的人喊一个颜色，这个颜色是他前面所有人帽子颜色最	*
*		多的那个，则他前面所有人均报该颜色）。并问该策略可最低得到多少$？					*
*	情景2：问有没有更好的策略？该策略可最低得到多少$？	算法复杂度是多少？					*
*	情景3：还有没有更好的策略？同上。												*
*	情景4：针对提出的这个策略，估计需要多长时间？	能不能真机实现一下？然后就是实操了。		*
*	情景5：如果增加人数，递归还能不能正常执行？										*
*********************************************************************************
"""

import time
import random
from threading import Thread
import multiprocessing

time_start = time.time()	# 记录开始时间
pnum = 200000	# 队列人数
print('please input player num:', pnum)
cnum = 10000		# 帽子颜色数
space_num = 1000000000		# 预防超出值范围（目前是和，一般不会超出）
can_error = 0.001	# 当数据较大时，加入可容错率（数据大，则意味的时间长，加入该值，可提高效率）
print('color:', cnum)

# 随机生成初始队列
def randomarr(p, c):
	arr = []
	for x in range(p):
		rnum = int(random.random()*c)
		arr.append(rnum)
	return arr

curlist = randomarr(pnum, cnum)		# 当次的队列
larr = len(curlist)		# 当次队列的长度-即队列人数
resarr = []		# 记录结果的队列

# 获取’我‘前面所有人的值（对颜色总数取余）
def getFrontResult(arr, idx):
	sum = 0
	for x in range(idx):
		sum += arr[x]
		# if sum > space_num:
		# 	sum = sum % cnum
	return sum % cnum

# 获取’我‘后面所有人的值（对颜色总数取余，除最后一位。ps：最后一位是矫正位）
def getAfterResult(arr):
	sum = 0
	for x in range(len(arr)):
		if x > 0:
			sum += arr[x]
			# if sum > space_num:
			# 	sum = sum % cnum
	return sum % cnum

# 获取总猜对人数（也就是两个队列的相同值的数量）
def getSameNum(arr1, arr2):
	# print('arr1:', arr1)
	# print('arr2:', arr2)
	n = 0;
	for x in range(len(arr1)):
		if arr1[x] == arr2[x]:
			n = n + 1
	return n

# 类：参数为数组。
class GetCatsColor:
	# 初始化
	def __init__(self, arr):
		self._arr = arr
		self._resarr = []
	# 获取idx位置的颜色
	def getResultByPos(self, idx, l):
	  	if idx > 0:
		 	if idx == l:
		  		res = getFrontResult(self._arr, idx - 1)
		 	else:
		  		_prev = getFrontResult(self._arr, idx - 1)
		  		_next = getAfterResult(self._resarr)
		  		_res = self._resarr[0]
		  		res = _res - (_next + _prev)
		  		while res < 0:
		  			res = res + cnum
	  		self._resarr.append(res)
	# 计算result（其实可以使用队列，之所以改成for，因为递归是有堆栈长度限制的 当 pnum = 999 就报错）
	def getResultByPos2(self, larr):
		for x in range(larr):
			self.getResultByPos(larr - x, larr)
	# 返回结果（取反self._resarr）
	def getResultColor(self):
		self.getResultByPos2(len(self._arr))
		return self._resarr[::-1]

# 采用容许出错率（提升运行效率）
def useCanErrorRate(arr1, rate):
	num_error = int(rate * larr)
	if num_error <= 0:
		num_error = 1
	len_arr = len(arr1)
	len_part = int(len_arr / num_error)
	arr = []
	arr_result = []
	t_list = []
	for x in range(num_error):
		_end = (x + 1) * len_part
		if x == num_error - 1:
			_end = len_arr
		_arr = arr1[x * len_part : _end]
		_resarr1 = GetCatsColor(_arr).getResultColor()
		arr_result.extend(_resarr1)

	return arr_result

# 使用 Process
obj_result2 = multiprocessing.Manager().dict() # 使用 Process 时的中间变量
p_list = []		# 使用 Process 时的中间变量

# Process 调用对象函数
def doInProcess(arr1, idx, obj):
	global obj_result2
	t1 = time.time()
	pCatsColor = GetCatsColor(arr1)
	arrResult = pCatsColor.getResultColor()
	obj[idx] = arrResult
	# print('doInProcess idx:', idx, str(int(1000*(time.time() - t1))) + 'ms')

# 使用Process执行
def useCanErrorRateByProcess(arr1, rate):
	num_error = int(rate * larr)
	if num_error <= 0:
		num_error = 0
	len_arr = len(arr1)
	len_part = int(len_arr / num_error)
	arr = []
	for x in range(num_error):
		_end = (x + 1) * len_part
		if x == num_error - 1:
			_end = len_arr
		_arr = arr1[x * len_part : _end]
		_t = multiprocessing.Process(target=doInProcess,args=(_arr, x, obj_result2))
		_t.start()
		p_list.append(_t)
		# print('_arr', _arr)
		# print('_res', _resarr1)

	print('excute process here.')

# 使用join 会阻塞主进程
def joinAllProcess():
	for p in p_list:
		p.join()

# 返回结果
def getResulByProcess():
	arr_result = []
	for x in range(len(p_list)):
		if obj_result2.has_key(x):
			arr_result.extend(obj_result2[x])
	return arr_result

# 打印耗时
def logTime():
	print('time:', str(int(1000*(time.time() - time_start))) + 'ms')

if __name__ == '__main__':
	resarr = useCanErrorRate(curlist, can_error)
	numRight = getSameNum(resarr, curlist);
	print('res1:', (numRight, larr))
	logTime()

	###### 使用 Process ---START
	time_start = time.time()
	useCanErrorRateByProcess(curlist, can_error)
	# 使用 join
	joinAllProcess()
	_arr = getResulByProcess()
	numRight2 = getSameNum(_arr, curlist)
	print('res3:', (numRight2, larr))
	# # 使用sleep
	# while 1:
	# 	time.sleep(0.1)
	# 	_arr = getResulByProcess()
	# 	if len(_arr) == larr:
	# 		numRight2 = getSameNum(_arr, curlist)
	# 		print('res3:', (numRight2, larr))
	# 		break;
	logTime()
	###### 使用 Process ---END
