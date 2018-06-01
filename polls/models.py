from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    multi_answer = models.BooleanField(default=False)
    question_type = models.CharField(max_length=200, default='python')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_right = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Test(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_of_correct_answer = models.IntegerField(default=0)
    number_of_incorrect_answer = models.IntegerField(default=0)
    data_passing = models.DateTimeField('date published')


class TestInfo(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    user_answer = models.CharField(max_length=200)
    right_answer = models.CharField(max_length=200)
    is_user_answered_right = models.BooleanField(default=False)
