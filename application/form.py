from django import forms



class SettingsForm(forms.ModelForm):
    onff = forms.BooleanField()
