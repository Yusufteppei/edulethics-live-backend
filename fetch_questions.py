import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "edulethics.settings")
django.setup()

from exam.models import Student, ExamQuestion, StudentExamQuestion, Exam

def exam_question_data(exam_question):
    try:
        question = exam_question.question.question_text
        option_A = exam_question.question.choice_set.a
        option_B = exam_question.question.choice_set.b
        option_C = exam_question.question.choice_set.c
        option_D = exam_question.question.choice_set.d
        answer = exam_question.question.correct_answer
        order = exam_question.order

        clean_question = question.replace(',',' ').replace(',', '').replace('\n', '   ')
    except NoneType:
        pass
    
    return f"{order},{clean_question},{option_A.replace(',',' ').replace(',', '')},{option_B.replace(',', ' ').replace(',', '')},{option_C.replace(',', ' ').replace(',', '')},{option_D.replace(',', ' ').replace(',', '')},{answer}\n"


def create_csv(exam):
    exam_questions = ExamQuestion.objects.filter(exam=exam)
   
    try:
        print(f'datasets/exam_questions/{exam.subject}/{exam.level} to make')
        os.mkdir(f"datasets/exam_questions/{exam.subject}")

        os.mkdir(f'datasets/exam_questions/{exam.subject}/{exam.level}')
        print(f'datasets/exam_questions/{exam.subject}/{exam.level}')

    except FileExistsError:
        pass
        

    with open(f'datasets/exam_questions/{exam.subject}/{exam.level}/{exam.subject}-{exam.level}.csv', 'w') as f:
        
        f.write("Order,Question,A,B,C,D,answer\n")

        for exam_question in exam_questions:
            print(f'{exam_question.exam}')
            f.write(exam_question_data(exam_question))
   

for exam in Exam.objects.filter(subject__name='English Language'):
    create_csv(exam)
