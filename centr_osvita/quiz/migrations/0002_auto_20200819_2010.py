# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-08-19 20:10
from __future__ import unicode_literals

import centr_osvita.quiz.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('profiles', '0004_auto_20200710_1403'),
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', models.IntegerField(choices=[(0, 'In Progress'), (1, 'Done'), (2, 'Suspend')], default=0, verbose_name='Status')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='profiles.Profile', verbose_name='Student')),
            ],
            options={
                'verbose_name': 'Quiz',
                'verbose_name_plural': 'Quizzes',
            },
        ),
        migrations.CreateModel(
            name='QuizAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
            ],
            options={
                'verbose_name': 'Quiz Answer',
                'verbose_name_plural': 'Quiz Answers',
                'manager_inheritance_from_future': True,
            },
        ),
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', models.IntegerField(choices=[(0, 'Active'), (1, 'Done'), (2, 'Suspend')], default=0, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Quiz Question',
                'verbose_name_plural': 'Quiz Questions',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(help_text='Maximum length is 255 symbols', max_length=255, verbose_name='Test name')),
                ('status', models.BooleanField(verbose_name='Publish status')),
            ],
            options={
                'verbose_name': 'Test',
                'verbose_name_plural': 'Tests',
            },
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.SmallIntegerField(verbose_name='Year info')),
            ],
        ),
        migrations.CreateModel(
            name='YearSubjectStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent_c', models.FloatField(verbose_name='Percent of pupils that have C mark')),
                ('percent_b', models.FloatField(verbose_name='Percent of pupils that have B mark')),
                ('percent_a', models.FloatField(verbose_name='Percent of pupils that have A mark')),
            ],
        ),
        migrations.RemoveField(
            model_name='orderanswer',
            name='number',
        ),
        migrations.RemoveField(
            model_name='question',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='created',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='modified',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='status',
        ),
        migrations.AddField(
            model_name='commonanswer',
            name='number',
            field=models.IntegerField(choices=[(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'E')], null=True, verbose_name='Answer Order'),
        ),
        migrations.AddField(
            model_name='orderanswer',
            name='number_1',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')], null=True, verbose_name='Answer FIRST Position'),
        ),
        migrations.AddField(
            model_name='orderanswer',
            name='number_2',
            field=models.IntegerField(choices=[(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D')], null=True, verbose_name='Answer SECOND Position'),
        ),
        migrations.AddField(
            model_name='subject',
            name='slug',
            field=models.SlugField(null=True, verbose_name='Slug name'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=centr_osvita.quiz.models.NON_POLYMORPHIC_CASCADE, to='quiz.Question', verbose_name='Question'),
        ),
        migrations.AlterField(
            model_name='commonanswer',
            name='correct',
            field=models.BooleanField(verbose_name='Correct answer'),
        ),
        migrations.AlterField(
            model_name='mappinganswer',
            name='number_1',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (0, '0')], null=True, verbose_name='First chain'),
        ),
        migrations.AlterField(
            model_name='mappinganswer',
            name='number_2',
            field=models.IntegerField(choices=[(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'E')], null=True, verbose_name='Second chain'),
        ),
        migrations.CreateModel(
            name='QuizCommonAnswer',
            fields=[
                ('quizanswer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='quiz.QuizAnswer')),
                ('number', models.IntegerField(choices=[(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'E')], verbose_name='Answer Order')),
            ],
            options={
                'verbose_name': 'Quiz Common Answer',
                'verbose_name_plural': 'Quiz Common Answers',
                'manager_inheritance_from_future': True,
            },
            bases=('quiz.quizanswer',),
        ),
        migrations.CreateModel(
            name='QuizMappingAnswer',
            fields=[
                ('quizanswer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='quiz.QuizAnswer')),
                ('number_1', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (0, '0')], verbose_name='First chain')),
                ('number_2', models.IntegerField(choices=[(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'E')], verbose_name='Second chain')),
            ],
            options={
                'verbose_name': 'Quiz Mapping Answer',
                'verbose_name_plural': 'Quiz Mapping Answers',
                'manager_inheritance_from_future': True,
            },
            bases=('quiz.quizanswer',),
        ),
        migrations.CreateModel(
            name='QuizOrderAnswer',
            fields=[
                ('quizanswer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='quiz.QuizAnswer')),
                ('number_1', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')], verbose_name='Answer FIRST Position')),
                ('number_2', models.IntegerField(choices=[(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D')], verbose_name='Answer SECOND Position')),
            ],
            options={
                'verbose_name': 'Quiz Order Answer',
                'verbose_name_plural': 'Quiz Order Answers',
                'manager_inheritance_from_future': True,
            },
            bases=('quiz.quizanswer',),
        ),
        migrations.AddField(
            model_name='yearsubjectstatistics',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to='quiz.Subject', verbose_name='Subject'),
        ),
        migrations.AddField(
            model_name='yearsubjectstatistics',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to='quiz.Year', verbose_name='Year'),
        ),
        migrations.AddField(
            model_name='test',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='quiz.Subject', verbose_name='Subject'),
        ),
        migrations.AddField(
            model_name='quizquestion',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_questions', to='quiz.Question', verbose_name='Question'),
        ),
        migrations.AddField(
            model_name='quizquestion',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_questions', to='quiz.Quiz', verbose_name='Quiz'),
        ),
        migrations.AddField(
            model_name='quizanswer',
            name='answer',
            field=models.ForeignKey(on_delete=centr_osvita.quiz.models.NON_POLYMORPHIC_CASCADE, related_name='quiz_answers', to='quiz.Answer', verbose_name='Answer'),
        ),
        migrations.AddField(
            model_name='quizanswer',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_quiz.quizanswer_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='quizanswer',
            name='quiz_question',
            field=models.ForeignKey(on_delete=centr_osvita.quiz.models.NON_POLYMORPHIC_CASCADE, to='quiz.QuizQuestion', verbose_name='Quiz Question'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='quiz.Test', verbose_name='Test'),
        ),
        migrations.AddField(
            model_name='question',
            name='test',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quiz.Test', verbose_name='Test'),
        ),
    ]
