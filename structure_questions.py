import pandas as pd 

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "edulethics.settings")
django.setup()


from exam.models import Question, ExamQuestion, ChoiceSet, Exam, Subject, Event, Level
subjects = ['Agricultural Science', 'Basic Science', 'Business Studies', 'Christian Religious Studies',
	'Civic Education', 'Commerce',
	'Physical and Health Education', 'Social Studies','English Language']
errors = ['Home Economics', 'English Language','Mathematics', 'I.C.T']

#print(df['options'])


def clean_options(options):
    try:
        VAL = eval(eval(options)[0])
    except NameError:
        pass
    try: 
        choices = {
	    'A': VAL[0],
	    'B': VAL[1],
	    'C': VAL[2],
	    'D': VAL[3],
	    'E': VAL[4]
	}
    except IndexError:
	    choices = {
		'A': VAL[0],
		'B': VAL[1],
		'C': VAL[2],
		'D': VAL[3],
		'E': ''
	    }
    except NameError:
        pass
       
    return choices	


def get_answer_option(options, answer):
    try:
        v = options.index(answer)
    except ValueError:
        v = 99
    if v == 0:
        return 'A'
    elif v == 1:
        return 'B'
    elif v == 2:
        return 'C'
    elif v == 3:
        return 'D'
    elif v == 4:
        return 'E'
    else:
        return 'F'


def clean_options_col(df):
    a = []
    b = []
    c = []
    d = []
    e = []
    answer=[]

    for i in df.index:
        options = df.iloc[i]['options']
    	#print("i['options']", df.iloc[i]['options'])
        clean = clean_options(options)
		#df.iloc[i]['A'] = clean['A']
		#df.iloc[i]['B'] = clean['B']
		#df.iloc[i]['C'] = clean['C']
		#df.iloc[i]['D'] = clean['D']

        a.append(clean['A'])
        b.append(clean['B'])
        c.append(clean['C'])
        d.append(clean['D'])
        e.append(clean['E'])
        answer.append(get_answer_option( [clean['A'], clean['B'], clean['C'], clean['D'], clean['E']], df.iloc[i]['answer'] ))

		#	GET ANSWER OPTION

    return {
	'A': a,
	'B': b,
	'C': c,
	'D': d,
	'E': e,
	'ANS': answer
    }



def clean_table(df):
    df = df.drop('Unnamed: 0', axis=1)
    df.rename({'subject.name': 'subject'})

    opts = clean_options_col(df)
    df['A'] = opts['A']
    df['B'] = opts['B']
    df['C'] = opts['C']
    df['D'] = opts['D']
    df['E'] = opts['E']
    df['ANS'] = opts['ANS']
    df = df[['question', 'A', 'B', 'C', 'D', 'E', 'ANS']]

    return df

def create_question(df):
    question_text = df['question']
    answer =  0






###################################################      DATABASE ACCESS REQUIRED      ##########################################333

def create_choice_set(a,b,c,d,e):
    return ChoiceSet.objects.create(a=a,b=b,c=c,d=d,e=e)

def create_questions(df, subject):
    for i in df.index:
        subject = Subject.objects.get(name=subject, category='J')
        Question.objects.create(question_text=df.iloc[i]['question'], correct_answer=df.iloc[i]['ANS'], subject=subject, choice_set=create_choice_set(df.iloc[i]['A'], df.iloc[i]['B'], df.iloc[i]['C'], df.iloc[i]['D'], df.iloc[i]['E']))


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
    try:
        eq = ExamQuestion.objects.get_or_create(exam=exam, order=order, question=question)
    finally:
        pass
    return eq

def create_exam_questions(questions, exam):
    count = 0
    for i in questions:
        count += 1
        try:
            print(create_exam_question(exam, count, i))
        except:
            pass
        finally:
            pass

#subjects = []
def create_subjects(subjects):
    
    for i in subjects:
        Subject.objects.get_or_create(name=i, category='J')


def create_exams(event, level):
    exams = []
    level = Level.objects.get(name=level)
    subjects = Subject.objects.filter(category='J')
    for subject in subjects:
        exams.append(create_exam(event, level, subject))
    return exams


#   CREATE SUBJECTS
#create_subjects(subjects)

#   CREATE EXAMS


event = Event.objects.get(title='2023 Harmattan')
#create_exams(event, 'JSS1')
#create_exams(event, 'JSS2')
#create_exams(event, 'JSS3')

exams1 = get_level_exams(event, 'JSS1')
exams2 = get_level_exams(event, 'JSS2')
exams3 = get_level_exams(event, 'JSS3')

#   CREATE QUESTIONS
#for i in []:
#    print(f"Creating {i}")
#    df = pd.read_csv(f'Junior Questions/{i}.csv') 
#    DF = clean_table(df)
#    create_questions(DF, i)


    #   CREATE EXAM QUESTIONS
S = ['JSS1', 'JSS2', 'JSS3']

def get_level_subjects(lvl):
    level = Level.objects.get(name=lvl)
    return level.subjects.all()

def get_level_questions(lvl):
    QUESTIONS = {}
    level = Level.objects.get(name=lvl)
    subjects = get_level_subjects(lvl)
    for subject in subjects:
        #   DELETE BAD QUESTIONS
       # choice_sets_ = ChoiceSet.objects.filter(a='').delete()
        questions =  Question.objects.filter(subject=subject).order_by('?')[:100]
        

        QUESTIONS[subject] = questions
    return QUESTIONS

 
for level in S:
    #level = Level.objects.get(level)
    subjects = get_level_subjects(level)
    exams = get_level_exams(event, level)

def upload_level_exam_questions(level):
    exams = get_level_exams(event, level)
    for exam in exams:
        subject = exam.subject
        questions = get_level_questions(level)
        try:
            create_exam_questions(questions[subject], exam)
        except KeyError:
            pass
        finally:
            pass
        #print(ExamQuestion)
choice_sets_ = ChoiceSet.objects.filter(a='').delete()

upload_level_exam_questions('JSS3')
upload_level_exam_questions('JSS2')
upload_level_exam_questions('JSS1')
