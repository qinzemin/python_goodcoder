################################################################################
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
#
################################################################################

"""
Desc:    将网页保存到磁盘
"""

import os
import threading
import logging
import traceback


class SaveThread(threading.Thread):
    """
    保存线程
    """
    def __init__(self, res_queue, output_directory, thread_name="save_thread"):
        """
        初始化保存线程
        :param res_queue: 结果保存队列
        :param output_directory: 抓取结果存储目录
        """
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.res_queue = res_queue
        self.output_directory = output_directory
        self.stop_event = threading.Event()

    def run(self):
        """
        启动线程
        """
        try:
            logging.info("%s 初始化完成，开始执行" % self.thread_name)

            with open(self.output_directory, 'w') as outfile:
                while not self.stop_event.is_set():
                    res = self.res_queue.get()
                    if res:
                        logging.info("保存 %s" % res)
                        outfile.write(res + os.linesep)
                        self.res_queue.task_done()
        except Exception as e:
            logging.error("保存抓取文件异常, msg is [%s]" % traceback.format_exc())

    def stop(self):
        """
        结束线程
        """
        self.stop_event.set()

    @classmethod
    def thread_save(cls, res_queue, output_directory):
        """
        构建收集结果线程
        :param res_queue: 结果保存队列
        :param output_directory: 抓取结果存储目录
        :return: save_thread: 收集结果线程
        """
        # 构建保存线程
        save_thread = SaveThread(res_queue, output_directory)
        return save_thread

