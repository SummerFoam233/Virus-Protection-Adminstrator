from django.test import TestCase
import folium.plugins as plugins
import folium
from hashlib import md5

from jpype import *
import os.path

m = 'qwe'
salt = '30155053-aa33-426c-a883-b94d02b9'

jarpath = os.path.abspath('.')  # 这个函数用来获取当前 python 脚本所在的绝对路径
startJVM('shiro-all-1.2.6.jar')

