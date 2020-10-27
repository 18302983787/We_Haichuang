'''
#=============================================================================
#     FileName: 
#         Desc: 
#       Author: minghao.guan
#        Email: minghao.guan@woqutech.com
#     HomePage: www.woqutech.com
#      Version: 0.0.1
#   LastChange: 
#      History:
#=============================================================================
'''


def id_format(_id):
    """
    将_id变为5位表示
    :param _id:
    :return:
    """
    if len(str(_id)) == 1:
        return "0000{}".format(str(_id+ 1))
    elif len(str(_id)) == 2:
        return "000{}".format(str(_id + 1))
    elif len(str(_id)) == 3:
        return "00{}".format(str(_id + 1))
    elif len(str(_id)) == 4:
        return "0{}".format(str(_id + 1))
    else:
        return "{}".format(str(_id + 1))


def name_format(table_name):
    """
    构建uid时需要的表信息
    :param table_name:
    :return:
    """
    if "user" in table_name:
        return "USR"
    elif "act" in table_name:
        return "ACT"
    elif "rec" in table_name:
        return "REC"


