from django import forms  
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from article_dashboard.models import Summaries, Articles 


class SummariesForm(forms.ModelForm):  
    ''' Form for Summaries model'''
    class Meta:  
        model = Summaries  
        fields = '__all__'


class ArticlesList(forms.Form):
    ''' Form for main view - "articles_list" '''
    date_from = forms.DateField()
    date_to = forms.DateField()
    articles = forms.ModelMultipleChoiceField(Articles.objects.all())
    
    def clean(self):
        ''' Clean and validate valies of date period'''
        cleaned_data = super().clean()
        date_from = cleaned_data.get("date_from")
        date_to = cleaned_data.get("date_to")

        if date_from > date_to:
            raise forms.ValidationError("Start date must be less then end date.")
