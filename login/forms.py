from django import forms
class UserForm(forms.Form):
    email=forms.EmailField(label='邮箱')
    username=forms.CharField(max_length=20,label='用户名')
    password=forms.CharField(max_length=20,label='密码')
    enpassword=forms.CharField(max_length=20,label='确认密码')
    def clean_enpassword(self):
        password=self.cleaned_data['password']
        enpassword=self.cleaned_data['enpassword']
        if password==enpassword:
            return password
        else:
            raise forms.ValidationError('Please re-enter your password.')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label='用户名')
    password = forms.CharField(max_length=20, label='密码')