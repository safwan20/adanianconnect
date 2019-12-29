import operator
from functools import reduce
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from .forms import UserRegisterForm,ProfileUpdateForm,UserUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Profile,Message
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
import re
import json

def register(request):
    if not request.user.is_authenticated :
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                fn = form.cleaned_data.get('first_name').capitalize()
                ln = form.cleaned_data.get('last_name').capitalize()
                u = form.cleaned_data.get('username').lower()
                p = form.cleaned_data.get('password1')
                e = form.cleaned_data.get('email')
                p = make_password(p)

                user = User.objects.all()

                if user.filter(username=u).exists():
                    messages.error(request, "This username has already existed.")
                    return render(request, "register.html", {'form': form})

                if user.filter(email=e).exists():
                    messages.error(request, "This email has already existed.")
                    return render(request, "register.html", {'form': form})

                else :
                    user = User(username=u, first_name=fn, last_name=ln, email=e, password=p)
                    user.save()
                    messages.success(request,"Account created")
                    return redirect('/login')
        else:
            form = UserRegisterForm()
        return render(request, "register.html", {'form': form})
    else :
        return redirect('/home')


@login_required()
def profile(request) :
    return render(request,"profile.html")


@login_required()
def show(request,id):
    profiles = Profile.objects.get(id=id)
    is_liked = False
    if profiles.lkes.filter(id=request.user.id).exists() :
        is_liked = True
    params = {
               'profiles': profiles,
              'is_liked': is_liked,
              'total_likes': profiles.total_likes(),
              }
    return render(request, 'show.html', params)





def like(request) :
    profiles = get_object_or_404(Profile,id = request.POST.get('kop'))
    mark = get_object_or_404(Profile, id=request.user.profile.id)
    print(mark)
    is_liked = False
    if profiles.lkes.filter(id=request.user.id).exists() :
        profiles.lkes.remove(request.user)
        mark.book.remove(profiles.user)
        is_liked = False
    else :
        profiles.lkes.add(request.user)
        mark.book.add(profiles.user)
        is_liked = True
    return HttpResponseRedirect(profiles.get_absolute_url(profiles.id))


@login_required()
def friends(request) :
    profiles = Profile.objects.get(id=request.user.profile.id)
    params = {
        'profiles': profiles,
    }
    return render(request,"friend.html",params)


@login_required()
def delete(request):
    user = User.objects.get(id=request.user.id)
    user.delete()
    messages.error(request,"Account deleted")
    return redirect('/login')



@login_required()
def home(request) :
    profiles = Profile.objects.all()
    messages = Message.objects.all().filter(to=request.user.username).filter(read=0)


    names = []
    for i in profiles :
        names.append(i.user.first_name)

    n = json.dumps(names)

    if 'name' in request.GET :
        name = request.GET['name']
        if name :
            name = name.capitalize()
            profiles = profiles.filter(user__first_name=name)
            if len(profiles) == 0 :
                print("ha zero hai")
                profiles = Profile.objects.all()
                profiless = profiles.filter(user__last_name=name)
                print(profiless)
                paginator = Paginator(profiless, 15)
                page = request.GET.get('page')
                profiless = paginator.get_page(page)
                return render(request, "home.html", {'profiles': profiles, 'jp': 1,'n':n})
            else :
                paginator = Paginator(profiles, 15)
                page = request.GET.get('page')
                profiles = paginator.get_page(page)
                return render(request, "home.html", {'profiles': profiles, 'jp': 1,'n':n})


    if ('sem' in request.GET) and (request.GET['sem']!='Semester') :
        print("yahi")
        sem = request.GET['sem']
        if sem :
            if 'lang' in request.GET and (request.GET['lang']!='Language'):
                print("k11")
                brr = []
                lang = request.GET['lang']
                brr.append(lang)
                if lang!='Language':
                    profiles = Profile.objects.filter(reduce(operator.and_, [Q(lang__icontains=c) for c in brr])).filter(
                        sem=sem)
                    paginator = Paginator(profiles, 15)
                    page = request.GET.get('page')
                    profiles = paginator.get_page(page)
                    return render(request, "home.html", {'profiles': profiles, 'jp': 1,'n':n})
                else:
                    return redirect('/home')

            if 'tech' in request.GET and (request.GET['tech']!='Technology'):
                print("k2")
                arr = []
                tech = request.GET['tech']
                arr.append(tech)
                if tech:
                    if tech != "Technology":
                        profiles = Profile.objects.filter(reduce(operator.and_, [Q(tech__icontains=c) for c in arr])).filter(
                        sem=sem)
                        paginator = Paginator(profiles, 15)
                        page = request.GET.get('page')
                        profiles = paginator.get_page(page)
                        return render(request, "home.html", {'profiles': profiles, 'jp': 1,'n':n})
                    else:
                        return redirect('/home')

            else :
                print("no")
                profiles = profiles.filter(sem=sem)
                paginator = Paginator(profiles, 15)
                page = request.GET.get('page')
                profiles = paginator.get_page(page)
                return render(request, "home.html", {'profiles': profiles, 'jp': 1,'n':n})




    if 'tech' in request.GET and (request.GET['tech']!='Technology'):
        print("techies")
        arr = []
        tech = request.GET['tech']
        arr.append(tech)
        if tech :
            print(arr)
            if tech != "Technology" :
                queryset = Profile.objects.none()
                profiles = Profile.objects.filter(reduce(operator.and_, [Q(tech__icontains=c) for c in arr]))

                for i in profiles :
                    have = i.tech.replace('[', "").replace("]", "").split(',')
                    print(have)
                    for c in arr :
                        for j in have :
                            j = j.replace('"','').replace("'",'')
                            c = c.strip()
                            j = j.strip()
                            if c == j :
                                print("yes")
                                queryset |=  Profile.objects.filter(id=i.id)
                                break


                profiles = queryset


                paginator = Paginator(profiles, 15)
                page = request.GET.get('page')
                profiles = paginator.get_page(page)
                return render(request, "home.html", {'profiles': profiles, 'jp': 1,'n':n})
            else :
                return redirect('/home')

    if 'lang' in request.GET :
        brr = []
        lang = request.GET['lang']
        brr.append(lang)
        if lang :
            if lang != "Language" :

                #new code
                queryset = Profile.objects.none()
                profiles = Profile.objects.filter(reduce(operator.and_, [Q(lang__icontains=c) for c in brr]))


                for i in profiles :
                    have = i.lang.replace('[', "").replace("]", "").split(',')
                    print(have)
                    for c in brr :
                        for j in have :
                            j = j.replace('"','').replace("'",'')
                            c = c.strip()
                            j = j.strip()
                            print(c,j)
                            if c == j :
                                print("yes")
                                queryset |=  Profile.objects.filter(id=i.id)
                                break


                profiles = queryset

                paginator = Paginator(profiles,15)
                page = request.GET.get('page')
                profiles = paginator.get_page(page)
                return render(request, "home.html", {'profiles': profiles, 'jp': 1,'n':n})
            else :
                return redirect('/home')


    else :
        print("yes gaya")
        paginator = Paginator(profiles, 15)
        page = request.GET.get('page')
        profiles = paginator.get_page(page)
        return render(request, "home.html", {'profiles': profiles, 'jp': 2,'n':n,'size':len(messages)})


@login_required()
def edit(request) :
    if not request.user.is_authenticated:
        return redirect('login')
    else :
        if request.method == 'POST':
            p_form = ProfileUpdateForm(request.POST,
                                       request.FILES,
                                       instance=request.user.profile)
            if p_form.is_valid():
                p_form.save()
                return redirect('profile')

        else:
            p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'p_form': p_form
        }

    return render(request,"edit.html",context)





def editu(request) :
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            if u_form.is_valid():
                fn = u_form.cleaned_data.get('first_name').capitalize()
                ln = u_form.cleaned_data.get('last_name').capitalize()
                u = u_form.cleaned_data.get('username').lower()
                e = u_form.cleaned_data.get('email')
                user = User.objects.get(id = request.user.id)
                user.first_name = fn
                user.last_name = ln
                user.username = u
                user.email = e
                user.save()
                return redirect('profile')

        else:
            u_form = UserUpdateForm(instance=request.user)


        context = {
            'u_form': u_form
        }

    return render(request, "editu.html", context)





def login(request) :
    if not request.user.is_authenticated:
        if request.method == 'POST' :
            username = request.POST.get('username').lower()
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/home')
            else:
                messages.error(request,"Invalid credentials")
                return render(request, "registration/login.html", {'j': 5})
        else :
            return render(request, "registration/login.html",{'redirect_authenticated_user': True})
    else :
        return redirect('/home')


@login_required()
def stats(request) :
    profiles = Profile.objects.all()
    arr = []
    brr = []

    record = {}
    record1 = {}

    for i in profiles:
        arr.append(re.findall("'(.*?)'",i.tech))

    for i in profiles:
        brr.append(re.findall("'(.*?)'",i.lang))

    for i in arr:
        for j in i:
            if record.get(j) == None:
                record[j] = 0
            else:
                record[j] += 1

    for i in brr:
        for j in i:
            if record1.get(j) == None:
                record1[j] = 0
            else:
                record1[j] += 1


    arr1 = []
    brr1 = []

    for i in record :
        lis = []
        lis.append(i)
        lis.append(record[i])
        arr1.append(lis)


    for i in record1 :
        lis = []
        lis.append(i)
        lis.append(record1[i])
        brr1.append(lis)


    json_list = json.dumps(arr1)
    json_list1 = json.dumps(brr1)

    params = {'json_list': json_list,'json_list1':json_list1}

    return render(request,"stats.html",params)


@login_required()
def messagebox(request,id) :
    if request.method == 'POST' :
        text = request.POST.get('message')
        # person = User.objects.get(id=id)
        person = Profile.objects.get(id = id)
        print(person.user.username,text)
        message  =  Message(to=person.user.username,froms=request.user.username,message=text)
        message.save()
        messages.success(request,"message send")
        return redirect("/show/" + str(person.id))
    else :
        return render(request,'messagebox.html')


@login_required()
def messageshow(request) :
    messages = Message.objects.all().filter(to = request.user.username)
    context = {
        'messages' : messages[::-1]
    }
    print(messages)
    return render(request,'showmessages.html',context)



@login_required()
def singlemessage(request,id) :
    message = Message.objects.get(id=id)
    look = Profile.objects.get(user__username=message.froms)
    context = {
        'message' : message,
        'look' : look
    }
    print(look)
    message.read = 1
    message.save()
    return render(request,'singlemessage.html',context)




