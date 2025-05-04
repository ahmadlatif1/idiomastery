import bcrypt
from django.shortcuts import redirect, render
from app.models import *

# Create your views here.


def serve_explore(request):
    user='none'
    if 'userid' in request.session:
        user=User.objects.get(id=request.session['userid'])

    context={
        'user':user,
        'idioms':Idiom.objects.all(),
        'tags':Tag.objects.all()
    }
    return render(request, 'explore.html', context)

def serve_login(request):
    
    return render(request, 'login.html', {})

def serve_registration(request):
    return render(request, 'registration.html', {})

def serve_profile(request,id):
    context={
        'user':User.objects.get(id=id),
        'idioms':Idiom.objects.filter(user=id),
    }
    return render(request, 'profile.html',context)

def serve_details(request,id):
    
    user='none'
    if 'userid' in request.session:
        user=User.objects.get(id=request.session['userid'])

    context={
        'user':user,
        'idiom':Idiom.objects.get(id=id),
        
    }
    return render(request, 'details.html',context)

def serve_about(request):
    user='none'
    if 'userid' in request.session:
        user=User.objects.get(id=request.session['userid'])

    return render(request, 'about.html', {'user':user})

def serve_create(request):
    user='none'
    if 'userid' in request.session:
        user=User.objects.get(id=request.session['userid'])

    return render(request, 'create.html', {'user':user})

def get_profile(request):
    if 'userid' in request.session:
        user=request.session['userid']
        return redirect(f'/profile/{user}')
    else:
        return redirect('/login')

def register(request):
    # NOTE TO MAKE SURE TO ADD CONFIRM PASSWORD TO VALIDATION
    errors=User.objects.user_validator(post=request.POST)
    if len(errors)>0:
        return redirect('/',errors)
    # validate input
    password= request.POST['password']
    pw_hash=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
    firstname=request.POST['firstname'].capitalize()
    lastname=request.POST['lastname'].capitalize()
    email=request.POST['email']
    User.objects.create(firstname=firstname,lastname=lastname,email=email,password=pw_hash)

    request.session['userid']=User.objects.get(email=email).id
    return redirect("/")

def login(request):
    print("post request",request.POST)
    user=User.objects.filter(email=request.POST['email'])
    if user:
        logged_user=user[0]
        print('user:',user)
        if bcrypt.checkpw(request.POST['password'].encode('utf-8'), logged_user.password.encode('utf-8')):
            print("logged user",logged_user)
            request.session['userid']=logged_user.id
            
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')


def create(request):
    errors=Idiom.objects.idiom_validator(post=request.POST)
    if len(errors)>0:
        print(errors)
        return redirect('/create',errors)
    # validate input
    phrase=request.POST['phrase']
    meaning=request.POST['meaning']
    example=request.POST['example']
    origin=request.POST['origin']
    # we handle adding tags by separating them by commas in the input field
    # tags_string=request.POST['tags']

    user=User.objects.get(id=request.session['userid'])
    idiom=Idiom.objects.create(phrase=phrase, meaning=meaning, example=example, origin=origin, user=user)

    # tags_list = [tag.strip() for tag in tags_string.split(',')]
    # for tag_name in tags_list:

    #     idiom.tags.add(Tag.objects.get(name=tag_name))

    print("IDIOM CREATED?",idiom)
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
    idiom.origin = request.POST['origin']
    idiom.tags = request.POST['tags'] # this should be a list of tags, but for now we will just take it as a string
    idiom.save()

    return redirect("/")
