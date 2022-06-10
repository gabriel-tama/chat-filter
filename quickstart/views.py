from django.shortcuts import render,redirect

# Create your views here.

def index(request,**kwargs):
    if request.method=="GET":
        return render(request,'chat/index.html',{"room_name":None})
    else:
        room_name= request.POST.get('room')
        username= request.POST.get('username')
        request.session['room']=room_name
        request.session['username']=username
        return redirect('{}/'.format(room_name))

def room(request, room_name):
    username= request.session.get('username')
    print(username)
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'username':str(username),
    })