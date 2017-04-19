from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email



def words_validator(comment):
    if len(comment)<5:
        raise ValidationError("您输入的评论字数太短，请重新输入至少5个字符")

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(),validators=[words_validator])

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'用户名'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'密码'}))

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'用户名'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'邮箱'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'密码'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'确认密码'}))

    def clean(self):
        cleaned_data = super(RegisterForm,self).clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if User.objects.filter(username=username):
           raise forms.ValidationError("用户已存在")
        if User.objects.filter(email=email):
           raise forms.ValidationError("该邮箱已被注册")

        try:
           validate_email(email)
        except ValidationError:
           raise forms.ValidationError("不正确的邮箱格式")

        if len(password) < 6:
           raise forms.ValidationError("密码长度至少6位")

        if password_confirm != password:
           raise forms.ValidationError("两次输入的密码不一致")

class EditForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'邮箱'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'密码'}),required=False)
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'确认密码'}),required=False)
    avatar = forms.FileField(label="上传头像")

    def clean(self):
        cleaned_data = super(EditForm,self).clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")


        try:
           validate_email(email)
        except ValidationError:
           raise forms.ValidationError("不正确的邮箱格式")

        if len(password) < 6:
           raise forms.ValidationError("密码长度至少6位")

        if password_confirm != password:
           raise forms.ValidationError("两次输入的密码不一致")
