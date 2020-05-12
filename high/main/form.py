from django import forms
from .models import Users,Business
class UsersForm(forms.ModelForm):
    class Meta:
        model=Users
        fields=['account','phone','email','password','name']
        widgets={
            'name':forms.TextInput(attrs={'class': 'form-control', 'placeholder': '姓名'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密碼'}),
            'email':forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '電子信箱'}),
            'phone':forms.TextInput(attrs={'class': 'form-control', 'placeholder':'手機'}),
            'account':forms.TextInput(attrs={'class': 'form-control', 'placeholder': '使用者帳號'})
        }
class BusinessForm(forms.ModelForm):
    class Meta:
        model=Business
        fields=['buyer','seller','totalprice','amount','product_id','ordernumber']
        widgets={
            'buyer':forms.TextInput(),
            'seller': forms.TextInput(),
            'amount':forms.TextInput(),
            'product_id':forms.TextInput(),
            'totalprice':forms.TextInput(),
            'ordernumber':forms.TextInput()
        }