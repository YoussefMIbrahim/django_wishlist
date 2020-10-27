from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm 
# Create your views here.

def place_list(request):

    if request.method == 'POST':
        #new place
        form = NewPlaceForm(request.POST)
        place = form.save() #creates a model onject from form. Already know columns because we gave it the model
        if form.is_valid(): # validates with the database restraints
            place.save()  #saves object to database
            return redirect('place_list') #reloads that url which is the home page

    places = Place.objects.filter(visted=False).order_by('name')
    new_place_form = NewPlaceForm()
    return render(request, 'trave_wishlist/wishlist.html', {'places' : places, 'new_place_form': new_place_form })  

def about(request):
    author = 'Youssef'
    about = 'A website to create a list of places to visit'

    return render(request, 'trave_wishlist/about.html', {'author': author, 'about' : about})

def places_visited(request):
    visited = Place.objects.filter(visted=True)
    return render(request, 'trave_wishlist/visited.html', {'visited':visited})

def place_was_visited(request, place_pk):
    if request.method == 'POST':    
        place = get_object_or_404(Place, pk=place_pk) # getting one specific item from db, in this cake it's from the pk column
        # place = Place.objects.get(pk=place_pk) 
        place.visted = True # changing that items visited value
        place.save()

    return redirect('place_list')