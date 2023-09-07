from django import forms

class SearchForm(forms.Form):
    person_number = forms.CharField(label='Person Number', required=False)
    national_id = forms.CharField(label='National ID', required=False)
    first_name = forms.CharField(label='First Name', required=False)
    last_name = forms.CharField(label='Last Name', required=False)
    person_id_hcm = forms.CharField(label='Person Id HCM', required=False)
