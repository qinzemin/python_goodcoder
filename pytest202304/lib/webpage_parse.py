################################################################################
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
#
################################################################################

"""
Desc:    对抓取网页的解析
"""

import bs4
import logging

import urllib.parse as url_parse


def get_url_list_or_res_list(crawl_url, urls, target_re):
    """
    获取 url_list 、res_list
    :param crawl_url: 当前抓取url
    :param urls: 页面元素
    :param target_re: 正则对象
    :return 返回的url_list 或 res_list
    """
    fanal_list = []
    for url in urls:
        href_url = url.get("href")
        if not href_url:
            continue
        elif href_url.startswith("http"):
            final_url = href_url
        elif "javascript:location.href" in href_url:
            # javascript:location.href="/url"
            final_url = url_parse.urljoin(crawl_url, href_url.split("=")[-1].split("\"")[-2])
        else:
            final_url = url_parse.urljoin(crawl_url, href_url)
        # 匹配校验
        if target_re.match(final_url):
            fanal_list.append(final_url)
    return fanal_list


def main(crawl_url, webpage_res, target_re):
    """
    下载url
    :param crawl_url: 当前抓取url
    :param webpage_res: 下载的网页内容
    :param target_re: 正则对象
    :return url_list: 当前网页的所有url
    :return res_list: 满足正则的网页抓取内容
    """
    url_list = []
    res_list = []
    if webpage_res:
        soup = bs4.BeautifulSoup(webpage_res, "html.parser")
        # 获取所有的<a><link><img>
        tag_a_link_res = soup.find_all(["a", "link"])
        tag_a_link_img_res = soup.find_all(["a", "link", "img"])

        url_list = get_url_list_or_res_list(crawl_url, tag_a_link_res, target_re)
        res_list = get_url_list_or_res_list(crawl_url, tag_a_link_img_res, target_re)
        logging.info("%s 页面含新url个数:%s，页面获取到符合正则限定的数据个数:%s" %
                     (crawl_url, len(url_list), len(res_list)))
    return url_list, res_list
