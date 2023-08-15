from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import serializers


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class SubjectSerializer(ModelSerializer):
    count = serializers.SerializerMethodField()
    class Meta:
        model = Subject
        fields = '__all__'

    def count(self):
        return Subject.objects.all().count()

class StudentSerializer(ModelSerializer):
    count = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = '__all__'

    def get_count(self):
        return Student.objects.all().count()


class SchoolSerializer(ModelSerializer):
    count = serializers.SerializerMethodField()
    class Meta:
        model = School
        fields = '__all__'

    def get_count(self):
        return School.objects.all().count()


class LevelSerializer(ModelSerializer):
    name = serializers.StringRelatedField()
    class Meta:
        model = Level
        fields = '__all__'


class ChoiceSetSerializer(ModelSerializer):
    class Meta:
        model = ChoiceSet
        #fields = '__all__'
        exclude = ('f',)


class QuestionSerializer(ModelSerializer):
    question_text = serializers.StringRelatedField()
    choice_set = ChoiceSetSerializer()
    class Meta:
        model = Question
        #fields = '__all__'
        exclude = ('correct_answer',)


class ExamSerializer(ModelSerializer):
    title = serializers.StringRelatedField()
    duration = serializers.SerializerMethodField()
    subject = serializers.StringRelatedField()
    event = serializers.StringRelatedField()
    level = serializers.StringRelatedField()
    class Meta:
        model = Exam
        #fields = '__all__'
        exclude = ('students',)

    def get_duration(self, obj):
        if obj.event.policy:
            exam_duration = obj.event.policy.exam_duration
        else:
            exam_duration = 30
        return exam_duration

class ExamQuestionSerializer(ModelSerializer):
    question = QuestionSerializer()
    
    class Meta:
        model = ExamQuestion
        fields = '__all__'


class StudentExamQuestionSerializer(ModelSerializer):
    subject = serializers.StringRelatedField()
    class Meta:
        model = StudentExamQuestion
        fields = '__all__'


class StudentExamPaperSerializer(ModelSerializer):
    exam = ExamSerializer()
    percentage = serializers.SerializerMethodField()
    class Meta:
        model = StudentExamPaper
        fields = '__all__'

    def get_percentage(self, obj):
        sc = obj.final_score
        return sc * 100/40

class RegistrationSerializer(ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'
        read_only_fields = ('paid',)

class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
