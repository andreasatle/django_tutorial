import datetime
from django.utils import timezone
from django.db import models

# Create your models here.

class WithTimestamp(models.Model):
    created_at = models.DateTimeField("date published", auto_now_add=True)
    updated_at = models.DateTimeField("date of last change", auto_now=True)

    class Meta:
        abstract = True

class Question(WithTimestamp):
    question_text = models.CharField(max_length=200)

    def was_published_recently(self):
        return self.created_at >= timezone.now() - datetime.timedelta(days=1)

class Choice(WithTimestamp):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
