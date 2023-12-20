################################################################################
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
#
################################################################################

"""
Desc:    下载网页
"""

import requests
import re
import logging
import traceback


def is_url(url):
    """
    判断url是否合法
    """
    pattern = r"^https?:/{2}\w.+$"
    res = re.match(pattern, url)
    if res:
        return True
    else:
        return False


def main(thread_name, crawl_url, crawl_timeout, retries=3):
    """
    下载url
    :param thread_name: 线程名
    :param crawl_url: 下载url
    :param crawl_timeout: 抓取超时时间
    :param retries: 重试次数
    :return: 返回url对应的网页内容
    """
    crawl_res = None
    if is_url(crawl_url):
        try:
            crawl_res_req = requests.get(crawl_url, timeout=crawl_timeout)
            if crawl_res_req and crawl_res_req.status_code == requests.codes.ok:
                crawl_res = crawl_res_req.text
                logging.info('%s 从 url:%s 抓取页面信息，status_code: %s'
                             % (thread_name, crawl_url, crawl_res_req.status_code))
        except Exception as e:
            if retries > 0:
                logging.error("第 %s 次下载 url:%s 失败, 开始第 %s 次尝试" %
                              (4 - retries, crawl_url, 5 - retries))
                return main(thread_name, crawl_url, crawl_timeout, retries=retries - 1)
            else:
                # 打印异常，只打印第一和最后一行
                formatted_lines = traceback.format_exc().splitlines()
                logging.error("下载 url:%s 失败, %s, %s" % (crawl_url, formatted_lines[0], formatted_lines[-1]))
        finally:
            return crawl_res
    else:
        logging.error("url:%s 是无效地址" % crawl_url)
    return crawl_res
