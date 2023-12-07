from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    readonly_fields = ['created_at', 'updated_at']

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'created_at', 'updated_at', 'was_published_recently')
    fieldsets = [
        (None, {'fields': ['question_text']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
