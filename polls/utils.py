""" This module contains auxiliary functions """
from json import dumps
from lxml.etree import fromstring, XMLSyntaxError

from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Question, Test, TestInfo


def handle_uploaded_file(user_data):
    """ Parse xml file and add new questions to DB """
    try:
        root = fromstring(user_data.read())
    except XMLSyntaxError:
        return 'error'
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


def get_results(results, current_user):
    """" Handle form data """
    test = Test(user=current_user, data_passing=timezone.now())
    test.save()
    for question_id, answers in results.items():

        question = get_object_or_404(Question, pk=question_id)
        is_text_field = question.choice_set.count() == 1

        test_info = TestInfo(test=test)
        test_info.save()
        test_info.question_text = question.question_text

        user_choices = answers[0].encode('utf-8') if is_text_field else [
            question.choice_set.get(pk=int(answer_id)) for answer_id in answers
        ]
        right_answers = question.choice_set.filter(is_right=True)

        test_info.user_answer = dumps(user_choices) if is_text_field else dumps(
            [choice.choice_text for choice in user_choices]
        )
        test_info.right_answer = dumps([answer.choice_text for answer in right_answers])

        is_answers_correct = user_choices.lower() == right_answers[0].choice_text.lower() if is_text_field \
            else all([c.is_right for c in user_choices]) and len(user_choices) == len(right_answers)

        if is_answers_correct:
            test.number_of_correct_answer += 1
            test_info.is_user_answered_right = True
        else:
            test.number_of_incorrect_answer += 1
            test_info.is_user_answered_right = False
        test_info.save()
    test.save()
    return test.pk
