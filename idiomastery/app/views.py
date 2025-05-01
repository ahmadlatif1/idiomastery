import bcrypt
from django.shortcuts import redirect, render
from app.models import *

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def serve_explore(request):
    return render(request, 'explore.html', {})

def serve_login(request):
    return render(request, 'login.html', {})

def serve_registration(request):
    return render(request, 'registration.html', {})

def serve_profile(request,id):
    context={}
    context['user']=User.objects.get(id=id)
    return render(request, 'profile.html',context)

def serve_details(request,id):
    context={}
    context['idiom']=Idiom.objects.get(id=id)
    return render(request, 'details.html',context)

def serve_about(request):
    return render(request, 'about.html', {})

def serve_create(request):
    return render(request, 'create.html', {})

def register(request):

    errors=User.objects.validateregistry(postdata=request.POST)
    if len(errors)>0:
        return redirect('/',errors)
    # validate input
    password= request.POST['password']
    pw_hash=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
    first_name=request.POST['first_name']
    last_name=request.POST['last_name']
    email=request.POST['email']
    User.objects.create(first_name=first_name,last_name=last_name,email=email,password=pw_hash)

    request.session['userid']=User.objects.get(email=email).id
    return redirect("/")

def login(request):
    user=User.objects.filter(email=request.POST['email'])
    if user:
        logged_user=user[0]
        if bcrypt.checkpw(request.POST['password'].encode('utf-8'), logged_user.password.encode('utf-8')):
            request.session['userid']=logged_user.id
            
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')


def create(request):
    errors=Idiom.objects.validateidiom(postdata=request.POST)
    if len(errors)>0:
        return redirect('/create',errors)
    # validate input
    phrase=request.POST['phrase']
    meaning=request.POST['meaning']
    example=request.POST['example']
    description=request.POST['description']
    tags=request.POST['tags'] # this should be a list of tags, but for now we will just take it as a string
    user=User.objects.get(id=request.session['userid'])
    Idiom.objects.create(phrase=phrase, meaning=meaning, example=example, description=description, tags=tags, user=user)

    return redirect("/")

def delete(request, id):
    idiom = Idiom.objects.get(id=id)
    idiom.delete()
    return redirect('/')
    
def edit(request, id):
    errors=Idiom.objects.validateidiom(postdata=request.POST)
    if len(errors)>0:
        return redirect('/create',errors)
    # validate input
    idiom = Idiom.objects.get(id=id)
    idiom.phrase = request.POST['phrase']
    idiom.meaning = request.POST['meaning']
    idiom.example = request.POST['example']
    idiom.description = request.POST['description']
    idiom.tags = request.POST['tags'] # this should be a list of tags, but for now we will just take it as a string
    idiom.save()

    return redirect("/")