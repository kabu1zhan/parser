# Generated by Django 3.1.7 on 2021-04-16 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parserToPostgre', '0009_auto_20210416_1832'),
    ]

    operations = [
        migrations.CreateModel(
            name='BadData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('bad_word', models.TextField()),
            ],
        ),
    ]