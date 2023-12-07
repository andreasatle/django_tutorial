from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    readonly_fields = ['created_at', 'updated_at']

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'created_at', 'updated_at')
    fieldsets = [
        (None, {'fields': ['question_text']}),
    ]
    inlines = [ChoiceInline]
    readonly_fields = ['created_at', 'updated_at']

admin.site.register(Question, QuestionAdmin)
