from django.db import models
from django.urls import reverse

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.question_text

    @property
    def get_correct_answer(self):
        return self.set_choices.get(is_correct_answer=True)

class Choice(models.Model):
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 related_name='set_choices')
    choice_text = models.CharField(max_length=50)
    is_correct_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

# ---------------------------
