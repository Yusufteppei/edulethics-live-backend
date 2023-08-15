import pandas as pd

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "edulethics.settings")
django.setup()


from exam.models import Question, ExamQuestion, ChoiceSet, Exam, Subject, Event, Level


unoptioned_questions = Question.objects.filter(correct_answer='F')

optioned_questions = Question.objects.exclude(correct_answer='F')

fixed = 0
for q in unoptioned_questions:

    print(q.question_text)
    try:
        same_questions = Question.objects.filter(question_text=q.question_text)
        print(same_questions.count(), " same questions")
        for i in same_questions:
        
            if i.correct_answer != None and i.correct_answer != 'F':
                print("Answer ", i.correct_answer)
                q.correct_answer = i.correct_answer
                q.save()
                fixed += 1
                print(q.question_text[:5], q.correct_answer)
    except:
        pass
print(len(unoptioned_questions), " unoptioned questions")
print("Fixed ", fixed)
print("New unoptioned", Question.objects.filter(correct_answer='F').count())
