################################################################################
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
#
################################################################################

"""
Desc:    迷你定向网页抓取器
实现对种子链接的广度优先抓取，并把URL长相符合特定pattern的网页内容（图片或者html等）保存到磁盘上
"""

import argparse
import time

from lib import log
from lib.config_load import SpiderConfiger
from lib.seedfile_load import SeedLoader
from lib.url_table import UrlQueue
from lib.res_table import ResQueue
from lib.crawl_thread import CrawlThread
from lib.webpage_save import SaveThread


def main(conf_path):
    """
    主程序入口
    :param conf_path: 配置文件路径
    :return:
    """
    # 日志初始化, 设置日志写入文件和控制台
    log.init_log('./logs/mini_spider_%s' % time.strftime('%Y-%m-%d', time.localtime(time.time())))

    # 读取配置文件
    # spider_config = config_load.main(conf_path)
    spider_config = SpiderConfiger.config_load(conf_path)
    # 读取种子文件
    seedfile_list = SeedLoader.seed_file_load(spider_config.url_list_file)

    # 构建url管理队列
    url_queue = UrlQueue.queue_build()
    # 构建res保存队列
    res_queue = ResQueue.res_build()

    # 构建抓取线程列表
    crawl_thread_list = CrawlThread.thread_load(url_queue, res_queue, spider_config.thread_count,
                                spider_config.target_url, spider_config.crawl_interval, spider_config.crawl_timeout)
    # 构建收集结果线程
    save_thread = SaveThread.thread_save(res_queue, spider_config.output_directory)

    # 对抓取进行控制
    CrawlThread.controller(
        seedfile_list, url_queue, res_queue, spider_config.max_depth, crawl_thread_list, save_thread)


if __name__ == '__main__':
    # 命令行参数处理
    desc = """迷你定向网页抓取器"""
    argparse = argparse.ArgumentParser(prog="mini_spider", description=desc)
    argparse.add_argument("-v",
                          "--version",
                          action="version",
                          version="%(prog)s 1.0",
                          help="显示版本信息")
    argparse.add_argument("-c",
                          "--config",
                          required=True,
                          help="必填选项，输入爬虫配置文件路径")
    args = argparse.parse_args()
    main(args.config)  # -c conf/spider.conf
