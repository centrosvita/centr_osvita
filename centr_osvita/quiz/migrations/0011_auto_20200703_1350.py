# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-03 13:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_auto_20200603_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commonanswer',
            name='number',
            field=models.IntegerField(choices=[(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'E')], verbose_name='Answer Order'),
        ),
        migrations.AlterField(
            model_name='quizcommonanswer',
            name='number',
            field=models.IntegerField(choices=[(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'E')], verbose_name='Answer Order'),
        ),
    ]
