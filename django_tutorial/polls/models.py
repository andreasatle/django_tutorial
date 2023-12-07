import datetime
from django.utils import timezone
from django.db import models
from django.contrib import admin
# Create your models here.

class WithTimestamp(models.Model):
    created_at = models.DateTimeField("date published", auto_now_add=True)
    updated_at = models.DateTimeField("date of last change", auto_now=True)

    class Meta:
        abstract = True

class Question(WithTimestamp):
    question_text = models.CharField(max_length=200)

    @admin.display(
        boolean=True,
        ordering="created_at",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created_at <= now

class Choice(WithTimestamp):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
