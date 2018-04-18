from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic
from django.shortcuts import render, redirect, render_to_response
from django.contrib import auth
from django.template.context_processors import csrf

from .models import Question, Test, TestInfo
from django.contrib.auth.models import User


def index(request):
    return render(request, 'polls/index.html')


def detail(request):
    number_questions = [2, 4, 3]
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
        return HttpResponseRedirect('loggedin')
    else:
        return HttpResponseRedirect('invalid_login')


def logout(request):
    auth.logout(request)
    return render_to_response('polls/logout.html')


def loggedin(request):
    return render_to_response('polls/loggedin.html', {'full_name': request.user.username})


def invalid_login():
    return render_to_response('polls/invalid_login.html')


def register(request):
    username = request.POST.get('id_username', '')
    email = request.POST.get('email', '')
    password = request.POST.get('id_password1', '')
    user = User.objects.create_user(username, email, password)
    user.save()
    auth.login(request, auth.authenticate(username=username, password=password))
    return HttpResponseRedirect('loggedin')


def history(request):
    # Define user
    h = get_object_or_404(User, pk=request.user.pk)
    return render(request, 'polls/history.html', {'h': h})
