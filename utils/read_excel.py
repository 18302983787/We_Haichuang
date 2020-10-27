# =============================================================================
#     FileName: read_excel.py
#         Desc: read excel to sql
#       Author: minghao.guan
#        Email: minghao.guan@woqutech.com
#     HomePage: www.woqutech.com
#      Version: 0.0.1
#   LastChange: 
#      History:
# =============================================================================

import os
from datetime import datetime

import xlrd


def read_excel(path, name, sheet_index=0):
    workbook = xlrd.open_workbook(os.path.join(path, name))
    sheet = workbook.sheet_by_index(sheet_index)
    if sheet_index == 0:
        "获取招聘信息"
        for i in range(1, sheet.nrows):
            row = sheet.row_values(i)
            recname = row[0]
            tags = str(row[1])
            detail = row[2]
            pub_time = row[7]
            rec_time = row[3] if row[3] else "unknown"
            likes = row[4]
            views = row[5]
            link = row[6] if row[6] else "unknown"
            user_info = {"uid": "HC_REC_000{}".format(i),
                         "recname": recname,
                         "tags": tags,
                         "rec_detail": detail,
                         "pub_time": xlrd.xldate_as_datetime(pub_time, 0).strftime("%Y-%m-%d"),
                         "rec_time": xlrd.xldate_as_datetime(rec_time, 0).strftime(
                             "%Y-%m-%d") if rec_time != "unknown" else None,
                         "link": link,
                         "likes": likes,
                         "views": views,
                         }
            yield user_info
    elif sheet_index == 1:
        "获取活动信息"
        for i in range(1, sheet.nrows):
            row = sheet.row_values(i)
            act_time = row[0]
            loc = row[1]
            act_name = row[2]
            people = row[3][:-1]
            act_detail = row[4]
            user_info = {"uid": "HC_ACT_000{}".format(i),
                         "actname": act_name,
                         "tags": ["活动"],
                         "act_detail": act_detail,
                         "act_time": xlrd.xldate_as_datetime(act_time,
                                                             0).strftime(
                             "%Y-%m-%d"),
                         "loc": loc,
                         "people": people,
                         "posters": ""}
            yield user_info
