from django.forms import ModelForm, Textarea, extras
from django import forms
from models import Event , Seek_User
from django.forms import ModelChoiceField
from django.contrib.admin import widgets
from django.contrib.admin import widgets     

class EventForm(forms.ModelForm):
	class Meta:
		model = Event
	eventname = forms.CharField(widget=forms.TextInput(attrs = {'class':'form-control','placeholder':'Event Name'}))
	description = forms.CharField(widget=forms.TextInput(attrs = {'class':'form-control','placeholder':'Description'}))
	numpeople = forms.IntegerField()
	deadline =forms.DateTimeField(widget=forms.SplitDateTimeWidget())
	#profilePhoto = forms.ImageField()
	
	#user id 
	def __init__(self, *args, **kwargs):
		super(EventForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['readonly'] = True
		self.fields['email'].widget.attrs['readonly'] = True
		self.fields['pubdate'].widget.attrs['readonly'] = True
		self.fields['status'].widget.attrs['readonly'] = True
		self.fields['profilePhoto'].widget.attrs['readonly'] = True
		self.fields['eventtype'].widget.choices =self.fields['eventtype'].choices
		
class SignupForm(forms.ModelForm):
	class Meta:
		model = Seek_User
	profilePhoto = forms.ImageField()
	hobbies = forms.CharField(widget=forms.TextInput(attrs = {'class':'form-control','placeholder':'Hobbies'}))
	
	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['readonly'] = True
		self.fields['firstname'].widget.attrs['readonly'] = True
		self.fields['lastname'].widget.attrs['readonly'] = True
		self.fields['email'].widget.attrs['readonly'] = True
		self.fields['points'].widget.attrs['readonly'] = True
		self.fields['courses'].widget.choices =self.fields['courses'].choices
		self.fields['batch'].widget.choices =self.fields['batch'].choices
		