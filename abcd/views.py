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
from abcd.models import comment_send

from django.template import RequestContext

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
		abc = (comment_send.objects.all())
		rows=[]
		
		for i in abc:
			row={}
			row['User_Name']=i.User_Name
			row['User_Comment']=i.User_Comment
			rows.append(row)
			 
		return JsonResponse(rows,safe=False)
	except ValueError as e:
		return Response(e.args[0],status.HTTP_400_BAD_REQUEST)

def Article(request):
	try:
		return render(request,"article.html")

	except ValueError as e:
		return Response(e.args[0],status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def comment_post(request):
	try:
		comment=json.loads(request.body) #json.loads converts json object or string into 
		print(comment)
		username=request.session['username']
		print(username)
		comment=comment['comment']
		print(comment)
		a=comment_send(User_Name=username,User_Comment=comment)
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