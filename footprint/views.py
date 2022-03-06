from django.shortcuts import render
import requests
import folium
import folium.plugins as plugins
import numpy as np
import time
import json
import pandas as pd
from django.shortcuts import redirect
from footprint.lstm_functions import predict

# from django.views.decorators.clickjacking import xframe_options_exempt

#
'''
Django 2.2

pyecharts  数据统计画图
folium 地图可视化
python  网页前端

app  Android studio
（高德框架map2d）
'''
# 首页
def home(request):
    return render(request, 'index.html')

# 智能可视化
def our_track_heat(request):
    return render(request, 'a1_ourtrack.html')


def our_track_line(request):
    return render(request,'a2_ourtrack.html')


def our_track_in_heat(request):
    get_all_new()
    return render(request,'ourmap_heat.html')


def our_track_in_line(request):
    get_all()
    return render(request,'ourmap_line.html')


# 个人轨迹
def my_track(request):
    return render(request,'a0_mytrack.html')


def my_track_in_(request):
    get_id(201)
    return render(request,'mymap.html')

def my_track_login(request):
    return render(request,'a3_mytrack_login.html')


def my_track_register(request):
    return render(request,'a4_mytrack_register.html')

# 统计数据
def statistic_data(request):
    return render(request,'a5_statistic_chart.html')

def function_introduction(request):
    return render(request,'a7_function_introduction.html')

def draw(request):
    return render(request,'draw.html')
from django.shortcuts import HttpResponse, render, redirect

def get_cookie(request):
    """获取cookie"""
    cookie = request.COOKIES['user']
    #url转义
    cookie_unquote = eval(urllib.parse.unquote(cookie))
    user_id = cookie_unquote['id']
    print("id是"+str(user_id))

    return HttpResponse(user_id)


# 人员查询功能
def personnel_search_with_status(request):
    #以防报错,首先赋初值
    status = None
    changed_status = None
    result_data = ''
    flag = 0
    normal_length = 0
    trouble_length = 0
    dangerous_length = 0
    if request.method == 'POST':
        #这里用于查询状态
        str_status = request.POST.get('status')
        if str_status == "正常":
            status = 0
        elif str_status == "密接":
            status = 1
        elif str_status == '患病':
            status = 2
        #这里用于改变状态
        user_id = request.POST.get('user_id')
        str_changed_status = request.POST.get('changed_status')
        print("userid是{},要改变的状态是{}".format(user_id,str_changed_status))
       
        
        if str_changed_status == '正常':
            changed_status = 0
        elif str_changed_status == '密接':
            changed_status = 1
        elif str_changed_status == '患病':
            changed_status = 2
    
    #查询状态连接后端
    try:
        url = "http://116.62.204.251:3/virus/user/userstatus{}".format(status)
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()['data']
            zldc = {"username":[],"phone_number":[],"id":[]}
            cols = {"username","phone_number","id"}
            for th in data:
                for col in cols:
                    zldc[col].append(th[col])
            result_data = [[name,phone,user_id,str_status] for name,phone,user_id in zip(zldc['username'],zldc['phone_number'],zldc["id"])]
            flag = 1
            for i in range(0,len(result_data)):
                for j in range(0,len(result_data[i])):
                    if result_data[i][j] == None:
                        result_data[i][j] = 'null'
                        
        # 统计数据
        for user_status in range(0,3):
            url = "http://116.62.204.251:3/virus/user/userstatus{}".format(user_status)
            res = requests.get(url)
            if res.status_code == 200:
                data = res.json()['data']
                zldc = {"username":[],"phone_number":[],"id":[]}
                cols = {"username","phone_number","id"}
            for th in data:
                for col in cols:
                    zldc[col].append(th[col])
            statistic_data = [[name,phone,user_id,str_status] for name,phone,user_id in zip(zldc['username'],zldc['phone_number'],zldc["id"])]
            if user_status == 0:
                normal_length = len(statistic_data)
            elif user_status == 1:
                trouble_length = len(statistic_data)
            elif user_status == 2:
                dangerous_length = len(statistic_data)
                
    except:
        pass
    
    #修改状态连接后端
    try:
        ip = "http://116.62.204.251:3/virus/"
        user_information_url = ip + "user/userid/{}".format(user_id)
        user_information = requests.get(user_information_url)
        user_information_res = requests.get(user_information_url)
        if user_information_res.status_code == 200:
            data = user_information_res.json()['data']
        simplify_information = {'phone_number':data['phone_number'],'status':data['status'],'username':data['username']}
        simplify_information['status'] = changed_status
        user_information_updated_url = ip + "user/update/{}".format(user_id)
        params = simplify_information
        payload = json.dumps(params)
        #这里很重要,需要将header设置为这种形式。
        headers_put = {
            'Content-Type':"application/json"}
        user_information_updated_res = requests.put(user_information_updated_url,data = payload,headers=headers_put)
    except:
        pass

    return render(request,'a6_admin_search.html',{"result_data":result_data,"flag":flag,"normal":normal_length,"trouble":trouble_length,"dangerous":dangerous_length})

# 轨迹时间查询功能
from django.http import JsonResponse

def get_searched_data(request):
    searched_data = []
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    try:
        #首先获取cookies，得到用户id信息。
        cookies = request.COOKIES['user'].replace('null','None')
        #url转义
        cookies_unquote = eval(urllib.parse.unquote(cookies))
        user_id = cookies_unquote['id']
        url = "http://116.62.204.251:3/virus/track/idtime1time2?id={}&time1={}%20{}%3A{}%3A00&time2={}%20{}%3A{}%3A00".format(user_id,start_date.split("T")[0],start_date.split("T")[1].split(":")[0],start_date.split("T")[1].split(":")[1],end_date.split("T")[0],end_date.split("T")[1].split(":")[0],end_date.split("T")[1].split(":")[1])
        res = requests.post(url)
        if res.status_code == 200:
            data = res.json()['data']
            zldc = {"track_id": [], "user_id": id, "lng": [], "lat": [], "track_time": [], "track_name": []}
            cols = ["track_id", "lng", "lat", "track_time", "track_name"]
            for th in data:
                for col in cols:
                    zldc[col].append(th[col])
            searched_data = [[x,y] for x,y in zip(zldc['lat'], zldc['lng'])]
    except:
        pass
    return JsonResponse({"code": 200, "msg": "成功", "searched_data" : searched_data,"user_length":len(searched_data)})

# 轨迹总和返回函数
def track_total(request):
    locations,track_name,track_time,user_length,simulated = track_find(request)
    flag,pat_data,patient_length,patient_simulated,patient_track_name,patient_track_time = track_cross(request)
    predict_data,predict_length = track_predict()
    
    return render(request, 'a8_predict_track.html',
                  {"patient_track_name":patient_track_name,"patient_track_time":patient_track_time,"patient_simulated_flag":patient_simulated,"user_simulated_flag":simulated,"data": locations, "track_name": track_name,
                   "track_time": track_time, "user_length": user_length, "patient_length": patient_length,
                   "predict_length": predict_length, "cross_flag": flag, "pat_data": pat_data,
                   "predict_data": predict_data})
import urllib
# 查看自己轨迹
def track_find(request):
    #防止报错，赋初值
    locations = []
    track_name = 'null'
    track_time = 'null'
    user_length = 'null'
    simulated = 'null'
    # 这里有一个坑需要注意，js和python中分别是没有None和null类型的，因此在互传参数时，需要提前将null和None进行对换。
    try:
        #首先获取cookies，得到用户id信息。
        cookies = request.COOKIES['user'].replace('null','None')
        #url转义  
        cookies_unquote = eval(urllib.parse.unquote(cookies))
        user_id = cookies_unquote['id']
        url = "http://116.62.204.251:3/virus/track/findTracks{}".format(user_id)
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()['data']
        # 从data中拆出需要的信息:轨迹id,轨迹点坐标,轨迹时间,轨迹地点名。
        zldc = {"track_id": [], "user_id": [], "lng": [], "lat": [], "track_time": [], "track_name": [],'simulated':[]}
        cols = ["track_id", "lng", "lat", "track_time", "track_name",'simulated']
        for th in data:
            for col in cols:
                zldc[col].append(th[col])
        else:
            print("id 不存在，未成功响应")
        locations = [[la, ln] for la, ln in zip(zldc['lat'], zldc['lng'])]
        track_name = zldc["track_name"]
        track_time = [time[:-10] for time in zldc["track_time"]]
        user_length = len(locations)
        simulated = zldc["simulated"][0]
    except:
        pass
    
    return locations,track_name,track_time,user_length,simulated
    

# 交叉轨迹 这里id1传入的为用户id,id2传入病患id;且该函数的返回数据为病患曲线
def track_cross(request,dis=100,id2=301,time=100):
    #同样先赋值
    flag = 'null'
    locations = []
    patient_length = 'null'
    patient_simulated_flag = 'null'
    patient_track_name = 'null'
    patient_track_time = 'null'
    #查询病患轨迹信息
    url1 = "http://116.62.204.251:3/virus/track/findTracks{}".format(id2)
    res1 = requests.get(url1)
    if res1.status_code == 200:
        data1 = res1.json()['data']
    #从data中拆出需要的信息:轨迹id,轨迹点坐标,轨迹时间,轨迹地点名。
        zldc = {"track_id": [], "user_id": id, "lng": [], "lat": [], "track_time": [], "track_name": [],'simulated':[]}
        cols = ["track_id", "lng", "lat", "track_time", "track_name",'simulated']
        for th in data1:
            for col in cols:
                zldc[col].append(th[col])
        locations = [[la, ln] for la, ln in zip(zldc['lat'], zldc['lng'])]
        patient_track_name = zldc["track_name"]
        patient_track_time = [time[:-10] for time in zldc["track_time"]]
        patient_simulated_flag = zldc["simulated"][0]
                
    else:
        print("id 不存在，未成功响应")
    # 这里为判断是否存在交叉
    try:
        cookies = request.COOKIES['user'].replace('null','None')
        #url转义
        cookies_unquote = eval(urllib.parse.unquote(cookies))
        id1 = cookies_unquote['id']
        url2 = "http://116.62.204.251:3/virus/meet/userconflict?dis={}&id1={}&id2={}&time={}".format(dis,id1,id2,time)
        res2 = requests.get(url2)
        if res2.status_code == 200:
            data2 = res2.json()['data']
        if data2 != None:
            flag = 1
        else:
            flag = 0
    except:
        pass
    patient_length = len(locations)
    
    return flag,locations,patient_length,patient_simulated_flag,patient_track_name,patient_track_time

# 预测轨迹
def track_predict(id=301):
    url = "http://116.62.204.251:3/virus/track/findTracks{}".format(id)
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()['data']
    
    #从data中拆出需要的信息:轨迹id,轨迹点坐标,轨迹时间,轨迹地点名。
    zldc = {"track_id": [], "user_id": id, "lng": [], "lat": [], "track_time": [], "track_name": []}
    cols = ["track_id", "lng", "lat", "track_time", "track_name"]
    for th in data:
        for col in cols:
            zldc[col].append(th[col])
    location = pd.DataFrame([zldc["lat"],zldc["lng"]]).T
    location = location.rename(columns={0:"x",1:"y"})
    out = predict(location,20)
    predict_data = [[x,y] for x,y in zip(out['x'],out['y'])]
    predict_length = len(predict_data)
    return predict_data,predict_length

def get_all_new():
    # 时间序列表 open
    time_time = []
    [end_y, end_m] = [int(i) for i in time.strftime('%Y-%m', time.localtime(time.time())).split('-')]
    time_end = str(end_y) + '-' + str(end_m)
    time_year, time_month = 2020, 1
    t = str(time_year) + '-' + str(time_month)
    while t != time_end:
        time_month = ((time_month - 1) % 12) + 1
        t = str(time_year) + '-' + str(time_month)
        time_time.append(t + '-1')
        time_year += time_month // 12
        time_month += 1
    # end  time_time
    all_data = []

    for ti in range(len(time_time) - 1):
        t1, t2 = time_time[ti], time_time[ti + 1]
        url = "http://116.62.204.251:3/virus/track/findTrackstime?time1={}&time2={}".format(t1, t2)
        res = requests.post(url)
        sample_data = []
        if res.status_code == 200:
            path = 'templates/ourmap_heat.html'
            data = res.json()['data']
            for d in data:
                sample_data.append([d['lat'], d['lng'], 10])
        else:
            print("time-time 不符合规则,未成功响应.")
        all_data.append(sample_data)
    for i in range(len(all_data)):
        if len(all_data[i]) == 0:
            all_data[i] = [[0, 0, 1]]
    lat_list = []
    lng_list = []
    for o1 in all_data:
        for o2 in o1:
            if o2[0] != 0:
                lat_list.append(o2[0])
                lng_list.append(o2[1])
    center_lat, center_lng = np.mean(lat_list), np.mean(lng_list)
    m = folium.Map([center_lat, center_lng], zoom_start=8, attr='default',
                   control_scale=True,
                   # tiles="stamentoner",
                   )
    hm = plugins.HeatMapWithTime(all_data, index=time_time[1:], auto_play=True, max_opacity=0.3)
    hm.add_to(m)
    m.save(path)
    fix_https(path)


def get_all():
    [end_y, end_m] = [int(i) for i in time.strftime('%Y-%m', time.localtime(time.time())).split('-')]
    t1, t2 = '2020-1-1', str(end_y) + '-' + str(end_m) + '-1'
    url = "http://116.62.204.251:3/virus/track/findTrackstime?time1={}&time2={}".format(t1, t2)
    res = requests.post(url)
    if res.status_code == 200:
        path = 'templates/ourmap_line.html'
        data = res.json()['data']
        zldata = dict()
        for track in data:
            if track['user_id'] not in zldata.keys():
                zldata[track['user_id']] = [track]
            else:
                zldata[track['user_id']].append(track)

        center_lat, center_lng = np.mean([x1['lat'] for x1 in data]), np.mean([x2['lng'] for x2 in data])
        # folium绘图
        # tile参数调整地图是高德还是什么
        m = folium.Map([center_lat, center_lng], zoom_start=10, attr='default')
        for id, id_track in zldata.items():
            zldc = {"track_id": [], "lng": [], "lat": [], "track_time": [], "track_name": []}
            cols = ["track_id", "lng", "lat", "track_time", "track_name"]
            for th in id_track:
                for col in cols:
                    zldc[col].append(th[col])
            tk = [[la, ln] for la, ln in zip(zldc['lat'], zldc['lng'])]
            folium.PolyLine(  # polyline方法为将坐标用实线形式连接起来
                tk,  # 将坐标点连接起来
                weight=4,  # 线的大小为4
                color='blue',  # 线的颜色为红色
                opacity=0.8,  # 线的透明度
            ).add_to(m)  # 将这条线添加到刚才的区域m内

            folium.PolyLine(  # polyline方法为将坐标用虚线形式连接起来
                tk,  # 将坐标点连接起来
                weight=2,  # 线的大小为2
                color='red',  # 线的颜色为蓝色
                opacity=0.8,  # 线的透明度
                dash_array='5'  # 虚线频率
            ).add_to(m)  # 将这条线添加到刚才的区域m内

        m.save(path)  # 将结果以HTML形式保存到指定路径
        fix_https(path)
    else:
        print("time-time 不符合规则,未成功响应.")

def get_id(id):
    
    url = "http://116.62.204.251:3/virus/track/findTracks{}".format(id)
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()['data']
        # 部分
        zldc = {"track_id": [], "user_id": id, "lng": [], "lat": [], "track_time": [], "track_name": []}
        cols = ["track_id", "lng", "lat", "track_time", "track_name"]
        for th in data:
            for col in cols:
                zldc[col].append(th[col])
        path = 'templates/mymap.html'

        plot_map(zldc, path)
        fix_https(path)
    else:
        print("id 不存在,未成功响应.")


def plot_map(data, path):
    tk = [[la, ln] for la, ln in zip(data['lat'], data['lng'])]
    m = folium.Map([np.mean(data['lat']), np.mean(data['lng'])], zoom_start=12, attr='default')
    folium.PolyLine(  # polyline方法为将坐标用实线形式连接起来
        tk,  # 将坐标点连接起来
        weight=4,  # 线的大小为4
        color='blue',  # 线的颜色为红色
        opacity=0.8,  # 线的透明度
    ).add_to(m)  # 将这条线添加到刚才的区域m内

    folium.PolyLine(  # polyline方法为将坐标用虚线形式连接起来
        tk,  # 将坐标点连接起来
        weight=2,  # 线的大小为2
        color='red',  # 线的颜色为蓝色
        opacity=0.8,  # 线的透明度
        dash_array='5'  # 虚线频率
    ).add_to(m)  # 将这条线添加到刚才的区域m内

    # 起始点，结束点
    for ll, p, t in zip(tk, data["track_name"], data["track_time"]):
        folium.Marker(ll,
                      # icon=folium.Icon(color="green"),
                      popup='<b>地点: {}<br>时间: {}</b>'.format(p, t[:-10])).add_to(m)

    m.save(path)  # 将结果以HTML形式保存到指定路径

def fix_https(path):
    with open(path, 'rb+') as f:
        text = f.read().decode()
        oldtext = ["https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/",
                   "https://code.jquery.com/",
                   "https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/",
                   "https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/",
                   "https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/",
                   "https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/",
                   "https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/",
                   "https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/",
                   "https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/",
                   "https://rawcdn.githack.com/python-visualization/folium/master/folium/templates/",
                   "https://rawcdn.githack.com/nezasa/iso8601-js-period/master/",
                   "https://rawcdn.githack.com/socib/Leaflet.TimeDimension/master/dist/",
                   "https://rawcdn.githack.com/python-visualization/folium/master/folium/templates/",
                   "https://rawcdn.githack.com/python-visualization/folium/master/folium/templates/",
                   "https://rawcdn.githack.com/socib/Leaflet.TimeDimension/master/dist/"
                   ]
        for t in oldtext:
            text = text.replace(t, "/static/folium/")
    f.close()
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    f.close()
