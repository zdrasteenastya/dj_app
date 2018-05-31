""" This module contains auxiliary functions """

from lxml.etree import fromstring

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Question, Test, TestInfo


def handle_uploaded_file(user_data):
    """ Parse xml file and add new questions to DB """
    root = fromstring(user_data.read())
    for question in root.getchildren():
        question_text = question.attrib['question_text']
        question_object = Question(question_text=question_text)
        question_object.save()
        if len(question.findall('choice[@is_right="true"]')) > 1:
            question_object.multi_answer = True

        str2bool = lambda x: x == 'true'
        for choice in question.getchildren():
            question_object.choice_set.create(
                choice_text=choice.text,
                is_right=str2bool(choice.attrib['is_right'])
            )
        question_object.save()


def admin_required(func):
    """" Check admin access rights """
    def check_perms(request):
        user = get_object_or_404(User, pk=request.user.pk)
        is_member = user.groups.filter(name='admin').exists()
        if is_member:
            return func(request)
        else:
            raise PermissionDenied
    return check_perms


def login_required(func):
    """" Check login access rights """
    def check_perms(request):
        return func(request) if request.user.id else render(request, 'polls/invalid_login.html')
    return check_perms


def get_results(results, current_user):
    """" Handle form data """
    quiz = Test(user=current_user, data_passing=timezone.now())
    quiz.save()
    for question_id, answer_ids in results.items():

        question = get_object_or_404(Question, pk=question_id)

        quiz_info = TestInfo(test_id=quiz)
        quiz_info.save()
        quiz_info.question_text = question.question_text

        user_choices = [question.choice_set.get(pk=answer_id) for answer_id in answer_ids]
        right_answers = question.choice_set.filter(is_right=True)

        quiz_info.user_answer = ','.join(choice.choice_text for choice in user_choices)
        quiz_info.right_answer = ','.join(answer.choice_text for answer in right_answers)

        if all([c.is_right for c in user_choices]) and len(user_choices) == len(right_answers):
            quiz.number_of_correct_answer += 1
            quiz_info.is_user_answered_right = True
        else:
            quiz.number_of_incorrect_answer += 1
            quiz_info.is_user_answered_right = False
        quiz_info.save()
    quiz.save()
    return quiz.pk
