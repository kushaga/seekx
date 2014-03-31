from django.db import models
from django.forms import ModelForm

Event_Choices=(
('misc','misc'),
('sports','sports'),
('hangout','hangout'),
('food','food'),
('project','project'),
('movies','movies'),
('competitions','competitions'),
('carpool','carpool'),
)

batch_choice =(
('BTECH2011','BTECH2011'),
('BTECH2010','BTECH2010'),
('BTECH2012','BTECH2012'),
('BTECH2013','BTECH2013'),
('MTECH2011','MTECH2011'),
('MTECH2012','MTECH2012'),
('PHD','PHD')
)

courses_choice =(
('Mobile Computing','Mobile Computing'),
('Software Engineering','Software Engineering'),

)

class Seek_User(models.Model):
	username= models.CharField(max_length=100) # //
	firstname= models.CharField(max_length=100) #//
	lastname=models.CharField(max_length=100) #//
	email = models.EmailField(max_length=75) #//
	hobbies = models.CharField(max_length=1000) #//
	courses = models.CharField(max_length=100, choices=courses_choice)	#//
	batch = models.CharField(max_length=100 , choices= batch_choice)	 #//
	#points = models.IntegerField(max_length=4,null= True) # //
	points = models.IntegerField(max_length=4, default=0, null= True)
	#quote =models.CharField(max_length=100)
	profilePhoto = models.ImageField(blank = True, null = True,upload_to = 'profile_pic/', max_length = 255)#//
	#have to also add photo

class Event(models.Model):
	eventname = models.CharField(max_length=120)#event name eg - volley ball team // //
	eventtype = models.CharField(max_length=30,  choices=Event_Choices) #category - eg - sports // //
	username = models.CharField(max_length=100) #								// //
	description = models.CharField(max_length=1000) # 							//
	numpeople = models.IntegerField() #											//
	pubdate = models.DateTimeField('date published') # current time recordder as pub date , start date // //
	deadline = models.DateTimeField(null=True) #user selects deadline of the event , end date		//
	email = models.EmailField(max_length=75) #email of the requester			// //
	status=models.CharField(max_length=100)
	profilePhoto = models.ImageField(blank = True, null = True,upload_to = 'profile_pic/', max_length = 255)
	userid = models.IntegerField(max_length=4, default=1, null= True) # who puts the request
	