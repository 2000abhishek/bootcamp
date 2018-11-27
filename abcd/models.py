from django.db import models



# Create your models here.
class user_information(models.Model):
	First_Name=models.CharField(max_length=30)
	Last_Name=models.CharField(max_length=30)
	User_Name=models.CharField(max_length=40,primary_key=True)
	Pass_Word=models.CharField(max_length=40)
	Email=models.CharField(max_length=50)
	Mobile_no=models.CharField(max_length=20)
	

class first_level_comment(models.Model):
	User_Name=models.CharField(max_length=40)
	User_Comment=models.CharField(max_length=1000)
	Current_Time= models.DateTimeField(auto_now_add=True)

class first_level_like(models.Model):
	User_Name=models.CharField(max_length=40)
	User_Comment_ID=models.IntegerField()

class second_level_comment(models.Model):
	User_Name=models.CharField(max_length=40)
	User_Comment_ID=models.IntegerField()
	User_Comment_Post=models.CharField(max_length=1000)
