from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from models import Seek_User , Event
from django.utils import timezone
from datetime import datetime
from django.core.mail import send_mail
from forms import EventForm , SignupForm
from django.core.mail import send_mail

def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return redirect('done')

    return render_to_response('home.html', {}, RequestContext(request))

def done(request):
    #print request
    s=User.objects.get(username=request.user).email
    flag=0
    s1=""
    for i in s:
        if(flag==1):
            s1=s1+i
        if(i=='@'):
         flag=1
            
    if(s1!="iiitd.ac.in"):
        User.objects.get(username=request.user).delete()
        return render_to_response('wronglogin.html', {}, RequestContext(request))
    """Login complete view, displays user data"""
    #check on the data base created automatically by the user
    sk = User.objects.get(username=request.user).first_name
    print sk
    sk1 = User.objects.get(username=request.user).email
    print sk1
    username = request.user
    request.session['username']=username
    #request.session['email']=sk1

    if Seek_User.objects.filter(email=sk1).count() ==0:
    	return redirect('signup')
    else:
    	return redirect('dashboard')	
    #return HttpResponse('hello')

def signup(request):
	try:
		if request.method== 'POST' :
			if Seek_User.objects.filter(username=request.user).count()==0: #doubt use email instead of user name
				signup_form=SignupForm(request.POST,request.FILES)
				print signup_form
				if signup_form.is_valid():
					signup_form.save()
					return redirect('done')
				return render_to_response('wrongpage.html', {},{})
			else:
				return render_to_response('wrongpage.html', {},{})
			
		else :
			if Seek_User.objects.filter(username=request.user).count()==0:
			
				s=User.objects.get(username=request.user)
				signup_form={'signup_form':SignupForm({'username':request.user,'points':0,'email':s.email,'firstname':s.first_name,'lastname':s.last_name})}
				return render_to_response('Signup.html',signup_form,context_instance=RequestContext(request))
			else:
				return render_to_response('wrongpage.html', {},{})
	except KeyError:
		pass
		return render_to_response('wrongpage.html', {},{})

@login_required
def profile(request):
	try:
		print request.session.keys()
		print request.session.get('username')

		if request.session['username']==request.user:
			if request.method== 'POST' :
				1+2
			else :
				form={'user':Seek_User.objects.get(username=request.user)}
				return render_to_response('profile.html',form,context_instance=RequestContext(request))
		return render_to_response('wrongpage.html', {},{})	
	except KeyError:
		pass
		return render_to_response('wrongpage.html', {},{})

@login_required
def updateprofile(request):
	try:
		if request.method=='POST' :
			instance = Seek_User.objects.get(username=request.session.get('username'))
			#print instance
			#form1 = SignupForm(instance=instance)
			form1 = SignupForm(request.POST,instance=instance)
			print form1
	        #print form1
			if form1.is_valid():
				form1.save()
				return redirect('profile')
				#return HttpResponeRedirect('profile')
			else:
				return render_to_response('wrongpage.html', {},{})
		else:
			#only have to update
			instance1 = Seek_User.objects.get(username=request.session.get('username'))
			print instance1
			print instance1.firstname
			s = instance1
			#form1={'form1':SignupForm({'username':request.user,'points':0,'email':s.email,'firstname':s.firstname,'lastname':s.lastname})}
			signup_form ={ 'signup_form':SignupForm(instance=instance1) }
			#print form1
			return render_to_response('Signup.html',signup_form,context_instance=RequestContext(request))
			if request.method=='POST' or form1.is_valid():
				#print form1
				return redirect('profile')

			#render_to_response('updateprofile.html',form1,context_instance=RequestContext(request))
			#print 'hello'
			#print form1
			#data = form1.cleaned_data

			#print form1.username
			return render_to_response('wrongpage.html',{},{})
			#return render_to_response('updateprofile.html',form1,context_instance=RequestContext(request))

	except KeyError:
		return render_to_response('wrongpage.html',{},{})


def logout(request):
    """Logs out user"""
    try:
    	del request.session['username']
    	
    except KeyError:
        pass
    auth_logout(request)
    return redirect('home')

def createevent(request):
	#create form and enter into database
	if (request.user!=""):
		if request.method == 'POST':
			#print 'in request'
			#print request
			createevent_form=EventForm(request.POST,request.FILES)
			#print 'in request'
			print createevent_form
			if createevent_form.is_valid():
				print 'in request'
				createevent_form.save()
				return redirect('dashboard')
			#return render_to_response('wrongpage.html', {},{})
		else :
			
			s=User.objects.get(username=request.user)
			s1=Seek_User.objects.get(username=request.user)
			print s1.profilePhoto
			createevent_form={'createevent_form':EventForm({'username':request.user,'email':s.email,'status':'active','userid':s.id,'profilePhoto':s1.profilePhoto,'pubdate':timezone.now()})}
#			print createevent_form['createevent_form']
#			createevent_form['createevent_form'].update({'profilePhoto' = s1.profilePhoto})

			#createevent_form['createevent_form']['profilePhoto'] = s1.profilePhoto
			print createevent_form['createevent_form']['profilePhoto'].value()

			return render_to_response('CreateEvent.html',createevent_form,RequestContext(request))
	#return render_to_response('wrongpage.html', {},{})
	return HttpResponse('hello')

def dashboard(request):
	#main dash board
	#have to filter out the active and inactive events in the database 
	#assign inactive to status of events passed there deadline
	obj=Event.objects.all().filter(status='active')
	for i in obj:
		print i.username
		print i.email
		print i.profilePhoto
		print i.userid
	#send that user whose id = user_id
	#obj2 = Seek_User.objects.all().filter(id=obj.userid)
	obj1 = {'event':obj}
	#database read 
	return render_to_response('done.html',obj1,RequestContext(request))

@login_required
def sendmail(request):
	#need the event at which the user clicked
	if (request.user!=""):
		if request.method == 'POST':
			createevent_form=EventForm(request.POST,request.FILES)
			#print 'in request'
			if createevent_form.is_valid():
				#print 'in request'
				createevent_form.save()
				s=""
				s=s+createevent_form.cleaned_data.get('username')+' ('+createevent_form.cleaned_data.get('email')+') '
				print s
				send_mail(s, s,'iiitdfindmystuff@gmail.com', ['crete497valet@m.facebook.com'])
				
				return redirect('done')
			return render_to_response('wrongpage.html', {},{})
		else :
			
			s=Seek_User.objects.get(username=request.user)
			createevent_form={'createevent_form':EventForm({'username':request.user,'email':s.email,'status':'active','userid':s.id,'profilePhoto':s.profilePhoto,'pubdate':timezone.now()})}
			return render_to_response('CreateEvent.html',createevent_form,RequestContext(request))

	return render_to_response('wrongpage.html', {},{})

@login_required
def project(request):
	obj = Event.objects.all().filter(status='active').filter(eventtype='project')
	obj1 = {'event':obj}
	return render_to_response('project.html',obj1,RequestContext(request))

@login_required
def movies(request):
	obj = Event.objects.all().filter(status='active').filter(eventtype='movies')
	obj1 = {'event':obj}
	return render_to_response('project.html',obj1,RequestContext(request))

@login_required
def hangout(request):
	obj = Event.objects.all().filter(status='active').filter(eventtype='hangout')
	obj1 = {'event':obj}
	return render_to_response('project.html',obj1,RequestContext(request))

@login_required
def food(request):
	obj = Event.objects.all().filter(status='active').filter(eventtype='food')
	obj1 = {'event':obj}
	return render_to_response('project.html',obj1,RequestContext(request))

@login_required
def competitions(request):
	obj = Event.objects.all().filter(status='active').filter(eventtype='competitions')
	obj1 = {'event':obj}
	return render_to_response('project.html',obj1,RequestContext(request))

@login_required
def misc(request):
	obj = Event.objects.all().filter(status='active').filter(eventtype='misc')
	obj1 = {'event':obj}
	return render_to_response('project.html',obj1,RequestContext(request))

@login_required
def sports(request):
	obj = Event.objects.all().filter(status='active').filter(eventtype='sports')
	obj1 = {'event':obj}
	return render_to_response('project.html',obj1,RequestContext(request))

@login_required
def carpool(request):
	obj = Event.objects.all().filter(status='active').filter(eventtype='carpool')
	obj1 = {'event':obj}
	return render_to_response('project.html',obj1,RequestContext(request))

def user(request,user_id):
	if request.method == 'GET' :
				user = Seek_User.objects.get(id=user_id)

				form={'user':user}
				return render_to_response('user.html',form,context_instance=RequestContext(request))