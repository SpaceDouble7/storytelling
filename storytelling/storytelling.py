# -*- coding: utf-8 -*-
__author__ = 'Zhao Yu'

import urllib2
import re
import time
import json
import wget
import socket
from os import path


class Storytelling:
    def __init__(self, app_id, app_secret):
        self.__download_page_regex__ = re.compile(r"<a href=\"(http://www\.5ips\.net/down[\w\W]+?)\">[\w\W]*?</a>")
        # 查询ip的地址，具体使用可以参考https://www.showapi.com/api/lookPoint/632的说明
        base_url = 'https://route.showapi.com/632-1?showapi_appid=' + app_id + '&showapi_timestamp=' + time.strftime(
            '%Y%m%d%H%M%S')
        api_url = base_url + '&showapi_sign=' + app_secret
        try_time = 3
        timeout = 5
        html_doc = None

        while True:
            if try_time <= 0:
                break
            try:
                response = urllib2.urlopen(api_url, timeout=timeout)
                html_doc = response.read()
                break
            except urllib2.URLError:
                try_time -= 1
                html_doc = None

        if html_doc is None:
            print("please check your network")
            exit()
        ip_info = json.loads(html_doc)
        self.isp = ip_info['showapi_res_body']['isp']

    def get_download_page_list(self, root_page, try_time=3, timeout=5):
        """
        该函数用于给定一个http://www.5ips.net/的评书首页之后，获得该评书的下载页面的url
        比如，三国演义的首页为：http://www.5ips.net/ps/36.htm
        :param root_page: 需要下载的评书的首页
        :param try_time: 尝试次数，默认3次
        :param timeout: 超时时间，默认5s
        :return: 返回下载链接的list，如果没有则为None
        """
        html_doc = None
        while True:
            if try_time <= 0:
                break
            try:
                response = urllib2.urlopen(root_page, timeout=timeout)
                html_doc = response.read()
                break
            except urllib2.URLError:
                html_doc = None
                try_time -= 1
                # print(e)

        if html_doc is None:
            return None

        return re.findall(self.__download_page_regex__, html_doc)

    def get_resource_url_from_download_page_url(self, download_page_url, try_time=3, timeout=5):
        """
        根据下载网页的地址，解析下载资源的地址
        :param download_page_url:
        :param try_time:
        :param timeout:
        :return:
        """
        down_url = None
        while True:
            if try_time <= 0:
                break
            try:
                response = urllib2.urlopen(download_page_url, timeout=timeout)
                html_doc = response.read()
                # 获取下载地址的三个部分的url
                url0 = re.search(r"url\[0\]= \"([\d\D]+?)\";", html_doc)  # 电信的url开头
                url1 = re.search(r"url\[1\]= \"([\d\D]+?)\";", html_doc)  # 联通的url开头
                url2 = re.search(r"url\[2\]= \"([\d\D]+?)\";", html_doc)  # 资源的子目录
                if self.isp == u"电信":
                    down_url = url0.group(1) + url2.group(1)
                elif self.isp == u"联通":
                    down_url = url1.group(1) + url2.group(1)
                else:
                    down_url = url0.group(1) + url2.group(1)
                break
            except urllib2.URLError:
                try_time -= 1
                down_url = None

        return down_url

    @staticmethod
    def download_file(url, save_path, file_name=None, try_time=3, timeout=60):
        """
        使用wget模块进行数据的下载
        :param url:
        :param save_path:
        :param file_name:
        :param try_time:
        :param timeout:
        :return:
        """
        print(save_path)
        print(file_name)
        print(url)
        print(path.basename(url))
        print(path.basename(url).split("?")[0])
        if file_name is not None:
            save_file_full_name = path.join(save_path, file_name)
        else:
            save_file_full_name = path.join(save_path, path.basename(url).split("?")[0])
        socket.setdefaulttimeout(timeout)
        print(save_file_full_name)
        while True:
            if try_time <= 0:
                break
            try:
                wget.download(url, save_file_full_name)
                break
            except socket.timeout:
                try_time -= 1
