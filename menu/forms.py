from django import forms


class CreateMenu(forms.Form):
    date = forms.DateTimeField()
    option1 = forms.CharField(widget=forms.Textarea)
    option2 = forms.CharField(widget=forms.Textarea)
    option3 = forms.CharField(widget=forms.Textarea)


class MenuOption(forms.Form):
    def __init__(self, options, *args, **kwargs):
        super(MenuOption, self).__init__(*args, **kwargs)
        self.fields["option"] = forms.CharField(
            widget=forms.RadioSelect(choices=options)
        )


class SelectOption(forms.Form):
    customizations = forms.CharField(widget=forms.Textarea)
    option = forms.CharField()
