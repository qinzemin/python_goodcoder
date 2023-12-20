################################################################################
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
#
################################################################################

"""
Desc:    读取抓取配置文件
:param conf_path: 配置文件路径
:return spider_config: 配置类 SpiderConfig 实例
"""

import configparser
import logging
import sys
import traceback


class SpiderConfiger(object):
    """
    抓取配置类
    """
    def __init__(self, url_list_file,
                 target_url='.*\.(html|gif|png|jpg|bmp)$', output_directory='./output',
                 max_depth=1, crawl_interval=1, crawl_timeout=1, thread_count=1):
        """
        抓取配置类初始化
        :param url_list_file: 种子文件路径，必需
        :param target_url: 需要存储的目标网页URL pattern(正则表达式) ,需要考虑兼容抓取html等情况，默认 .*\.(html|gif|png|jpg|bmp)$
        :param output_directory: 抓取结果存储目录，默认 ./output
        :param max_depth: 最大抓取深度(种子为0级)，默认 1
        :param crawl_interval: 抓取间隔. 单位：秒，默认 1
        :param crawl_timeout: 抓取超时. 单位：秒，默认 1
        :param thread_count: 抓取线程数，默认 1
        """
        self.url_list_file = url_list_file
        self.target_url = target_url
        self.output_directory = output_directory
        self.max_depth = max_depth
        self.crawl_interval = crawl_interval
        self.crawl_timeout = crawl_timeout
        self.thread_count = thread_count

    @classmethod
    def config_load(cls, conf_path):
        cf = configparser.ConfigParser()
        filename = cf.read(conf_path)
        if len(filename) == 0:
            logging.error("配置文件：%s 路径无效" % conf_path)
            sys.exit("配置文件：%s 路径无效" % conf_path)
        section_name = 'spider'
        # 得到所有的section，以列表形式返回
        if section_name in cf.sections():
            try:
                # 得到section下的所有option
                opt = cf.options(section_name)
                url_list_file = cf.get(section_name, "url_list_file")  # 必需
                # 非必需
                target_url = cf.get(section_name, "target_url") if "target_url" in opt else None
                output_directory = cf.get(section_name, "output_directory") if "output_directory" in opt else None
                max_depth = cf.getint(section_name, "max_depth") if "max_depth" in opt else None
                crawl_interval = cf.getint(section_name, "crawl_interval") if "crawl_interval" in opt else None
                crawl_timeout = cf.getint(section_name, "crawl_timeout") if "crawl_timeout" in opt else None
                thread_count = cf.getint(section_name, "thread_count") if "thread_count" in opt else None
                logging.info("读取配置信息结果：url_list_file: %s, target_re: %s, "
                             "output_directory: %s, max_depth: %s, "
                             "crawl_interval: %s, crawl_timeout: %s, thread_count: %s"
                             % (url_list_file, target_url, output_directory, max_depth,
                                crawl_interval, crawl_timeout, thread_count))
                if max_depth <= 0 or crawl_interval <= 0 or crawl_timeout <= 0 or thread_count <= 0:
                    raise Exception("抓取参数不能为负数，请重新设置")
                spider_config = SpiderConfiger(url_list_file, target_url, output_directory, max_depth, crawl_interval,
                                             crawl_timeout, thread_count)
                return spider_config
            except Exception as e:
                logging.error("配置文件：%s 格式异常, msg is [%s]" % traceback.format_exc())
                sys.exit("配置文件：%s 格式异常，请检查配置内容" % conf_path)
        else:
            logging.error("配置文件：%s 中不含[spider]，请检查配置" % conf_path)
            sys.exit("配置文件：%s 中不含[spider]，请检查配置" % conf_path)