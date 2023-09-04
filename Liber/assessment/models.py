from django.db import models
import spacy
from module.models import Module
from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer
from django.contrib.auth import get_user_model
User = get_user_model()


class Assessment(models.Model):
    user = models.ForeignKey(
        User, blank=False, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    unique_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    user = models.ForeignKey(
        User, blank=False, null=True, on_delete=models.CASCADE)
    module_code = models.CharField(max_length=10, default=1, blank=False)
    assessment = models.ForeignKey(Assessment,
                                   on_delete=models.CASCADE,
                                   default=1,
                                   blank=False)
    header = models.CharField(max_length=200)

    def __str__(self):
        return self.header


class Section(models.Model):
    user = models.ForeignKey(
        User, blank=False, null=True, on_delete=models.CASCADE)
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 default=1,
                                 blank=False)
    sub_q = models.CharField(max_length=300)
    # Make sure 'blank' is set to True
    reference = models.TextField(blank=True)

    def __str__(self):
        # return self.sub_q
        return f"{self.question.header}: {self.sub_q}"

    def get_answer_from_reference(self):
        # Step 1: Use sub_q as the question
        question_text = self.sub_q

        # Step 2: Get related Question
        related_question = self.question

        # Step 3: Get related Module's code as context
        related_module_code = related_question.module_code

        # Step 4: Get related Module's pages' content as context
        related_module = Module.objects.get(code=related_module_code)
        context = ""
        # Assuming you have related_name='pages' in the Module-Page relationship
        for page in related_module.pages.all():
            context += page.content + " "

        # Load model & tokenizer
        model_name = "deepset/roberta-base-squad2"
        model = AutoModelForQuestionAnswering.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Get predictions
        nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)
        qa_input = {
            'question': question_text,
            'context': context
        }
        res = nlp(qa_input)

        return res

    def save(self, *args, **kwargs):
        if not self.reference:  # Check if reference is empty
            answer_result = self.get_answer_from_reference()
            # Set reference to the answer
            self.reference = answer_result['answer']
        super().save(*args, **kwargs)  # Call the original save method
