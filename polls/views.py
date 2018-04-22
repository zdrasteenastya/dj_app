import random
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic
from django.shortcuts import render, redirect, render_to_response
from django.contrib import auth
from django.template.context_processors import csrf
from django import forms

from polls.templates.utils.files import handle_uploaded_file
from .models import Question, Choice, Test, TestInfo
from django.contrib.auth.models import User

NUMBER_OF_QUESTION_PER_TEST = 5


def index(request):
    return render(request, 'polls/index.html')


def detail(request):
    all_questions = range(1, len(Question.objects.all()) + 1)
    random.shuffle(all_questions)
    number_questions = all_questions[:NUMBER_OF_QUESTION_PER_TEST]
    questions = []
    for question_id in number_questions:
        questions.append(get_object_or_404(Question, pk=question_id))
    return render(request, 'polls/detail.html', {'questions': questions})


def results(request, ids):
    return render(request, 'polls/results.html')


def vote(request):
    # Define user
    current_user = get_object_or_404(User, pk=request.user.pk)

    # Create a new quiz and quiz info
    quiz = Test(user=current_user, data_passing=timezone.now())
    quiz.save()
    results = {}
    for question, answer in request.POST.items():
        if question == 'csrfmiddlewaretoken':
            continue
        results[int(question.split('_')[1])] = int(answer)

    for question_id, answer_id in results.items():
        quiz_info = TestInfo(test_id=quiz)
        quiz_info.save()
        question = get_object_or_404(Question, pk=question_id)
        quiz_info.question_text = question.question_text
        selected_choice = question.choice_set.get(pk=answer_id)

        quiz_info.user_answer = selected_choice.choice_text
        right_choice = ''
        if selected_choice.is_right:
            quiz.number_of_correct_answer += 1
            quiz_info.is_user_answered_right = True
        else:
            quiz.number_of_incorrect_answer += 1
            right_choice = question.choice_set.filter(is_right=True)[0].choice_text
            quiz_info.is_user_answered_right = False
        quiz_info.right_answer = right_choice if right_choice else selected_choice.choice_text
        quiz_info.save()
    quiz.save()

    q = get_object_or_404(Test, pk=quiz.pk)

    return render(request, 'polls/results.html', {'quiz': q})


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        if user.groups.filter(name='admin').exists():
            return HttpResponseRedirect('admin_view')
        else:
            return HttpResponseRedirect('loggedin')
    else:
        return HttpResponseRedirect('invalid_login')


def logout(request):
    auth.logout(request)
    return render_to_response('polls/logout.html')


def loggedin(request):
    return render_to_response('polls/loggedin.html',
                              {'user': request.user, 'is_admin': request.user.groups.filter(name='admin').exists()})


def admin_view(request):
    return render_to_response('polls/admin_view.html',
                              {'full_name': request.user.username, 'tests': Test.objects.all()})


def invalid_login(request):
    return render(request, 'polls/invalid_login.html')


def register(request):
    username = request.GET.get('id_username', '')
    email = request.GET.get('email', '')
    password = request.GET.get('id_password1', '')
    user = User.objects.create_user(username, email, password)
    user.save()
    auth.login(request, auth.authenticate(username=username, password=password))
    return HttpResponseRedirect('loggedin')


def history(request):
    # Define user
    h = get_object_or_404(User, pk=request.user.pk)
    return render(request, 'polls/history.html', {'h': h})


def forgot(request):
    # email = request.POST.get('email', '')
    # User.objects.filter(email=email)
    return render(request, 'polls/forgot.html')


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


def upload_file(request):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        handle_uploaded_file(request.FILES['file'])
    return render(request, 'polls/upload_file.html')


def add_question(request):
    return render(request, 'polls/add_question.html')