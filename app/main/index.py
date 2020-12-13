# file name : index.py
# pwd : /project_name/app/main/index.py
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as current_app
from matplotlib import pyplot as plt
import re
import math
import pandas as pd
import numpy as np
from scipy.stats import norm

main = Blueprint('main', __name__, url_prefix='/')

@main.route('/main', methods = ['GET'])
def index():
    return render_template('/main/index.html')

# decorating index function with the app.route with url as /login
@main.route('/main/login', methods = ['GET'])
def login():
   return render_template('/main/login.html')


def Credit_Rating(point):
    rv = norm(loc=650, scale=300)
    if (point <= rv.ppf(0.99999)) & (point >= rv.ppf(0.95)):
        y = '1'
    elif (point <= rv.ppf(0.95)) & (point >= rv.ppf(0.85)):
        y = '2'
    elif (point <= rv.ppf(0.85)) & (point >= rv.ppf(0.7)):
        y = '3'
    elif (point <= rv.ppf(0.7)) & (point >= rv.ppf(0.5)):
        y = '4'
    elif (point <= rv.ppf(0.5)) & (point >= rv.ppf(0.3)):
        y = '5'
    elif (point <= rv.ppf(0.3)) & (point >= rv.ppf(0.15)):
        y = '6'
    elif (point <= rv.ppf(0.15)) & (point >= rv.ppf(0.05)):
        y = '7'
    elif (point <= rv.ppf(0.05)) & (point >= rv.ppf(0.00001)):
        y = '8'
    return y

def Calculate_Rest_Point(point):
    level = Credit_Rating(point)
    rv = norm(loc = 650, scale = 300)
    if level == '1':
        y = 0
    elif level == '2':
        y= rv.ppf(0.95) - point
    elif level == '3':
        y= rv.ppf(0.85) - point
    elif level == '4':
        y= rv.ppf(0.7)- point
    elif level == '5':
        y= rv.ppf(0.5)- point
    elif level == '6':
        y= rv.ppf(0.3)- point
    elif level == '7':
        y= rv.ppf(0.15)- point
    elif level == '8':
        y= rv.ppf(0.05)- point
    return int(y)



def Draw_Distribution(username, point):

    plt.style.use('default')
    plt.rcParams['figure.figsize'] = (6, 3)
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.family'] = 'NanumGothic'
    plt.rcParams['font.size'] = 12
    plt.rcParams['lines.linewidth'] = 5

    rv = norm(loc=650, scale=300)
    x = np.arange(0, 1800, 1)
    y = rv.pdf(x)
    fig, ax = plt.subplots(1, 1)
    plt.plot(x, y, alpha=0.7, label=r"잇츠미 사용자 분포")
    plt.xlabel("It's Me 포인트")
    plt.ylabel('사용자 누적 비율')
    plt.title("{}님의 신용분포".format(username))

    # 사용자 위치 표시
    percent = 1 - rv.cdf(point)  # 퍼센트 구하기
    score = rv.ppf(percent)  # 퍼센트 x값 구하기
    x_score = np.arange(score, x.max() + 1, 1)  # range 만들기
    y_score = rv.pdf(x_score)  # 범위에 따른 확률값 구하기

    ax.vlines(x_score, 0, y_score, colors='steelblue', lw=5, label="{}님 현재 위치".format(username))
    plt.legend(bbox_to_anchor=(0.7, 0.95), fontsize=8)

    file_save = "./app/static/img/dist/" + username + '-dist.jpg'
    plt.savefig(file_save, bbox_inches='tight')
    plt.clf()

    return file_save


def create_x(t, w, n, d):
    return [t * x + w * n for x in range(d)]


def Draw_BarChart(username, user_df):

    plt.style.use('default')
    plt.rcParams['figure.figsize'] = (6, 3)
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.family'] = 'NanumGothic'
    plt.rcParams['font.size'] = 10
    plt.rcParams['lines.linewidth'] = 5

    topics = ['종합(%)', '과제제출(%)', '출석(%)']
    avg = [89.28, 88.51, 90.05]
    user = user_df
    avg_x = create_x(2, 0.8, 1, 3)
    user_x = create_x(2, 0.8, 2, 3)

    ax = plt.subplot()
    ax.bar(avg_x, avg, facecolor='#9999ff', edgecolor='white')
    ax.bar(user_x, user, facecolor='#ff9999', edgecolor='white')

    for x, y in zip(avg_x, avg):
        plt.text(x - 0.01, y + 4.5, '{}%'.format(y), ha='center', va='top', fontsize=7.5)

    for x, y in zip(user_x, user):
        plt.text(x + 0.01, y + 4.5, '{}%'.format(y), ha='center', va='top', fontsize=7.5)

    middle_x = [(a + b) / 2 for (a, b) in zip(avg_x, user_x)]
    ax.set_xticks(middle_x)
    ax.set_xticklabels(topics)

    plt.xlabel('평가기준')
    plt.ylabel('퍼센트(%)')
    plt.legend(['평균', username], loc='upper center', bbox_to_anchor=(0.9, 0.25), ncol=1, fontsize=9)

    plt.title("{}님의 학교생활 데이터".format(username))

    file_save = "./app/static/img/barchart/" + username + '-barchart.jpg'
    plt.savefig(file_save, bbox_inches='tight')
    plt.clf()

    return file_save

Name = 'SuWanKim' ; Point = 800 ; user_df = [97.43, 94.85, 100.0]
Draw_Distribution(Name, Point)
Draw_BarChart(Name, user_df)

@main.route('/success',  methods=['POST'])
def success():
   if request.method == 'POST':
       Name = request.form['Name']
       # It's Me 계좌에서 가지고 올 값
       Point = '12'
       Monthly_Point  = '50'
       # 출석 페이지, 과제 페이지에서 가져올 값
       Attendance  = '100'
       Assignment = '94.85'
       Total = '97.43'
       # 최종 누계 포인트와 신용 등급 값
       Total_Point = 800
       # 퍼센트 계산
       rv = norm(loc = 650, scale = 300)
       percent = round(100 - rv.cdf(Total_Point) * 100, 2)

       # 신용등급 계산
       Credit_Rate = Credit_Rating(Total_Point)
       # 나머지 점수 계산
       rest = Calculate_Rest_Point(Total_Point)

       return render_template('/main/success.html', Name=Name, Point = Point, Monthly_Point =Monthly_Point ,Attendance = Attendance,
                              Assignment = Assignment, Total = Total, Total_Point = Total_Point, percent= percent, Credit_Rate = Credit_Rate,
                              rest = rest)
   else:
       pass

