# Generated by Django 3.1.7 on 2021-05-21 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parserToPostgre', '0018_grouplistuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grouplistuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parserToPostgre.user', to_field='user_id', unique=True),
        ),
    ]