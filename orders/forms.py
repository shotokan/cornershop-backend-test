from django import forms


class SelectOption(forms.Form):
    customizations = forms.CharField(widget=forms.Textarea)
    option = forms.CharField()
