from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf.urls import url
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

# Create your views here.


@login_required
def place_list(request):

    if request.method == 'POST':
        #new place
        form = NewPlaceForm(request.POST)
        place = form.save(commit=False) #creates a model onject from form. Already know columns because we gave it the model
        place.user = request.user
        if form.is_valid(): # validates with the database restraints
            place.save()  #saves object to database
            return redirect('place_list') #reloads that url which is the home page

    places = Place.objects.filter(user=request.user).filter(visted=False).order_by('name')
    new_place_form = NewPlaceForm()
    return render(request, 'trave_wishlist/wishlist.html', {'places' : places, 'new_place_form': new_place_form })  

def about(request):
    author = 'Youssef'
    about = 'A website to create a list of places to visit'

    return render(request, 'trave_wishlist/about.html', {'author': author, 'about' : about})

@login_required
def places_visited(request):
    visited = Place.objects.filter(visted=True)
    return render(request, 'trave_wishlist/visited.html', {'visited':visited})


@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':    
        place = get_object_or_404(Place, pk=place_pk) # getting one specific item from db, in this cake it's from the pk column
        if place.user == request.user:
        # place = Place.objects.get(pk=place_pk) 
            place.visted = True # changing that items visited value
            place.save()
        else:
            return HttpResponseForbidden()

    return redirect('place_list')


@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)

    if place.user != request.user:
        return HttpResponseForbidden()
        
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip infromation updated')
        else:
            messages.error(request, form.errors)

        return redirect('place_details', place_pk=place_pk)

    else:

        #forms for place being visited or not visited

        if place.visted:
            review_form = TripReviewForm(instance=place)
            return render(request, 'trave_wishlist/place_detail.html', {'place':place, 'review_form' : review_form})
        else:
            return render(request, 'trave_wishlist/place_detail.html', {'place':place})



@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()
