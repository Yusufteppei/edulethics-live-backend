import json
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "edulethics.settings")
django.setup()


from exam.models import Question, ExamQuestion, ChoiceSet, Exam, Subject, Event, Level



##			'englishlit', 'crk', 'irk', 'civiledu', 'government']

SUBJECTS = {
    'Physics': 'physics',
    'Chemistry': 'chemistry',
    'Biology': 'biology',
    'Commerce': 'commerce',
    'Accounting': 'accounting',
    'Mathematics': 'mathematics',
    'History': 'history',
    'Economics': 'economics',
    'Literature in English': 'englishlit',
    'Christian Religious Studies': 'crk',
    'Islamic Religious Studies': 'irk',
    'Civic Education': 'civiledu',
    'Government': 'government'
}

#with open('Questions2/physics questions', 'rb') as f:
#    l = json.load(f)

#print(l['data'][0])


def create_choice_set_from_file(od):
   
    choice_set = ChoiceSet.objects.create(a=od['a'], b=od['b'], c=od['c'], d=od['d'])
    return choice_set


def create_question(qd, subject):
    choice_set = create_choice_set_from_file(qd['option'])
    if len(qd['answer']) > 1:
        return
    q = Question.objects.get_or_create(subject=subject, question_text=qd['question'], choice_set=choice_set, correct_answer=qd['answer'].upper())
    return q

def create_questions_from_file(subject, level):
    questions = []
    with open(f'Questions{level}/{SUBJECTS[subject.name]} questions', 'rb') as f:
        l = json.load(f)
    
    for qd in l['data']:
        questions.append(create_question(qd, subject))
    return questions


def create_exam(event, level, subject):
    print(f"Creating Exam {subject} {level}")
    exam = Exam.objects.get_or_create(event=event, level=level, subject=subject)
    return exam

def get_exam(event, level, subject):
    exam = Exam.objects.get(event=event, level=level, subject=subject)
    return exam

def get_level_exams(event, level):
    level = Level.objects.get(name=level)
    subjects = level.subjects.all()
    return Exam.objects.filter(event=event, level=level)


def create_exam_question(exam, order, question):
    eq = ExamQuestion.objects.create(exam=exam, order=order, question=question)
    return eq

def create_exam_questions(questions, exam):
    count = 0
    for i in questions:
        count += 1
        print(create_exam_question(exam, count, i))

subjects = []
def create_subjects(subject_dict):
    
    for i in subject_dict.keys():
        subjects.append(Subject.objects.create(name=i))


def create_exams(event, level):
    exams = []
    level = Level.objects.get(name=level)
    subjects = Subject.objects.all()
    for subject in subjects:
        exams.append(create_exam(event, level, subject))
    return exams


#   CREATE SUBJECTS
#create_subjects(SUBJECTS)

#   CREATE EXAMS
event = Event.objects.get(title='2023 Harmattan')
exams1 = get_level_exams(event, 'SS1')
exams2 = get_level_exams(event, 'SS2')
exams3 = get_level_exams(event, 'SS3')

#   CREATE QUESTIONS
#subjects = Subject.objects.all()
#for subject in subjects:
#    q1 = create_questions_from_file(subject, 1)
#    q2 = create_questions_from_file(subject, 2)
#
#    q3 = create_questions_from_file(subject, 3)


    #   CREATE EXAM QUESTIONS
S = ['SS1', 'SS2', 'SS3']

def get_level_subjects(lvl):
    level = Level.objects.get(name=lvl)
    return level.subjects.all()

def get_level_questions(lvl):
    QUESTIONS = {}
    level = Level.objects.get(name=lvl)
    subjects = get_level_subjects(lvl)
    for subject in subjects:
        questions =  Question.objects.filter(subject=subject).order_by('?')[:100]
        QUESTIONS[subject] = questions
    return QUESTIONS

 
#for level in S:
#    #level = Level.objects.get(level)
#    subjects = get_level_subjects(level)
#    exams = get_level_exams(level)

def upload_level_exam_questions(level):
    exams = get_level_exams(event, level)
    for exam in exams:
        subject = exam.subject
        questions = get_level_questions(level)
        create_exam_questions(questions[subject], exam)
        #print(ExamQuestion)

#upload_level_exam_questions('SS3')
upload_level_exam_questions('SS2')
upload_level_exam_questions('SS1')
