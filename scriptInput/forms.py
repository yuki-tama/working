from django import forms

class ScriptForm(forms.Form):
     name = forms.CharField()
     email = forms.EmailField()
     body = forms.CharField()
