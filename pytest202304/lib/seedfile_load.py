################################################################################
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
#
################################################################################


"""
Desc:    读取种子文件
:param seedfile_path: 种子路径
:return seedfile_list: 种子列表
"""

import logging


class SeedLoader(object):
    @classmethod
    def seed_file_load(cls, seedfile_path):
        """
        读取种子文件
        :param seedfile_path: 种子路径
        """
        with open(seedfile_path, 'r') as seedfile:
            # 去除换行符
            seedfile_list = [line.replace('\r', '').replace('\n', '').replace('\t', '')
                             for line in seedfile.readlines()]
            logging.info("读取种子文件：共有 %s 个种子文件，%s" % (len(seedfile_list), seedfile_list))
            return seedfile_list
