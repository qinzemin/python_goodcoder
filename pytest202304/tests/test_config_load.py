################################################################################
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
#
################################################################################

"""
Desc:    测试配置文件
"""

import unittest

from pytest202304.lib.config_load import SpiderConfiger


class ConflgCase(unittest.TestCase):
    """
    待测试的类，测试配置文件读取
    """

    def test_config_load_right_path(self):
        """
        测试配置文件读取正常路径
        """
        conf = SpiderConfiger.config_load("../conf/spider.conf")
        print(conf)

    def test_config_load_null_path(self):
        """
        测试配置文件读取空路径
        """
        conf = SpiderConfiger.config_load()
        print(conf)

    def test_config_load_wrong_path(self):
        """
        测试配置文件读取错误路径
        """
        conf = SpiderConfiger.config_load("../conf/spider2.conf")
        print(conf)


if __name__ == '__main__':
    unittest.main()
