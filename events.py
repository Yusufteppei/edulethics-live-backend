import json
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "edulethics.settings")
django.setup()

import random

from exam.models import Question, ExamQuestion, ChoiceSet, Exam, Subject, Event, Level


class Event:
    
    name = ''

    def __init__(self, name):
        name = self.name


    def create_all_exams(self):
        for level in Level.objects.all():
            for subject in level.subjects.all():
                Exam.objects.create(event=self, level=level, subject=subject)


    def assign_questions_to_exam(self, exam, count):
        subject = exam.subject
        questions = random.sample(Questions.objects.filter(subject=subject), 100)
        ##  CREATE EXAM QUESTIONS
        i = 1
        for q in questions:
            ExamQuestion.objects.create(question=q, exam=exam, order=i) 
            print(f" Question {i} - {exam}")

            i += 1


    def assign_questions_to_all_exams(self, event, question_count):

        for exam in exams:
            assign_questions_to_exam(exam, question_count)
