################################################################################
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
#
################################################################################

"""
Desc:    实现抓取线程
"""

import threading
import re
import logging
import time
import traceback

from pytest202304.lib import webpage_parse
from pytest202304.lib import webpage_download


class CrawlThread(threading.Thread):
    """
    抓取线程
    """
    def __init__(self, url_queue, res_queue, crawl_interval, crawl_timeout, target_re,
                 thread_name="crawl_thread"):
        """
        抓取线程初始化
        :param url_queue: url管理队列
        :param res_queue: 结果保存队列
        :param crawl_interval: 抓取间隔. 单位：秒
        :param crawl_timeout: 抓取超时. 单位：秒
        :param target_re: 正则对象
        """
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.url_queue = url_queue
        self.res_queue = res_queue
        self.crawl_interval = crawl_interval
        self.crawl_timeout = crawl_timeout
        self.target_re = target_re
        self.stop_event = threading.Event()
        self.url_list_cur = list()  # 待抓取url列表
        self.res_list_cur = list()  # 待保存res列表

    def run(self):
        """
        执行
        """
        try:
            logging.info("%s 初始化完成，开始执行" % self.thread_name)

            while not self.stop_event.is_set():
                crawl_url = self.url_queue.get()
                if crawl_url:
                    logging.info("%s 开始执行抓取url:%s" % (self.thread_name, crawl_url))
                    webpage_res = webpage_download.main(self.thread_name, crawl_url, self.crawl_timeout)
                    url_list, res_list = webpage_parse.main(crawl_url, webpage_res, self.target_re)
                    self.url_list_cur.extend(url_list)
                    self.res_list_cur.extend(res_list)
                    self.url_queue.task_done()
                time.sleep(self.crawl_interval)
        except Exception as e:
            logging.error("保存抓取文件异常, msg is [%s]" % traceback.format_exc())

    def get_url_list_cur(self):
        """
        获取待抓取url列表
        """
        return self.url_list_cur

    def get_res_list_cur(self):
        """
        获取待保存res列表
        """
        return self.res_list_cur

    def clear(self):
        """
        清理待抓取url列表与保存res列表
        """
        self.url_list_cur.clear()
        self.res_list_cur.clear()

    def stop(self):
        """
        结束线程
        """
        self.stop_event.set()

    @classmethod
    def controller(cls, seedfile_list, url_queue, res_queue, max_depth, crawl_thread_list, save_thread):
        """
        构建启动抓取线程
        :param seedfile_list: 种子列表
        :param url_queue: url管理队列
        :param res_queue: res保存队列
        :param max_depth: 最大抓取深度
        :param crawl_thread_list: 抓取线程列表
        :param save_thread: 收集结果线程
        :return:
        """
        # 加入urls中初始链接
        url_queue.put_list(seedfile_list)
        # 启动抓取线程
        for crawl_thread in crawl_thread_list:
            crawl_thread.start()
        # 启动保存线程
        save_thread.start()

        cur_depth = 1
        while True:
            logging.info(
                "***************************** 当前抓取深度：%d，最大抓取深度：%d *****************************"
                % (cur_depth, max_depth))
            url_queue.join()
            # 深度 cur_depth 抓取结束，更新 url_queue、res_queue
            if cur_depth < max_depth:
                for crawl_thread in crawl_thread_list:
                    url_queue.put_list(crawl_thread.get_url_list_cur())
                    res_queue.put_list(crawl_thread.get_res_list_cur())
                    crawl_thread.clear()
            elif cur_depth == max_depth:
                for crawl_thread in crawl_thread_list:
                    res_queue.put_list(crawl_thread.get_res_list_cur())
                    crawl_thread.clear()
                    crawl_thread.stop()
                break
            cur_depth += 1

        res_queue.join()
        save_thread.stop()

        for crawl_thread in crawl_thread_list:
            crawl_thread.join()

    @classmethod
    def thread_load(cls, url_queue, res_queue, thread_count, target_url, crawl_interval, crawl_timeout):
        """
        构建抓取线程
        :param url_queue: url管理队列
        :param res_queue: 结果保存队列
        :param thread_count: 抓取线程数
        :param target_url: 目标网页URL正则表达式
        :param crawl_interval: 抓取间隔. 单位：秒
        :param crawl_timeout: 抓取超时. 单位：秒
        :return crawl_thread_list: 抓取线程列表
        """
        # 编译正则对象
        target_re = re.compile(target_url)
        # 构建抓取线程
        crawl_thread_list = list()
        for index in range(thread_count):
            crawl_thread_list.append(CrawlThread(url_queue, res_queue, crawl_interval, crawl_timeout, target_re,
                                                 "crawl_thread_%s" % index))
        return crawl_thread_list
