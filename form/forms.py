from django import forms
ROLE_CHOICES = (
    ('protagonist','protagonist'),
    ('antagonist','antagonist'),
    ('mentor','mentor'),
    ('tempter','tempter'),
    ('skeptic','skeptic'),
    ('emotional','emotional'),
    ('logical','logical'),
)
class InputScenario(forms.Form):
     scenario = forms.CharField(widget=forms.Textarea)
     characterName = forms.CharField()
     characterRole = forms.ChoiceField(choices=ROLE_CHOICES)
