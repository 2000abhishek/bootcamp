# Generated by Django 2.1.1 on 2018-10-28 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abcd', '0004_auto_20181028_0326'),
    ]

    operations = [
        migrations.CreateModel(
            name='debit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debit1', models.IntegerField()),
                ('credit1', models.IntegerField()),
            ],
        ),
    ]
