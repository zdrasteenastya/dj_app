from django.contrib import admin

from .models import Question, Choice, Test


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text', 'multi_answer']}),

    ]
    inlines = [ChoiceInline]
    list_display = ('question_text',)
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Test)
