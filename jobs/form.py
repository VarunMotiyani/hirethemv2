from django.forms import ModelForm
from django import forms
from .models import Job,Company
from .models import Application
from hirethemv2.users.models import User

JOB_TYPE = (("1", "Full time"), ("2", "Part time"), ("3", "Internship"))

class DateInput(forms.DateInput):
    input_type = "date"


class JobCreateForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Job title'}))
    location = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Delhi, India'}))
    type = forms.ChoiceField(choices=JOB_TYPE,initial='1')
    link = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'www.microsoft.com/career/ka?=22 '}))
    salary = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '12.5 lacs'}))
    # tags
    class Meta:
        model = Job
        exclude = ["created","host", "applicants"]
        widgets = {"last_date": DateInput()}

class CompanyCreateForm(ModelForm):
    class Meta:
        model = Company
        exclude = ["created"]

class ApplicationForm(forms.ModelForm):

    name = forms.CharField(required=False)
    urn_number = forms.CharField(required=False)
    department = forms.CharField(required=False)
    address = forms.CharField(required=False)
    github = forms.CharField(required=False)
    tenth_percentage = forms.DecimalField(required=False)
    tenth_school_name = forms.CharField(required=False)
    twelth_percentage = forms.DecimalField(required=False)
    twelth_school_name = forms.CharField(required=False)
    current_cgpa = forms.DecimalField(required=False)
    active_backlogs = forms.IntegerField(required=False)
    resume = forms.FileField(label='Resume', required=True)

    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(), initial=User)

    class Meta:
        model = Application
        fields = ['user', 'job', 'name', 'urn_number', 'department',
                  'address', 'github', 'tenth_percentage', 'tenth_school_name',
                  'twelth_percentage', 'twelth_school_name', 'current_cgpa', 'active_backlogs', 'resume']