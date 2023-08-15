from django.contrib import admin
from .models import Level, Event, Exam, School, Student, Subject, Question, ChoiceSet, ExamQuestion, StudentExamQuestion, StudentExamPaper

from .modeladmins import *

m = ( Level, Event, School, Student, Subject, ChoiceSet, ExamQuestion, StudentExamQuestion, StudentExamPaper )

#admin.site.register(m)

admin.site.site_header = "Edulethics Admin"
admin.site.site_title = "Edulethics"
admin.site.index_title = "Exam Portal"

