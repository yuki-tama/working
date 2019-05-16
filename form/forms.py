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
     scenario = forms.CharField(widget=forms.Textarea(attrs={'class':'scenario_area'}))
     characterName = forms.CharField(widget=forms.TextInput(attrs={'size':'30', 'class' : 'name', 'id':'name1'}))
     characterRole = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class':'role', 'id':'role1'}))
