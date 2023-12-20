################################################################################
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
#
################################################################################

"""
Desc:    测试抓取链接
"""

import unittest
import re

from pytest202304.lib import webpage_download
from pytest202304.lib import webpage_parse


class UrlCrawlCase(unittest.TestCase):
    """
    网页抓取测试
    """

    def test_right_crawl(self):
        """
        正确的url抓取
        """
        crawl_url = 'http://www.sina.com.cn'
        target_re = re.compile('.*\.(html|gif|png|jpg|bmp)$')
        response = webpage_download.main('test', crawl_url, 2)
        url_list, res_list = webpage_parse.main(crawl_url, response, target_re)
        self.assertGreater(len(url_list), 0)
        self.assertGreater(len(res_list), 0)

    def test_error_crawl(self):
        """
        错误的url抓取
        """
        crawl_url = 'http://www.sina.wrong.url.com.cn'
        target_re = re.compile('.*\.(html|gif|png|jpg|bmp)$')
        response = webpage_download.main('test', crawl_url, 2)
        url_list, res_list = webpage_parse.main(crawl_url, response, target_re)
        self.assertEqual(len(url_list), 0)
        self.assertEqual(len(res_list), 0)


if __name__ == '__main__':
    unittest.main()