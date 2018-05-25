from lxml import etree

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

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


def admin_required(func):
    def check_perms(request):
        user = get_object_or_404(User, pk=request.user.pk)
        is_member = user.groups.filter(name='admin').exists()
        if is_member:
            return func(request)
        else:
            raise PermissionDenied

    return check_perms


def login_required(func):
    def check_perms(request):
        if request.user.id:
            return func(request)
        else:
            return render(request, 'polls/invalid_login.html')

    return check_perms
