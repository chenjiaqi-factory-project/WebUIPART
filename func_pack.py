import random
import datetime
from datetime import timedelta
import json
import pandas as pd


# 随机生成唯一编码
def create_random_hash():
    nowtime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    hash_code = hash(nowtime)
    # 绝对值处理
    if hash_code < 0 :
        hash_code = str(abs(hash_code))
    else:
        hash_code = str(hash_code)
    # 再添加随机位确保哈希值不重复
    seed = "abcdef"
    title = ""
    for _ in range(6):
        title = title + random.choice(seed)
    return str(title + hash_code)


# 生成记录唯一编码
def create_rec_hash():
    return "rec" + create_random_hash()


# 将 requests.get 或 post 的结果 result 获取到的信息转为由 dict 构成的 list
# 使用方法 :
# content = requests.get('http://23.106.158.242:30080/users')
# get_api_info(content)
# 注意！ API 的 json 数据的最外层必须是 list 的形式，如 [{'k':'value'}]
# 不用 list 作为最外层将不能转化成功，如 {'k':'value'}
def get_api_info(request_result):
    content_str = request_result.content.decode("utf-8")
    list_content = []
    # print("json.loads length=" + str(len(json.loads(content_str))))
    # 若 api 返回的是空值
    if json.loads(content_str) is None:
        # 返回空的 list
        return []
    # 否则对 api 信息进行处理
    else:
        for item in json.loads(content_str):
            list_content.append(item)
        # 返回处理好的 list
        return list_content


# 将 requests.get 或 post 的结果 result 获取到的信息转为唯一的 dict 。仅用于 list 中仅有一个元素的情况。
# 使用方法 :
# content = requests.get('http://23.106.158.242:30080/users')
# get_api_info(content)
# 注意！ API 的 json 数据的最外层必须是 list 的形式，如 [{'k':'value'}]
# 不用 list 作为最外层将不能转化成功，如 {'k':'value'}
def get_api_info_first(request_result):
    content_str = request_result.content.decode("utf-8")
    list_content = []
    # print("json.loads length=" + str(len(json.loads(content_str))))
    # 若 api 返回的是空值
    if json.loads(content_str) is None:
        # 返回空的 list
        return []
    # 否则对 api 信息进行处理
    else:
        for item in json.loads(content_str):
            list_content.append(item)
        # 如果 list 内没有元素, 返回空字典
        if len(list_content) < 1:
            return {'error': 'Count over the boundary!'}
        # 如果 list 内只有唯一一个元素 返回
        elif len(list_content) == 1:
            return list_content[0]
        else:
            # 返回处理好的 list 的头个元素
            return list_content[0]


# 生成当前时间 格式为 %Y-%m-%d/%H:%M:%S
def get_current_datetime():
    return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# 生成当前日期
def get_current_date():
    return str(datetime.datetime.now().strftime("%Y-%m-%d"))


# 以 strftime 生成当前日期
def get_current_date_strftime():
    return datetime.datetime.now()


# 生成上一天日期
def get_last_date():
    now = datetime.datetime.now()
    last_datetime = now - timedelta(days=1)
    return str(last_datetime.strftime("%Y-%m-%d"))


# 以 strftime 生成上一天日期
def get_last_date_strftime():
    now = datetime.datetime.now()
    last_datetime = now - timedelta(days=1)
    return last_datetime


# 生成当前时间
def get_current_time():
    return str(datetime.datetime.now().strftime("%H:%M:%S"))


# 创建 csv 文件
def write_csv(document_list, file_path):
    doc_pd = pd.DataFrame(document_list)
    doc_pd.to_csv(file_path)
    return
