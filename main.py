# -*- coding: utf-8 -*-
"""
@Software: PyCharm
@Project: WechatArticleCrawler
@Author: ZQ
@File: main.py
@Time: 2023/12/19 17:18
"""
import json
import re
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver

# 打开文件，以utf-8编码读取
with open('source/微信公众号历史文章网页源码.txt', encoding='utf-8') as f:
    # 创建一个空列表，用于存放url
    urls = []
    # 遍历文件中的每一行
    for line in f.readlines():
        # 使用正则表达式查找每一行中的url
        result = re.findall(r'<h4 class="weui_media_title" hrefs="(http://mp.weixin.qq.com.+?)">', line)
        # 如果查找到url，将其添加到列表中
        if len(result) == 1:
            urls.append(result[0])

# 创建EdgeOptions对象
edge_options = webdriver.EdgeOptions()
# 添加参数，启用打印浏览器功能
edge_options.add_argument('--enable-print-browser')
# 添加参数，以固定方式打印
edge_options.add_argument('--kiosk-printing')
# 定义了一个字典settings,其中包含了打印设置的参数,包括最近的打印目的地、选中的打印目的地ID、版本、是否启用页眉和页脚以及是否启用CSS背景
settings = {
    "recentDestinations": [
        {
            "id": "Save as PDF",
            "origin": "local"
        }
    ],
    "selectedDestinationId": "Save as PDF",
    "version": 2,
    "isHeaderFooterEnabled": False,
    "isCssBackgroundEnabled": True
}
# 设置打印设置
prefs = {
    'printing.print_preview_sticky_settings.appState': json.dumps(settings),  # JSON格式的打印设置字符串
    'savefile.default_directory': 'E:/PycharmProjects/WechatArticleCrawler/pdf'  # 保存PDF文件的路径
}
# 添加打印设置
edge_options.add_experimental_option('prefs', prefs)

# 创建浏览器对象
driver = webdriver.Edge(options=edge_options)
# 最大化窗口
driver.maximize_window()
# 遍历urls列表
for order in range(21, 22):
    # 获取url
    url = urls[order]
    # 打开url
    driver.get(url)
    # 等待title中不包含'微信公众平台'
    WebDriverWait(driver, 5).until_not(ec.title_contains('微信公众平台'))
    # 等待3秒
    time.sleep(3)
    # 获取html
    html = driver.page_source
    # 获取页面滚动高度
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    # 计算滚动步数
    count = scroll_height // 100
    scroll_step = scroll_height / (count if count > 0 else 1)
    # 遍历滚动步数
    for i in range(count):
        # 滚动到指定位置
        driver.execute_script(f"window.scrollTo(0, {(i + 1) * scroll_step});")
        # 等待0.2秒
        time.sleep(0.2)
    # 判断html中是否包含'404 not found'和'点击跳转'
    if '404 not found' not in html and '点击跳转' not in html:
        # 使用正则表达式匹配title
        result = re.findall('<title>(.+?)</title>', html)
        # 判断title是否只有一个
        if len(result) == 1:
            # 获取title
            title = result[0]
            # 设置title
            js = f"document.title='{title}';window.print();"
            # 执行js
            driver.execute_script(js)
            # 打印title和url
            print(f'{order}:{title}:{url}')
        else:
            # 打印未知标题和url
            print(f'{order}:未知标题:{url}')
# 等待3秒
time.sleep(3)
# 退出浏览器
driver.quit()
