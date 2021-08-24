# -*- coding:utf-8 -*-
# @Time     :2019/4/4 9:04
# @Author   :Tester_Liang
# @Email    :649626809@qq.com
# @File     :MyLog.py
# @software :PyCharm
from BusProject.Linebus_Platform_API.common import DataPaths
import logging


class MyLogs:

    def mylog(self, level, msg):
        logger = logging.getLogger('Bus_API')
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(formatter)
        fh = logging.FileHandler(DataPaths.LogsPath, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(sh)
        logger.addHandler(fh)

        if level == "DEBUG":
            logger.debug(msg)
        elif level == "INFO":
            logger.info(msg)
        elif level == "WARNING":
            logger.warning(msg)
        elif level == "ERROR":
            logger.error(msg)
        elif level == "CRITICAL":
            logger.critical(msg)
        logger.removeHandler(sh)
        logger.removeHandler(fh)

    def debug(self, msg):
        self.mylog("DEBUG", msg)

    def info(self, msg):
        self.mylog("INFO", msg)

    def warning(self, msg):
        self.mylog("WARNING", msg)

    def error(self, msg):
        self.mylog("ERROR", msg)

    def critical(self, msg):
        self.mylog("CRITICAL", msg)
