from django.utils import timezone
from lxml import etree

from models import Question


def handle_uploaded_file(file):
    root = etree.fromstring(file.read())
    for question in root.getchildren():
        question_text = question.attrib['question_text']
        q = Question(question_text=question_text, pub_date=timezone.now())
        q.save()
        for choice in question.getchildren():
            q.choice_set.create(choice_text=choice.text, is_right=choice.attrib['is_right'])
        q.save()
