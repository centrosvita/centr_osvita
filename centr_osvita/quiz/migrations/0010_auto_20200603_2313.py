# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-06-03 23:13
from __future__ import unicode_literals

import centr_osvita.quiz.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0009_auto_20200603_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=centr_osvita.quiz.models.NON_POLYMORPHIC_CASCADE, to='quiz.Question', verbose_name='Question'),
        ),
        migrations.AlterField(
            model_name='quizanswer',
            name='quiz_question',
            field=models.ForeignKey(on_delete=centr_osvita.quiz.models.NON_POLYMORPHIC_CASCADE, to='quiz.QuizQuestion', verbose_name='Quiz Question'),
        ),
    ]