# file name : index.py
# pwd : /project_name/app/main/index.py
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as current_app

main = Blueprint('main', __name__, url_prefix='/')

@main.route('/main', methods = ['GET'])
def index():
    return render_template('/main/index.html')

# decorating index function with the app.route with url as /login
@main.route('/main/login', methods = ['GET'])
def login():
   return render_template('/main/login.html')


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
       Total_Point = '800'
       Credit_Rate = '2'
       return render_template('/main/success.html', Name=Name, Point = Point, Monthly_Point =Monthly_Point ,Attendance = Attendance,
                              Assignment = Assignment, Total = Total, Total_Point = Total_Point, Credit_Rate = Credit_Rate)
   else:
       pass
