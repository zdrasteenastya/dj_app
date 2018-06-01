import random

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render, render_to_response

from .utils import handle_uploaded_file, get_results
from .models import Question, Test


def index(request):
    """ Render main page """
    return render(request, 'polls/index.html')


@login_required
def detail(request):
    """ Returns the required number of randomly selected questions  """
    list_ids_questions = [question.pk for question in Question.objects.all()]
    random.shuffle(list_ids_questions)
    number_questions = list_ids_questions[:settings.NUMBER_OF_QUESTION_PER_TEST]
    questions = [get_object_or_404(Question, pk=question_id) for question_id in number_questions]
    return render(request, 'polls/detail.html', {'questions': questions})


def results(request):
    """ Render page with current test result """
    return render(request, 'polls/results.html')


def vote(request):
    """ Handle current test """
    current_user = get_object_or_404(User, pk=request.user.pk)
    form_data = {
        int(question.split('_')[1]): [answer for answer in request.POST.getlist(question)]
        for question in request.POST.keys() if 'question_' in question
    }
    test_id = get_results(form_data, current_user)
    return render(
        request, 'polls/results.html',
        {'test': get_object_or_404(Test, pk=test_id)}
    )


def auth_view(request):
    """ Login user """
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        page = 'admin_view' if user.groups.filter(name='admin').exists() else 'loggedin'
        return HttpResponseRedirect(page)
    else:
        return HttpResponseRedirect('invalid_login')


def logout(request):
    """ Logout user ans redirect to the main page """
    auth.logout(request)
    return redirect('/polls')


@login_required
def loggedin(request):
    """ Render page with tests selection"""
    return render_to_response(
        'polls/loggedin.html',
        {
            'user': request.user,
            'is_admin': request.user.groups.filter(name='admin').exists()
        }
    )


@user_passes_test(lambda u: u.groups.filter(name='admin').exists())
def admin_view(request):
    """ Render page with results for all users """
    return render_to_response(
        'polls/admin_view.html',
        {
            'user': request.user,
            'is_admin': True,
            'tests': Test.objects.all()
        }
    )


def invalid_login(request):
    """ In case wrong auth data """
    return render(request, 'polls/invalid_login.html')


def register(request):
    """ Register a new user and redirect to page with tests selection """
    username = request.POST.get('id_username', '')
    email = request.POST.get('email', '')
    password = request.POST.get('id_password1', '')
    user = User.objects.create_user(username, email, password)
    user.save()
    auth.login(request, auth.authenticate(username=username, password=password))
    return HttpResponseRedirect('loggedin')


@login_required
def history(request):
    """ Render page with all tests for current user"""
    current_user = get_object_or_404(User, pk=request.user.pk)
    return render(request, 'polls/history.html', {'h': current_user})


# TODO
def forgot(request):
    """ Define user, using email address, and send email with password """
    # email = request.POST.get('email', '')
    # User.objects.filter(email=email)
    return render(request, 'polls/forgot.html')


@user_passes_test(lambda u: u.groups.filter(name='admin').exists())
def upload_file(request):
    """ Handle xml file for adding new questions """
    result = handle_uploaded_file(request.FILES['file'])
    return HttpResponseBadRequest(content='Please attach ONLY XML file') if result else render(
        request, 'polls/upload_file.html'
    )


@user_passes_test(lambda u: u.groups.filter(name='admin').exists())
def add_question(request):
    """ Render page for downloading file """
    return render(request, 'polls/add_question.html', {'is_admin': True})
