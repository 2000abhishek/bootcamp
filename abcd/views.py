# Create your views here.
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse,HttpResponse
from django.core import serializers
from django.conf import settings
import json
from django.core import serializers
from django.template.loader import get_template

from django.shortcuts import render
from abcd.models import user_information
from abcd.models import first_level_comment
from abcd.models import first_level_like
from django.template import RequestContext
from dateutil import tz
import datetime
import dateutil.relativedelta

import requests
import json

@api_view(["POST"])
def Signup(request):
	try: #IN AJAX CALL JSON DATA COMES IN request.body not in request.post.
		data=json.loads(request.body) #In AJAX CALL JSON DOES NOT CHANGE IN QUERYDICT LIKE FORM REQUEST SO WE PARSED IT IN DICT BY JAVASCRIPT FUNCTION json.loads()
		print(data)
		firstname=data['first-name']
		lastname=data['last-name']
		username=data['user-name']
		password=data['pass-word']
		email=data['e-mail']
		mobileno=data['mob-no']
		print(firstname)
		request.session['username']=username
		q=user_information(First_Name=firstname,Last_Name=lastname,User_Name=username,Pass_Word=password,Email=email,Mobile_no=mobileno)
		q.save()
		print ('abc')

		return Response("Hello")
	except ValueError as e:
		return Response(e.args[0],status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
def Login(request):
	try:
		a=json.loads(request.body)
		print(a)
		user_name=a['uname']
		password=a['psw']
		print('user_name')
		for i in user_information.objects.all():
			if i.User_Name==user_name and i.Pass_Word==password:
				request.session['username'] = user_name
				return HttpResponse('OK')
		
	except ValueError as e:
		return Response(e.args[0],status.HTTP_400_BAD_REQUEST)
		
from django.shortcuts import redirect
@api_view(["GET"])
def Home(request):

	if request.session.has_key('username'):
		username = request.session['username']
		response = redirect('/feed')
		return response
	else:
		return render(request, 'index.html', {})


@api_view(["GET"])
def Dashboard(request):
	try:
		return render(request,"dashboard.html")

	except ValueError as e:
		return Response(e.args[0],status.HTTP_400_BAD_REQUEST)
		

def track_user(request):
	if not request.COOKIES.get('visits'):
		response = HttpResponse("This is your first visit to the site. "
								"From now on I will track your vistis to this site.")
		response.set_cookie('visits', '1', 3600 * 24 * 365 * 2)
	else:
		visits = int(request.COOKIES.get('visits')) + 1
		response = HttpResponse("This is your {0} visit".format(visits))
		response.set_cookie('visits', str(visits),  3600 * 24 * 365 * 2)
	return response

def Feed(request):
	try:
		return render(request,"feed.html")

	except ValueError as e:
		return Response(e.args[0],status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def query(request):
	try:
		comment_set = first_level_comment.objects.all()
		
		liked=[]
		like_set = first_level_like.objects.all().filter(User_Name=request.session['username'])
		rows=[]
		for like_row in like_set:
			liked.append(like_row.User_Comment_ID)

		for comment_row in comment_set:
			row={}
			from_zone = tz.gettz('UTC')
			to_zone = tz.gettz('Asia/Kolkata')
			# utc = datetime.datetime.strptime(i.Current_Time, '%Y-%m-%d %H:%M:%S')
			# print(i.Current_Time)
			utc = comment_row.Current_Time.replace(tzinfo=from_zone)
			central = utc.astimezone(to_zone)
			
			comment_date=central.date()
			year=comment_row.Current_Time.year
			month=comment_row.Current_Time.month
			day=comment_row.Current_Time.day
			hour=comment_row.Current_Time.hour
			minute=comment_row.Current_Time.minute


			today=datetime.datetime.now()
			print(today)
			t_year=today.year
			t_month=today.month
			t_day=today.day
			t_hour=today.hour
			t_minute=today.minute

			d_year=t_year-year
			d_month=t_month-month
			d_day=t_day-day
			d_hour=t_hour-hour
			d_minute=t_minute-minute
		
			if d_minute<1 and d_hour==0 and d_day==0 and d_month==0 and d_year==0:
				time_ago="now"
			elif d_minute>=1 and d_hour==0 and d_day==0 and d_month==0 and d_year==0:
				time_ago=str(d_minute)+"min ago"
				print(time_ago)
			elif d_hour>=1 and d_day==0 and d_month==0 and d_year==0: 
				time_ago=str(d_hour)+"h ago"
				print(time_ago)
			elif d_day>=1 and d_month==0 and d_year==0:
				time_ago=str(d_day)+"d ago"
				print(time_ago)
			elif d_month>=1 and d_year==0:
				time_ago=str(d_month)+"mon ago"
				print(time_ago)
			elif d_year>=1:
				time_ago=str(d_year)+"y ago"
				print(time_ago)
			row['User_Comment_ID']=comment_row.id
			row['User_Name']=comment_row.User_Name
			row['User_Comment']=comment_row.User_Comment
			row['Current_Time']=time_ago
			rows.append(row)

		sending={}
		sending["comments"]=(rows)
		sending["liked"]=(liked)	
		return JsonResponse(sending,safe=False)
	except ValueError as e:
		return Response(e.args[0],status.HTTP_400_BAD_REQUEST)

def Article(request):
	try:
		return render(request,"article.html")

	except ValueError as e:
		return Response(e.args[0],status.HTTP_400_BAD_REQUEST)

import datetime
@api_view(["POST"])
def comment_post(request):
	try:
		comment=json.loads(request.body) #json.loads converts json object or string into 
		username=request.session['username']
		comment=comment['comment']
		now = datetime.datetime.now()
		a=first_level_comment(User_Name=username,User_Comment=comment,Current_Time=now)
		a.save()
		return HttpResponse("Done")
	except ValueError as e:
		return Response(e.args[0],status.HTTP_400_BAD_REQUEST)
		
from django.contrib.auth import logout
@api_view(["POST"])
def Logout(request):
	try:
		logout(request)
		return redirect('/home')
	except ValueError as e:
		return Response(e.args[0],status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def likeController(request):
	try:
		params=json.loads(request.body)
		print(params)
		username=request.session['username']
		print(username)
		ID=params['ID']
		print(ID)
		a=first_level_like(User_Name=username,User_Comment_ID=ID)
		a.save()
		return JsonResponse("ok",safe=False)
	except ValueError as e:
		print(e)
		return Response(e.args[0],status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def unlikeController(request):
	try:
		params=json.loads(request.body)
		print(params)
		username=request.session['username']
		ID=params['ID']
		print(ID)
		a=first_level_like.objects.all().filter(User_Comment_ID=ID).delete()
		print(a)
		return JsonResponse("OK",safe=False)
	except ValueError as e:
		return Response(e.args[0],status.HTTP_400_BAD_REQUEST)
