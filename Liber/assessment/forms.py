from django import forms
from .models import Assessment, Question, Section


class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['name', 'unique_code']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['module_code', 'assessment', 'header']


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['question', 'sub_q']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
