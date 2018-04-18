import datetime
from django.utils.translation import ugettext as _
import random
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'



class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    # votes = models.IntegerField(default=0)
    is_right = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Test(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_of_correct_answer = models.IntegerField(default=0)
    number_of_incorrect_answer = models.IntegerField(default=0)
    data_passing = models.DateTimeField('date published')


class TestInfo(models.Model):
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    user_answer = models.CharField(max_length=200)
    right_answer = models.CharField(max_length=200)
    is_user_answered_right = models.BooleanField(default=False)
