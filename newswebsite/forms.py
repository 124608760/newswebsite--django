from django import forms
from django.core.exceptions import ValidationError



def words_validator(comment):
    if len(comment)<5:
        raise ValidationError("您输入的评论字数太短，请重新输入至少5个字符")

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(),validators=[words_validator])
