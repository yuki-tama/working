from django import forms

class InputScenario(forms.Form):
     name = forms.CharField()
     email = forms.EmailField()
     body = forms.CharField()
