from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.views.generic import ListView, View
from django.views.generic.detail import DetailView
from django.http import Http404
from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta

from centr_osvita.quiz.forms import AnswerForm, OrderAnswerForm, AnswerValidatedFormSet
from centr_osvita.quiz.mixins import IsStaffRequiredMixin
from centr_osvita.quiz.models import Quiz, Test, Question, QUESTION_TYPES, QuizCommonAnswer, \
    QuizOrderAnswer, OrderAnswer, QuizMappingAnswer, MappingAnswer, QuizQuestion, CommonAnswer
from centr_osvita.profiles.models import UserReport


class QuizResultView(IsStaffRequiredMixin, DetailView):
    model = Quiz
    template_name = 'quiz/results.html'
    queryset = Quiz.objects.filter(status__in=(Quiz.QUIZ_STATUS_TYPES.suspend, Quiz.QUIZ_STATUS_TYPES.done))


class ProfileReportsView(IsStaffRequiredMixin, DetailView):
    model = UserReport
    template_name = 'quiz/reports.html'
    queryset = UserReport.objects.all()


class TestListView(LoginRequiredMixin, ListView):
    model = Test
    template_name = 'quiz/test_list.html'

    def get_queryset(self):
        subject_param = self.request.GET.get('subject')
        object_list = Test.objects.filter(status=True)
        if subject_param:
            object_list = object_list.filter(subject__slug=subject_param)
        return object_list


class TestView(LoginRequiredMixin, View):
    template_name = 'quiz/test_detail.html'
    current_question = None
    current_quiz = None
    instance = None
    current_formset = None

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        self.instance = Test.objects.filter(pk=pk, status=True).first()
        if not self.instance:
            raise Http404(_("Not found"))
        if not Quiz.objects.filter(student=request.user.profile, status=Quiz.QUIZ_STATUS_TYPES.progress).count():
            quiz = Quiz.objects.create(test=self.instance, student=request.user.profile)
            quiz.create_random_quiz_questions()

        self.current_quiz = Quiz.objects.filter(student=self.request.user.profile,
                                                status=Quiz.QUIZ_STATUS_TYPES.progress).first()
        available_question_ids = self.current_quiz.quiz_questions.filter(
            status=QuizQuestion.QUIZ_QUESTION_STATUS_TYPES.active).values_list('question__id', flat=True)

        self.current_question = Question.objects.filter(test=self.instance, type=QUESTION_TYPES.common).filter(
            id__in=available_question_ids).first()
        if not self.current_question:
            self.current_question = Question.objects.filter(test=self.instance, type=QUESTION_TYPES.order).filter(
                id__in=available_question_ids).first()
        if not self.current_question:
            self.current_question = Question.objects.filter(test=self.instance, type=QUESTION_TYPES.mapping).filter(
                id__in=available_question_ids).first()

        self.current_formset = None
        if self.current_question is not None:
            if self.current_question.type == QUESTION_TYPES.common:
                CommonAnswerFormSet = formset_factory(AnswerForm)
                self.current_formset = CommonAnswerFormSet()
            elif self.current_question.type == QUESTION_TYPES.order:
                OrderAnswerFormSet = formset_factory(OrderAnswerForm, formset=AnswerValidatedFormSet,
                                                     extra=self.current_question.answer_set.count())
                self.current_formset = OrderAnswerFormSet()
            else:
                MappingAnswerFormSet = formset_factory(AnswerForm, formset=AnswerValidatedFormSet,
                                                       extra=self.current_question.ordered_answers_by_position.exclude(
                                                           number_1=MappingAnswer.FIRST_CHAIN_TYPES.zero).count())
                self.current_formset = MappingAnswerFormSet()

        if not self.current_question:
            return redirect('quiz:quiz-finish', self.current_quiz.id)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = dict()
        context['object'] = self.instance
        context['question'] = self.current_question
        context['quiz'] = self.current_quiz
        context['formset'] = self.current_formset
        context['current_question_number'] = self.current_quiz.quiz_questions.filter(
            status=QuizQuestion.QUIZ_QUESTION_STATUS_TYPES.done).count() + 1
        context['max_question_number'] = self.current_quiz.quiz_questions.count()
        if timezone.now() < self.current_quiz.created + \
                timedelta(minutes=self.current_quiz.test.test_parameter.test_time):
            context['time_left'] = int((self.current_quiz.created +
                                    timedelta(minutes=self.current_quiz.test.test_parameter.test_time) -
                                    timezone.now()).total_seconds())
        else:
            context['time_left'] = 0
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = dict()
        formset = None
        order_chain_list = ['first', 'second', 'third', 'fourth']
        if self.current_question is not None:
            if self.current_question.type == QUESTION_TYPES.common:
                CommonAnswerFormSet = formset_factory(AnswerForm)
                formset = CommonAnswerFormSet(request.POST)
            elif self.current_question.type == QUESTION_TYPES.order:
                OrderAnswerFormSet = formset_factory(OrderAnswerForm, formset=AnswerValidatedFormSet,
                                                     extra=self.current_question.answer_set.count())
                formset = OrderAnswerFormSet(request.POST)
            else:
                MappingAnswerFormSet = formset_factory(AnswerForm, formset=AnswerValidatedFormSet,
                                                       extra=self.current_question.ordered_answers_by_position.exclude(
                                                           number_1=MappingAnswer.FIRST_CHAIN_TYPES.zero).count())
                formset = MappingAnswerFormSet(request.POST)

        if formset.is_valid():
            quiz_question = QuizQuestion.objects.filter(quiz=self.current_quiz, question=self.current_question,
                                                        status=QuizQuestion.QUIZ_QUESTION_STATUS_TYPES.active).first()
            quiz_question.status = QuizQuestion.QUIZ_QUESTION_STATUS_TYPES.done
            quiz_question.save()
            answers_ids = self.current_question.answer_set.values_list('id', flat=True)
            if self.current_question.type == QUESTION_TYPES.common:
                answer = CommonAnswer.objects.filter(id__in=answers_ids,
                                                     number=formset.cleaned_data[0]['position']).first()
                QuizCommonAnswer.objects.create(quiz_question=quiz_question, number=formset.cleaned_data[0]['position'],
                                                answer=answer)
            elif self.current_question.type == QUESTION_TYPES.order:
                for key, form_data in enumerate(formset.cleaned_data):
                    answer = OrderAnswer.objects.filter(id__in=answers_ids,
                                                        number_1=getattr(OrderAnswer.ORDER_FIRST_CHAIN,
                                                                         order_chain_list[key])).first()
                    QuizOrderAnswer.objects.create(quiz_question=quiz_question,
                                                   number_2=form_data['position'],
                                                   number_1=answer.number_1, answer=answer)
            else:
                key_list = []
                for key, form_data in enumerate(formset.cleaned_data):
                    key_list.append(int(form_data['position']))
                    answer = MappingAnswer.objects.filter(id__in=answers_ids,
                                                          number_1=getattr(MappingAnswer.FIRST_CHAIN_TYPES,
                                                                           order_chain_list[key])).first()
                    QuizMappingAnswer.objects.create(quiz_question=quiz_question,
                                                     number_2=form_data['position'],
                                                     number_1=answer.number_1, answer=answer)

                answers_zero_position_one = MappingAnswer.objects.filter(
                    id__in=answers_ids, number_1=MappingAnswer.FIRST_CHAIN_TYPES.zero)
                second_order_list = []
                for key, value in MappingAnswer.SECOND_CHAIN_TYPES:
                    second_order_list.append(key)
                unused_second_key_list = [x for x in second_order_list if x not in key_list]

                for key, zero_answer in enumerate(answers_zero_position_one):
                    QuizMappingAnswer.objects.create(quiz_question=quiz_question, number_2=unused_second_key_list[key],
                                                     number_1=zero_answer.number_1, answer=zero_answer)

            return redirect('quiz:test-detail', self.instance.id)
        else:
            context['formset'] = formset
            context['object'] = self.instance
            context['question'] = self.current_question
            context['quiz'] = self.current_quiz
            context['current_question_number'] = self.current_quiz.quiz_questions.filter(
                status=QuizQuestion.QUIZ_QUESTION_STATUS_TYPES.done).count() + 1
            context['max_question_number'] = self.current_quiz.quiz_questions.count()
            if timezone.now() < self.current_quiz.created + \
                    timedelta(minutes=self.current_quiz.test.test_parameter.test_time):
                context['time_left'] = int((self.current_quiz.created +
                                        timedelta(minutes=self.current_quiz.test.test_parameter.test_time) -
                                        timezone.now()).total_seconds())
            else:
                context['time_left'] = 0
            return render(request, self.template_name, context)


class CancelTestView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        self.instance = Quiz.objects.filter(pk=pk, student=self.request.user.profile).first()
        if not self.instance:
            raise Http404(_("Not found"))
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return redirect('quiz:quiz-finish', self.instance.id)


class FinishQuizView(LoginRequiredMixin, View):
    template_name = 'quiz/test_ending.html'

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        self.instance = Quiz.objects.filter(pk=pk, student=self.request.user.profile).first()
        if not self.instance:
            raise Http404(_("Not found"))

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.instance.status = Quiz.QUIZ_STATUS_TYPES.done
        self.instance.save()
        self.instance.quiz_questions.filter(status=QuizQuestion.QUIZ_QUESTION_STATUS_TYPES.active).update(
            status=QuizQuestion.QUIZ_QUESTION_STATUS_TYPES.suspend)
        context = dict()
        context['instance'] = self.instance
        return render(request, self.template_name, context)
