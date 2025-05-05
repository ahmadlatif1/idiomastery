import bcrypt
from django.shortcuts import redirect, render
from app.models import *
from django.http import JsonResponse

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
    user_profile=User.objects.get(id=id)
    idioms=Idiom.objects.filter(user=user_profile)
    favorites=Idiom.objects.filter(liked_by__user=user_profile)

    context={
        'user':user_profile,
        'idioms':idioms,
        'sessionid':'',
        'favorites':favorites,
    }
    if 'userid' in request.session:
        context['sessionid']=request.session['userid']

    print('context')
    
    return render(request, 'profile.html',context)

def serve_details(request,id):
    
    user='none'
    liked_idiom=False
    idiom=Idiom.objects.get(id=id)
    if 'userid' in request.session:
        user=User.objects.get(id=request.session['userid'])
        liked_idiom = LikedIdioms.objects.filter(user=user, idiom=idiom).exists()


    idiom=Idiom.objects.get(id=id)
    tags=idiom.tags.all()

    translations='none'
    if idiom.translations.all():
        translations = idiom.translations.all()
    # need to add if idiom is liked

    context={
        'user':user,
        'idiom':idiom,
        'translations':translations,
        'tags': tags,
        
        'liked': liked_idiom,
        'related':Idiom.objects.filter(related=idiom.related)
        
    }
    print('related:',context['related'])
    print('itranslations',translations)
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
        print(errors)
        return render(request, 'registration.html',{"errors": errors})
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
    errors={}
    if user:
        logged_user=user[0]
        print('user:',user)
        if bcrypt.checkpw(request.POST['password'].encode('utf-8'), logged_user.password.encode('utf-8')):
            print("logged user",logged_user)
            request.session['userid']=logged_user.id
        else:
            errors['password']='Check password'
    else: errors['email']="Invalid email address"
    if len(errors)>0:
        print(errors)
        return render(request, 'login.html',{"errors": errors})
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')


def create(request):
    errors=Idiom.objects.idiom_validator(post=request.POST)
    if len(errors)>0:
        print(errors)
        return render( request, 'create.html',{"errors": errors})
    # validate input
    phrase=request.POST['phrase']
    meaning=request.POST['meaning']
    example=request.POST['example']
    origin=request.POST['origin']
    
    # we handle adding tags by separating them by commas in the input field
    # tags_string=request.POST['tags']

    user=User.objects.get(id=request.session['userid'])
    idiom=Idiom.objects.create(phrase=phrase, meaning=meaning, example=example, origin=origin, user=user)
    idiom.related=idiom.id
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


def search(request):
    
    query=''
    if request.method == "  GET":
        query=request.GET.get('search')
    words=query.split(' ')
    idioms = Idiom.objects.none()
    for word in words:
        idioms |= Idiom.objects.filter(phrase__icontains=word) | Idiom.objects.filter(meaning__icontains=word)

    user='none'
    if 'userid' in request.session:
        user=User.objects.get(id=request.session['userid'])

    context={
        'user':user,
        'results':idioms,
        'idioms':Idiom.objects.all(),
    }
    print("idioms: ",idioms)
    return render(request,'explore.html',context)

def addtranslation(request,id):

    # create a translation
    idiom=Idiom.objects.get(id=id)
    text=request.POST['text']
    language=request.POST['language']
    Translation.objects.create(text=text,idiom=idiom,language=language)


    return redirect(f"/{id}")



def add_tag(request,tag,id):
    print("add tag",tag)

    if Tag.objects.filter(name=tag).exists():
        print("tag exists")
    else:
        print("tag does not exist")
        Tag.objects.create(name=tag)

    idiom=Idiom.objects.get(id=id)
    pagetag=Tag.objects.get(name=tag)
    print(pagetag)
    
    idiom.tags.add(pagetag)
    return JsonResponse({'message': 'Tag added successfully', 'tag': tag}, status=200)



def like_idiom(request, id):

    if 'userid' not in request.session:
        return JsonResponse({'error': 'User not logged in'}, status=401)
    user = User.objects.get(id=request.session['userid'])
    idiom = Idiom.objects.get(id=id)
    
    # Check if the user has already liked the idiom
    liked_idiom, created = LikedIdioms.objects.get_or_create(user=user, idiom=idiom)

    if not created:
        # Unlike the idiom
        liked_idiom.delete()
        idiom.score -= 1
        liked = False  # Indicate that the user has unliked the idiom
    else:
        # Like the idiom
        idiom.score += 1
        liked = True  # Indicate that the user has liked the idiom
    
    idiom.save()
    

    return JsonResponse({'message': 'Idiom liked successfully', 'score': idiom.score, 'liked': liked}, status=200)


def search_tags(request,search):

    print("search tags",request,search)
    
    if request.method == "GET":
        tags = Tag.objects.filter(name__icontains=search)
        taglist=[]
        for tag in tags:
            taglist.append(tag.name)

        print("taglist",taglist)
        return JsonResponse({'tags': taglist}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)