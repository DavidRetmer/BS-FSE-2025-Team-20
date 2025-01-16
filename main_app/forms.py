from django import forms 

class SendMailForm(forms.Form):
    title = forms.CharField(label="put our mail here",max_length=200)
    

class TaskForm(forms.Form):
    title = forms.CharField(label="put our mail here",max_length=200)
    description = forms.CharField(label="descrive ur problem here :" ,widget=forms.Textarea)  