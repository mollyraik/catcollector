from django.shortcuts import render, redirect # <-- this is for rendering templates
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cat, Toy, Photo
from .forms import FeedingForm
import uuid
import boto3
# from django.http import HttpResponse <-- this was just for sending a basic response

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'catcollector-tarzan'

#  we use this file to define controller logic
# NOTE: each controller is defined using either a function or a class
# NOTE: all view functions take at least one required positional argument: request

# dummy cat data for prototyping
'''
class Cat:
    def __init__(self, name, breed, description, age):
        self.name = name
        self.breed = breed
        self.description = description
        self.age = age

cats = [
  Cat('Lolo', 'tabby', 'foul little demon', 3),
  Cat('Sachi', 'tortoise shell', 'diluted tortoise shell', 0),
  Cat('Raven', 'black tripod', '3 legged cat', 4),
]
'''

def home(request):
    # NOTE responses are returned from view function
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def cats_index(request):
    cats = Cat.objects.filter(user=request.user)
    return render(request, 'cats/index.html', {
        'cats': cats,
    })

@login_required
def cat_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    feeding_form = FeedingForm()

    # step 1) create a list of toys the cat has
    cat_toy_ids = cat.toys.all().values_list('id') # gives list of toy ids belonging to a cat
    # step 2) create a list of toys the cat doesn't have
    toys_cat_doesnt_have = Toy.objects.exclude(id__in=cat_toy_ids)

    return render(request, 'cats/detail.html', {
        'cat': cat,
        'feeding_form': feeding_form,
        'toys': toys_cat_doesnt_have
    })

@login_required
def add_feeding(request, cat_id):
    # create a new model instance of feeding
    form = FeedingForm(request.POST) # {'meal': 'B', date: '2023-04-05', cat_id: None}
    # validate user input provided from form submission
    if form.is_valid():
       new_feeding = form.save(commit=False) # create an in-memory instance without saving to the database
       new_feeding.cat_id = cat_id # attach the associated cat's id to the cat_id attr
       new_feeding.save() # this will save a new feeding to the database
    # as long as form is valid we can associate the related cat to the new feeding
    # return a redirect response to the client
    return redirect('cat_detail', cat_id=cat_id)

@login_required
def assoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('cat_detail', cat_id=cat_id)

@login_required
def remove_assoc_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect('cat_detail', cat_id=cat_id)

# URL /accounts/signup -- GET/POST
def signup(request):
    error_message = ''
    # POST request
    if request.method == 'POST':
        # create a user using the UserCreationForm -- this way we can validate the form
        form = UserCreationForm(request.POST)
        # check if the form inputs are valid
        if form.is_valid():
        # if valid; save new user to the database
            user = form.save()
            # login the new user
            login(request, user)
            # redirect to the cats index page
            return redirect('cats_index')
        else:
        # else: generate an error message -- 
            error_message = 'Invalid sign up - please try again'

    # GET requests
        # send an empty form to the client
    form = UserCreationForm()
    return render(request, 'registration/signup.html', { 
        'form': form, 
        'error': error_message
    })

def add_photo(request, cat_id):
    # attempt collect photo submission from request
    photo_file = request.FILES.get('photo-file', None)
    # if photo file is present
    if photo_file:
        # set up s3 client object - obj w methods for working w s3
        s3 = boto3.client('s3')
        # create a unique name for the photo file
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # try to upload file to aws
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # generate a unique url for the image
            url = f'{S3_BASE_URL}{BUCKET}/{key}'
            # save the url as a new instance of the photo model
            Photo.objects.create(url=url, cat_id=cat_id)
            # MAKE SURE we associate the cat w the photo model instance
        # if there is a exception (error)
        except Exception as error:
            # print error message for debugging
            print('Photo upload failed')
            print(error)
    # redirect user to cat detail page regardless if successful
    return redirect('cat_detail', cat_id=cat_id)

class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = ('name', 'breed', 'description', 'age') # adds all fields to the model form
        # could alternately provide some of the fields in a list or tuple
    template_name = 'cats/cat_form.html'
    # success_url = '/cats/'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields = ('name', 'breed', 'description', 'age')
    template_name = 'cats/cat_form.html'

class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    success_url = '/cats/'
    template_name = 'cats/cat_confirm_delete.html'

class ToyList(LoginRequiredMixin, ListView):
    model = Toy
    template_name = 'toys/toy_list.html'

class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy
    template_name = 'toys/toy_detail.html'

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'
    template_name = 'toys/toy_form.html'

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = '__all__'
    template_name = 'toys/toy_form.html'

class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'
    template_name = 'toys/toy_confirm_delete.html'

