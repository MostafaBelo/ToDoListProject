from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth.models import User as autoUser

from rest_framework.authtoken.models import Token

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required


from .models import data
from .forms import aeForm, CreateUserForm
from .serializers import dataSerializer, userSerializer
from .decorators import *
from django.contrib import messages

# Create your views here.

# def main2(request):
#     cont = {'data': data.objects.all()}
#     return render(request, 'new_main.html', cont)

@unauth_user
def login_view(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('Main')
        messages.info(request, 'Username OR Password is incorrect')
    cont = {}
    return render(request, 'login.html', cont)

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('Main')

@unauth_user
def register_view(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            usered = form.save()

            messages.success(request, 'Account successfully created for ' + form.cleaned_data.get('username'))
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))

            if user is not None:
                login(request, user)
                return redirect('Main')

    cont = {'form':form}
    return render(request, 'register.html', cont)

@login_required(login_url='login')
def main(request):


    cont = {'data':data.objects.filter(task_user=request.user.id)}
    return render(request, 'main.html', cont)

# @login_required(login_url='login')
# def main2(request):
#     cont = {'data':data.objects.filter(task_user=request.user.id)}
#     return render(request, 'new_main.html', cont)

@login_required(login_url='login')
def viewtask(request, id):
    item = data.objects.get(id=id)
    if item.task_user != request.user.id:
        return redirect('Main')
    cont = {'data':item}
    return render(request,'view.html', cont)

@login_required(login_url='login')
def add(request):
    cont = {'form':aeForm}
    return render(request, 'add_edit.html', cont)

@login_required(login_url='login')
def addit(request):
    form = aeForm(request.POST)

    if form.is_valid():
        myreg = data(task=form.cleaned_data['task'],
                    duedate=form.cleaned_data['duedate'],
                    person=form.cleaned_data['person'],
                    done=False,
                     task_user=request.user.id)

        myreg.save()

    return redirect('Main')

@login_required(login_url='login')
def editit(request, itemid):
    if data.objects.get(id=itemid).task_user != request.user.id:
        return redirect('Main')
    form = aeForm(request.POST)

    if form.is_valid():
        myreg = data.objects.get(id=itemid)
        myreg.task = form.cleaned_data['task']
        myreg.duedate = form.cleaned_data['duedate']
        myreg.person = form.cleaned_data['person']

        myreg.save()

    return redirect('Main')

@login_required(login_url='login')
def edit(request, itemid):
    if data.objects.get(id=itemid).task_user != request.user.id:
        return redirect('Main')
    cdata = data.objects.get(id=itemid)
    initial_data = {'task':cdata.task,'duedate':cdata.duedate,'person':cdata.person}
    form = aeForm(initial=initial_data)
    cont = {'form':form, 'itemid':itemid}
    return render(request, 'editing.html', cont)

@login_required(login_url='login')
def removeit(request, itemid):
    if data.objects.get(id=itemid).task_user != request.user.id:
        return redirect('Main')
    item = data.objects.filter(id=itemid)
    item.delete()

    return redirect('Main')

@login_required()
def clearall(request):
    items = data.objects.filter(task_user=request.user.id)
    items.delete()

    return redirect('Main')

@login_required(login_url='login')
def changed(request, itemid, change):
    item = data.objects.get(id=itemid)
    if change == 'False':
        item.done = True
        item.save()
    else:
        item.done = False
        item.save()

    return redirect('Main')


@api_view(['POST'])
def api_register(request):
    if request.method == 'POST':
        # new_user = autoUser(username=request.POST.get('username'),password=request.POST.get('password'),email=request.POST.get('email'))
        new_user = CreateUserForm(request.POST)
        serializer = userSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            accounted = new_user.save()
            data['response'] = 'Successfully registered a new user'
            data['email'] = accounted.email
            data['username'] = accounted.username
            token = Token.objects.get(user=accounted).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)

@api_view(['POST'])
def api_show(request):
    if request.POST.get('tid') == '0':
        userid = Token.objects.get(key=request.POST.get('token')).user_id
        tasked = data.objects.filter(task_user=userid)
        serializer = dataSerializer(tasked, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    try:
        tasked = data.objects.get(id=request.POST.get('tid'))
        if tasked.task_user != Token.objects.get(key=request.POST.get('token')).user_id:
            return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    except data.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = dataSerializer(tasked)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def api_update(request):
    try:
        tasked = data.objects.get(id=request.data['tid'])
    except data.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if Token.objects.get(key=request.data['token']).user_id == tasked.task_user:
        if 'done' in request.data:
            serializer = dataSerializer(tasked, data={'task': request.data['task'], 'duedate': request.data['duedate'], 'person': request.data['person'], 'done': request.data['done'],'task_user': tasked.task_user})
        else:
            serializer = dataSerializer(tasked, data={'task': request.data['task'], 'duedate': request.data['duedate'], 'person': request.data['person'], 'done': False,'task_user': tasked.task_user})
        mydata = {}
        if serializer.is_valid():
            serializer.save()
            mydata['success'] = 'Update successful'
            return Response(data=mydata)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

@api_view(['DELETE'])
def api_del(request):
    # print(request.data['tid'], type(request.data['tid']), request.data['tid'] == '0', request.data['tid'] == 0)
    # mytid = request.data['tid']
    if request.data['tid'] == '0':
        tasked = data.objects.filter(task_user=Token.objects.get(key=request.data['token']).user_id)
        operation = tasked.delete()
        mydata = {}
        if operation:
            mydata['success'] = 'delete successful'
        else:
            mydata['failure'] = 'delete failed'
        return Response(data=mydata)

    try:
        tasked = data.objects.get(id=request.data['tid'])
    except data.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if tasked.task_user == Token.objects.get(key=request.data['token']).user_id:
        operation = tasked.delete()
        mydata = {}
        if operation:
            mydata['success'] = 'delete successful'
        else:
            mydata['failure'] = 'delete failed'
        return Response(data=mydata)

@api_view(['POST'])
def api_add(request):

    if request.method == 'POST':
        tasked = data()
        # request.data['task_user'] = Token.objects.get(key=request.data['token']).user_id
        serializer = dataSerializer(tasked, data={'task':request.data['task'],'duedate':request.data['duedate'],'person':request.data['person'],'task_user':Token.objects.get(key=request.data['token']).user_id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
