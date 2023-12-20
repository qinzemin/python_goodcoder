################################################################################
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
#
################################################################################

"""
Desc:    构建url管理队列
"""

import queue
import logging
import threading


class UrlQueue(object):
    """
    url管理队列
    """
    def __init__(self):
        """
        初始化url队列
        """
        self.url_queue = queue.Queue()
        self.url_set = set()  # 去重
        self.timeout = 5  # 获取队列，timeout等待时间
        self.lock = threading.Lock()

    def put_list(self, url_list):
        """
        新增url列表
        """
        if isinstance(url_list, list):
            for url in url_list:
                if url is not None:
                    self.lock.acquire()
                    try:
                        if url not in self.url_set:
                            self.url_queue.put(url)
                            self.url_set.add(url)
                    finally:
                        self.lock.release()

    def get(self):
        """
        取url
        """
        try:
            return self.url_queue.get(timeout=self.timeout)
        except Exception as e:
            logging.info("队列中暂无url")

    def task_done(self):
        """
        已完成
        """
        self.url_queue.task_done()

    def join(self):
        """
        阻塞
        """
        self.url_queue.join()

    @classmethod
    def queue_build(cls):
        """
        构建url管理队列
        :return: url_queue: url管理类 UrlQueue 实例
        """
        url_queue = UrlQueue()
        logging.info("构建url管理队列：完成")
        return url_queue


