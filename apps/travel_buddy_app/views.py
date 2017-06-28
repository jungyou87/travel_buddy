from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Trip

# Create your views here.

def createErrorMessages(request, errors):
    for error in errors:
        messages.error(request, error)

def getCurrentUser(request):
    user = User.objects.get(id = request.session['user_id'])
    return user

def main(request):
    print "------------main page-------------"
    # User.objects.all().delete()
    return render(request, 'travel_buddy_app/main.html')

def register(request):
    print "------------register page-------------"
    if request.method=="POST":
        errors =User.objects.register_validation(request.POST)
        print errors
        if not errors:
            user = User.objects.register(request.POST)
            if 'user_id' not in request.session:
                request.session['user_id'] = user.id
            request.session['user_id'] = user.id
            return redirect('/travels')
        createErrorMessages(request, errors)
        return redirect ('/main')

def login(request):
    print "------------login page-------------"
    if request.method=="POST":
        errors =User.objects.login_validation(request.POST)
        print errors

        if not errors:
            user = User.objects.login(request.POST)
            if 'user_id' not in request.session:
                request.session['user_id'] = user.id
            request.session['user_id'] = user.id
            return redirect ('/travels')

        createErrorMessages(request, errors)

        return redirect ('/main')

def travels(request):
    print "------------travels page-------------"
    user = getCurrentUser(request)
    trips = Trip.objects.filter(creator = user)
    joined_trips= Trip.objects.filter(buddy = user)
    othertrips = Trip.objects.all().exclude(creator = user).exclude(buddy=user)

    context ={
        'user' : user,
        'trips' : trips,
        'joined_trips' : joined_trips,
        'othertrips' : othertrips
    }

    return render (request, 'travel_buddy_app/travels.html', context)

def logout(request):
    print "------------logout page-------------"
    request.session.pop('user_id')
    return redirect('/main')

def travels_add(request):
    return render(request,'travel_buddy_app/travel_add.html')

def add_trip(request):
    user = getCurrentUser(request)
    if request.method == "POST":
        errors = Trip.objects.add_trip_validation(request.POST)
        if not errors:
            trip = Trip.objects.add_trip(request.POST, user)
            return redirect ('/travels')
        createErrorMessages(request, errors)
        return redirect('/travels/add')
    return redirect ('/travels')

def destination(request, id):
    user = getCurrentUser(request)
    trip = Trip.objects.get(id = id)

    users = trip.buddy.all()

    context = {
        'trip' : trip,
        'users' : users
    }
    return render(request, 'travel_buddy_app/destination.html', context)

def destination_join(request, id):
    user = getCurrentUser(request)
    trip = Trip.objects.get(id = id)
    trip.buddy.add(user)
    return redirect ('/travels')
