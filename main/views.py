from django.shortcuts import render, redirect
from .models import User, Trip
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    errs = User.objects.register_validator(request.POST)
    if len(errs) > 0:
        for msg in errs.values():
            messages.error(request, msg)
        return redirect('/')
    password = request.POST['password']
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=hashed,
    )
    request.session['user_id'] = new_user.id
    return redirect('/success')

def login(request):
    errs = User.objects.login_validator(request.POST)
    if errs:
        for msg in errs.values():
            messages.error(request, msg)
        return redirect('/')
    user_list = User.objects.filter(email=request.POST['email'])
    if user_list:
        our_user = user_list[0]
        print(request.POST['password'].encode())
        print(our_user.password)
        if bcrypt.checkpw(request.POST['password'].encode(), our_user.password.encode()):
            print("Passwords match!")
            request.session['user_id'] = our_user.id
            return redirect('/success')
    else:
        messages.error(request, "Login, failed, try again!")
    return redirect('/')

def success(request):
    logged_in_user = User.objects.get(id=request.session['user_id'])
    context = {
        'logged_in_user': logged_in_user,
        'my_trips': Trip.objects.filter(traveler=logged_in_user),
        'joined_trips': Trip.objects.filter(joiner=logged_in_user),
        'other_trips': Trip.objects.exclude(joiner=logged_in_user).exclude(traveler=logged_in_user),
    }
    return render(request, 'dashboard.html', context)

def new(request):
    logged_in_user = User.objects.get(id=request.session['user_id'])
    context = {
        'all_trips': Trip.objects.all(),
        'logged_in_user': logged_in_user,
    }
    return render(request, 'new_trip.html', context)

def create(request):
    errs = User.objects.trip_validator(request.POST)
    if errs:
        for msg in errs.values():
            messages.error(request, msg)
        return redirect('/trips/new')
    Trip.objects.create(
        destination=request.POST['destination'],
        start_date=request.POST['start_date'],
        end_date=request.POST['end_date'],
        plan=request.POST['plan'],
        traveler = User.objects.get(id=request.session['user_id']),
    )
    return redirect('/success')

def view(request, id):
    logged_in_user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=id)
    joined = trip.joiner.all()
    context = {
        'trip': Trip.objects.get(id=id),
        'joined': joined,
        'logged_in_user': logged_in_user,
    }
    return render(request, 'view_trip.html', context)

def edit(request, id):
    logged_in_user = User.objects.get(id=request.session['user_id'])
    context = {
        'trip': Trip.objects.get(id=id),
        'logged_in_user': logged_in_user,
    }
    return render(request, 'edit_trip.html', context)

def edit_trip(request, id):
    trip = Trip.objects.get(id=id)
    errs = User.objects.trip_validator(request.POST)
    if errs:
        for msg in errs.values():
            messages.error(request, msg)
        return redirect(f'/trips/edit/{trip.id}')
    trip.destination=request.POST['destination']
    trip.start_date=request.POST['start_date']
    trip.end_date=request.POST['end_date']
    trip.plan=request.POST['plan']
    trip.save()
    return redirect(f'/trips/view/{trip.id}')

def delete(request, id):
    trip = Trip.objects.get(id=id)
    trip.delete()
    return redirect('/success')

def join(request, id):
    trip = Trip.objects.get(id=id)
    user = User.objects.get(id=request.session['user_id'])
    trip.joiner.add(user)
    return redirect('/success')

def cancel_join(request, id):
    trip = Trip.objects.get(id=id)
    user = User.objects.get(id=request.session['user_id'])
    trip.joiner.remove(user)
    return redirect('/success')

def logout(request):
    request.session.flush()
    return redirect('/')