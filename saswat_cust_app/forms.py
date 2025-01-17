# forms.py
from django import forms
from django.forms import ModelChoiceField
from .models import QueryModel, ShortenedQueries


class QueryModelForm(forms.ModelForm):
    # description = forms.CharField(max_length=255, required=False, label="AI Description",
    #                               widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # additional_info = forms.CharField(max_length=255, required=False, label="AI Additional Information",
    #                                   widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = QueryModel
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'class': 'auto-expand', 'readonly': 'readonly'}),
            'additional_info': forms.Textarea(attrs={'class': 'auto-expand', 'readonly': 'readonly'}),
        }

    class Media:
        js = ('saswat_cust_app/js/admin_custom.js',)