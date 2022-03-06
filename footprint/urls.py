"""amap2d_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from footprint import views

urlpatterns = [
    # 主页
    path('index/', views.home, name='home'),
    # 个人轨迹
    path('my_track/', views.my_track, name='my_track'),
    path('my_track/my_track_in_/', views.my_track_in_, name='my_track_in_'),
    path('my_track/login', views.my_track_login, name='my_track_login'),
    path('my_track/register',views.my_track_register, name='my_track_register'),
    # 智能可视化解析
    path('our_track_line/', views.our_track_line, name='our_track_line'),
    path('our_track_heat/', views.our_track_heat, name='our_track_heat'),
    path('our_track_line/our_track_in_line/', views.our_track_in_line, name='our_track_in_line'),
    path('our_track_heat/our_track_in_heat/', views.our_track_in_heat, name='our_track_in_heat'),
    # pyechart 统计可视化
    path('statistic_data/',views.statistic_data,name = 'statistic_data'),
    # 人员查询
    path('personnel_search_with_status/',views.personnel_search_with_status,name = 'personnel_search_with_status'),
    # 功能介绍
    path('function_introduction/',views.function_introduction,name = "function_introduction"),
    # 智能轨迹预测
    path('my_track/predict',views.track_total,name ='track_total'),
    # 智能轨迹预测 ——时间查询: 
    path('get_searched_data/',views.get_searched_data,name='get_searched_data'),
    # cookie测试
    path('get_cookie/',views.get_cookie,name='get_cookie'),
    # draw测试
    path('draw/',views.draw,name='draw')
]
