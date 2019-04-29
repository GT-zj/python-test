#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
from conf import settings
from atm.main import atm_run
from db.db_handler import save_db, load_db
from shopping.main import shopping_run
import os
from utils.print_log import return_logger_obj, print_info
import time
import datetime


def welcome():
    while 1:
        menu = '''
        1.登录
        2.添加新用户
        3.修改用户额度
        4.退出
        '''
        menu_list = {
            "1": user_login,
            "2": add_new_user,
            "3": modify_credit,
            "4": exit
        }
        print_info(menu)
        your_choice = input("please input one number for your choice:").strip()
        if your_choice in menu_list:
            menu_list[your_choice]()
        else:
            print_info("your input is illegal!", "error")
            continue


def user_login():
    login_user = []
    lock_status = True
    login_times = 0
    user_data = {}
    user_name = ""
    login_user_file = ""
    """
    提示用户登录。
    :return:
    """
    while login_times < 3:
        logger = return_logger_obj("login_log")
        user_name = input("please input your name:").strip()
        password = input("please input your password:").strip()
        # login_user_file = E:\PythonProject\python-test\homework\atm/db\accounts/vita.json
        login_user_file = os.path.join(settings.DATABASE["path"], '%s/%s.json' % (settings.DATABASE["name"], user_name))
        if os.path.isfile(login_user_file):

            # 从文件中取出数据
            user_data = load_db(login_user_file)
            if password == user_data["password"]:
                if user_data["lock_status"] == "no":
                    logger.info("Account [%s] has login in successful!" % user_name)
                    # user_data = {"user_name": "vita", "password": "1234567", "login": "yes","lock_status":"no"}
                    user_data["login"] = "yes"
                    return user_data
                else:
                    print_info("Account [%s] has been locked!" % user_name)
            else:
                # print("\033[31;1mPassword of [%s] does not correct!\033[0m" % user_name)
                print_info("Password of [%s] does not correct!" % user_name, "error")
                logger.error("Password of [%s] does not correct!" % user_name)

        else:
            # print("\033[31;1mAccount [%s] does not exist!\033[0m" % user_name)
            print_info("Account [%s] does not exist!" % user_name, "error")
            logger.error("Account [%s] does not exist!" % user_name)

        lock_or_not(user_name, login_user)
        login_times += 1
    else:
        # len(user_data) > 0 只有用户存在时，user_data才不为空
        # user_data 为空就不需要设置lock_status了
        if len(user_data) > 0:
            # {'user_name': 'vita', 'password': '1234567', 'lock_status': 'yes'}
            user_data = set_lock_status(user_name, user_data, lock_status)
            # 一个用户，三次登录失败，就锁定，并写入文件

            save_db(login_user_file, user_data)
        # 条件不符合，返回None
        exit()


def shopping_or_atm(user_data):
    """
    给出提示信息，用于选择是进行shopping操作还是进行atm操作
    :return:
    """
    info = """
    welcome come to this system!
    1.for shopping
    2.for atm 
    3.exit
    """
    choice_list = {
        "1": shopping_run,
        "2": atm_run,
        "3": exit
    }
    print_info(info)
    your_choice = input("please input your choice:").strip()
    if your_choice.isdigit() and your_choice in choice_list:
        choice_list[your_choice](user_data)

    else:
        print_info("your input must be a number showed before!", "error")


def lock_or_not(user_name, login_user):
    # user_name = user_data["user_name"]
    if len(login_user) == 0:
        login_user.append(user_name)
    elif user_name != login_user[-1]:
        lock_status = False


# 锁定用户
def set_lock_status(user_name, user_data, lock_status):
    # 用于判断最后一次登录的用户是否存在
    # len(user_data) > 0 只有用户存在时，user_data才不为空
    if lock_status is True and user_data["lock_status"] == "no":
        user_data["lock_status"] = "yes"
    return user_data


def add_new_user():
    # 这些值在申请信用卡的时候已经是默认的了
    new_user = {"lock_status": "no", "credit": 15000, "left_credit": 15000, "repay_day": 22}
    your_choice = input("do you want to add a new uer[YES/NO]?:").strip().lower()
    if your_choice == 'yes':
        while 1:
            user_name = input("please input new user name:").strip()
            new_user_db_file = os.path.join(settings.DATABASE["path"], '%s/%s.json' %
                                            (settings.DATABASE["name"], user_name))
            if os.path.exists(new_user_db_file):
                print_info("this user has already exist!","error")
                continue
            password = input("please input password:").strip()
            if len(user_name) == 0 or len(password) == 0:
                print_info("username or password can not be null!")
                continue
            enroll_date = time.strftime("%Y-%m-%d", time.gmtime())
            # 2024-04-27 14:11:20.520427转换为字符串后，在进行切割，得到年月日
            # 假设有效期是5年
            expire_date = str(datetime.datetime.now() + datetime.timedelta(5*365)).split()[0]
            new_user["user_name"] = user_name
            new_user["password"] = password
            new_user["enroll_date"] = enroll_date
            new_user["expire_date"] = expire_date

            save_db(new_user_db_file, new_user)
            print_info("add new user success!")
            break


# 修改额度
def modify_credit():
    while 1:
        user_name = input("please input user name you want to change credit:").strip()

        user_db_file = os.path.join(settings.DATABASE["path"], '%s/%s.json' %
                                        (settings.DATABASE["name"], user_name))
        if os.path.exists(user_db_file):
            credit = input("please input your new credit:").strip()
            if credit.isdigit():
                user_data = load_db(user_db_file)
                user_data["credit"] = credit
                save_db(user_db_file, user_data)
                print_info("update credit successful!")
                break
            else:
                print_info("you can just input one number!")
                continue
        else:
            print_info("user is not exist!")
            continue
