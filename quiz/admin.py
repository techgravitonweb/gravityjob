from django.contrib import admin

from jobsapp.models import  QuizAdminn

from .models import Quiz, Question, Choice
# Register your models here.

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(QuizAdminn)