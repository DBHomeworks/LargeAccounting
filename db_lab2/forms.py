from django import forms

class IdForm(forms.Form):
    id = forms.CharField(label='Employee id', max_length=10)