# Generated by Django 2.1.1 on 2018-10-25 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user_information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('First_Name', models.CharField(max_length=30)),
                ('Last_Name', models.CharField(max_length=30)),
                ('User_Name', models.CharField(max_length=40)),
                ('Pass_Word', models.CharField(max_length=40)),
                ('Email', models.CharField(max_length=50)),
                ('Mobile_no', models.IntegerField()),
            ],
        ),
    ]
