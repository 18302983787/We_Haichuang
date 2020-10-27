import requests
import hashlib

from flask import Flask
from flask import render_template
from flask import request
from flask import json
from hc_database import *

app = Flask(__name__)


@app.route('/')
def haichuang_web():
    return render_template("haichuang_web.html")


@app.route('/api/onLogin', methods=['GET', 'POST'])
def login():
    data = request.values.get("code")
    appid = "wx04be3367dc046a40"
    app_secret = '8eed51d12d94160f3e8f4b50fc86d1f8'
    req_params = {
        'appid': appid,
        'secret': app_secret,
        'js_code': data,
        'grant_type': 'authorization_code'
    }
    code_2_session = "https://api.weixin.qq.com/sns/jscode2session"
    response_data = requests.get(code_2_session, params=req_params)  # 向API发起GET请求
    res_data = response_data.json()
    openid = res_data['openid']  # 得到用户关于当前小程序的OpenID
    # print("+-------------当前用户是:{}---------------+\n+---------------openid是:{}---------------+".format(data, openid))
    session_key = res_data['session_key']
    md5 = hashlib.md5()
    md5.update(openid.encode("utf-8"))
    user_session = md5.hexdigest()
    info = ("user_session", user_session)
    table_name = "hc_user"
    conn = DataBase("HaiChuang")
    info = conn.select(table_name, info=info)

    if info:
        user_info = {"user_session": user_session, "is_regist": True}
    else:
        user_info = {"user_session": user_session, "is_regist": False}

    # print(user_session)
    return json.dumps(user_info)


@app.route("/api/request_info", methods=['POST'])
def get_info():
    table_name = request.values.get("table")
    user_session = request.values.get("user_session")
    conn = DataBase()
    if user_session:
        res = conn.select(table_name, info=("user_session", user_session))
    else:
        res = conn.select(table_name)
    return res


@app.route("/api/request_my_activity", methods=["POST"])
def get_my_activity():
    """
    请求我的活动
    :return:
    """
    table_name = request.values.get("table")
    user_session = request.values.get("user_session")

    # 链接数据库
    # 1. 查询活动报名表中当前用户参加的活动id
    # 2. select
    conn = DataBase()


@app.route("/api/sign_up", methods=["POST"])
def sign_act():
    """
    报名函数
        - request包含表名，活动uid和用户session
    :return:
        res -> dict
            - response insert的返回值
            - is_signed 是否报名
    """
    response = None
    table_name = request.values.get("table_name")
    user_session = request.values.get("user_session")
    act_uid = request.values.get("act_uid")
    sign_key = hash(user_session + act_uid)

    sign_info = dict()
    sign_info["act_uid"] = request.values.get("act_uid")
    sign_info["user_session"] = request.values.get("user_session")
    sign_info["sign_key"] = sign_key

    conn = DataBase("HaiChuang")
    print("【sign-up】 : ", sign_info)
    select_res = conn.select(table_name, fields="sign_key", info=("sign_key", sign_key))
    if select_res and select_res:
        is_signed = True
        print(select_res)
    else:
        is_signed = False
        response = conn.insert(table_name, sign_info)

    res = {"response": response,
           "is_signed": is_signed}
    return res


@app.route("/api/register", methods=["POST"])
def register():
    table_name = request.values.get("table_name")
    register_info = dict()
    # register_info["uid"] = request.values.get("table_length")
    register_info["user_session"] = request.values.get("user_session")
    register_info["username"] = request.values.get("username")
    register_info["phone"] = request.values.get("phone")
    register_info["gender"] = request.values.get("gender")
    register_info["age"] = request.values.get("age")
    register_info["birth"] = request.values.get("birth")
    register_info["loc"] = request.values.get("loc")
    register_info["graduate"] = request.values.get("graduate")
    conn = DataBase("HaiChuang")
    response = conn.insert(table_name, register_info)
    res = {"response": response}
    return json.dumps(res)


@app.route("/api/get_user_infos")
def get_user_infos():
    act_uid = request.values.get("act_uid")
    user_session = request.values.get("user_session")
    conn = DataBase("HaiChuang")
    _sql = "select * from hc_activity as a right join hc_activity_sign as b on a.act_uid = b.act_uid;"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
