################################################################################
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
#
################################################################################

"""
Desc:    结果保存队列
"""

import queue
import logging


class ResQueue(object):
    """
    res管理类
    """

    def __init__(self):
        """
        初始化res队列
        """
        self.res_queue = queue.Queue()
        self.timeout = 5  # 获取队列，timeout等待时间

    def put_list(self, res_list):
        """
        新增res列表
        """
        if isinstance(res_list, list):
            for res in res_list:
                self.res_queue.put(res)

    def get(self):
        """
        取结果
        """
        try:
            return self.res_queue.get(timeout=self.timeout)
        except Exception as e:
            logging.info("队列中暂无res")

    def task_done(self):
        """
        已完成
        """
        self.res_queue.task_done()

    def join(self):
        """
        阻塞
        """
        self.res_queue.join()

    @classmethod
    def res_build(cls):
        """
        构建res保存队列
        :return: res_queue: res管理类 ResQueue 实例
        """
        res_queue = ResQueue()
        logging.info("构建res保存队列：完成")
        return res_queue


def main():
    """
    构建res保存队列
    :return: res_queue: res管理类 ResQueue 实例
    """
    res_queue = ResQueue()
    logging.info("构建res保存队列：完成")
    return res_queue
