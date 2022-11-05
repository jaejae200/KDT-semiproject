from django import forms
from .models import Article, Comment

GRADE_POINT_CHOICES = (
    ('1', 1),
    ('2', 2),
    ('3', 3),
    ('4', 4),
    ('5', 5),
)

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'grade', ]
        widgets = {
            'grade': forms.Select(choices=GRADE_POINT_CHOICES)
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment 
        fields = ['content', ]