# -*- coding:utf-8 -*-
# @Time     :2019/4/16 16:55
# @Author   :Tester_Liang
# @Email    :649626809@qq.com
# @File     :read_mysql.py
# @software :PyCharm
from sshtunnel import SSHTunnelForwarder
import MySQLdb
import MySQLdb.cursors
import mysql.connector


def operation_mysql(sql):
    # with SSHTunnelForwarder(
    #         ssh_address_or_host=("39.98.72.77", 22),  # B机器的配置
    #         ssh_password="1q2w3e4r",
    #         ssh_username="RR1q2w3e_",
    #         remote_bind_address=("47.94.8.135", 8306)) as server:  # A机器的配置
    #     # server.start()

    db_connect = MySQLdb.connect(host='47.94.8.135',  # 此处必须是是127.0.0.1
                                 port=8306,
                                 user="dbadmin",
                                 passwd="1qaz@WSX3edc",
                                 db="bus_linebus_platform",
                                 cursorclass=MySQLdb.cursors.DictCursor,
                                 charset='utf8'
                                 )
    cursor = db_connect.cursor()
    cursor.execute(sql)
    db_connect.commit()
    data = cursor.fetchall()
    db_connect.close()
    # server.stop()
    return data


if __name__ == '__main__':
    sql = "SELECT * from lb_config_text order by id desc LIMIT 10 "
    res = operation_mysql(sql)
    print(res[0]["id"])
