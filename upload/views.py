from django.db.models.deletion import SET_NULL
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, redirect
from .models import Sound, Category
from datetime import datetime
from login_app.models import User
from django.conf import settings
from django.http import HttpResponse
from django.http import Http404
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import os

def upload(request):
    logged_user = User.objects.get(id=request.session['logged_user'])
    try:
        Sound.objects.create( #re-did the upload form manually, model form was limited.
        # title=request.POST['ftitle'].title(),
        title=request.POST['ftitle'].title() or request.FILES['fsoundfile'] ,
        category =  Category.objects.get(id=request.POST['fcat']),
        soundfile = request.FILES['fsoundfile'],
        created_by = User.objects.get(id=request.session['logged_user']),
        created_at = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    )
    except Exception:
        messages.info(request,"select a file to upload")
    return redirect('/home')
    
def playsound(request):
    #messages = Message.objects.all().order_by('-created_at')[:5]# display last 5
    logged_user = User.objects.get(id = request.session['logged_user'])
    catalog = Sound.objects.all()
    for sound in catalog:
        print(sound.title)
    categories = Category.objects.all()
    lastsound= Sound.objects.last()
    soundfile = lastsound.soundfile if lastsound else None
    print("the file.soundfile",soundfile)
    for filename, file in request.FILES.items():# find the key
        name = request.FILES[filename].name
        print('name is', name)

    context= {
    'logged_user':logged_user,
    'soundfile': soundfile,
    'categories':categories,
    'catalog':catalog,
    }

    return render(request, 'sounds.html', context)

def details(request, id):
    logged_user = User.objects.get(id=request.session['logged_user'])
    the_sound = Sound.objects.get(id=id)
    soundfile = the_sound
    print(the_sound.__dict__)
    print(the_sound.fans)
    print("The file is",the_sound)
    context = {
        'sound':the_sound,
        'soundfile': soundfile,
        'logged_user':logged_user,
    }
    return render(request, 'details.html', context)


def delete_entry(request,id):
    entry = Sound.objects.get(id=id)
    print("***************************deleting file at media/sounds/"+str(entry))
    entry.delete()
    os.remove("media/sounds/"+str(entry))
    return redirect('/home')


def entry_edit(request,id):
    the_sound = Sound.objects.get(id=id)
    cat = Category.objects.get(sound=the_sound)
    print("cat is", cat.slug)
    categories = Category.objects.all()
    # soundfile = the_sound
    print(the_sound.__dict__)
    context = {
        'sound':the_sound,
        # 'soundfile': soundfile,
        'categories': categories,
    }
    return render(request,'entry-edit.html',context)

def process(request,id):#sound
    sound_to_edit = Sound.objects.get(id=id)
    sound_to_edit.title = request.POST['ftitle'].title()
    # print(request.POST['fcat'])
    #wrong! sound_to_edit.category = request.POST['fcat'].title()
    sound_to_edit.category= Category.objects.get(id=request.POST['fcat'])
    sound_to_edit.save()
    messages.success(request,"Item updated.")

    return redirect(f'/sounds/{id}/details')

def edit_cat(request,id):
    cat = Category.objects.get(id=id)
    print("cat is",cat.slug)
    cat.title = request.POST['ftitle'].title()
    sound_id = request.POST['sound_id'] #IMPORTANT!to redirect correctly from hidden input
    cat.save()
    messages.success(request,"Category updated.")
    return redirect(f'/sounds/{sound_id}/entry_edit')

def add_cat(request):
    sound_id = request.POST['sound_id']#for redirect
    errors = Category.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/sounds/{sound_id}/entry_edit')

    else:
        Category.objects.create(
        title = request.POST['ftitle'],
        slug = request.POST['fslug'],
        )
    messages.success(request, "New category added!")
    return redirect(f'/sounds/{sound_id}/entry_edit')
        
def add_to_fav(request,id):
    logged_user = User.objects.get(id=request.session['logged_user'])
    the_sound = Sound.objects.get(id=id)

    if logged_user in the_sound.fans.all():
        logged_user.faves.remove(the_sound)
    else:
        logged_user.faves.add(the_sound)

    context = {
        'sound':the_sound,
    }
    return render(request,'details.html',context)

def delete_cat(request):
    try:
        entry = Category.objects.get(id=request.POST['fcat'])
        entry.delete()
        sound_id = request.POST['sound_id']
        messages.info(request,"Category deleted.")
    except Exception:
        messages.info(request,"select category to delete.")
        sound_id = request.POST['sound_id']
    return redirect (f'/sounds/{sound_id}/entry_edit')



