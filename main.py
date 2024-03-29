# -*- coding: utf-8 -*-
__author__ = 'Zhao Yu'

import storytelling.storytelling

# 这里使用了https://www.showapi.com/ 的两个api，用于获取外网的ip信息
# app id和app secret可以从https://www.showapi.com/注册并获得
st = storytelling.storytelling.Storytelling('app id', 'app secret')
download_page_url_list = st.get_download_page_list('http://www.5ips.net/ps/36.htm')
print(download_page_url_list)

url = st.get_resource_url_from_download_page_url(download_page_url_list[0])
print(url)

st.download_file(url, 'C:', 'momoda')