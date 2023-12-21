# -*- coding: utf-8 -*-
"""
@Software: PyCharm
@Project: WechatArticleCrawler
@Author: ZQ
@File: export_environment.py
@Time: 2023/12/21 15:16
"""
import os
import sys

os.system(f'"{sys.executable}" -m pip freeze > requirements.txt')
