import datetime
import os

from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .forms import TributeForm
from .models import Tribute, Profile, Reading, Hymn, Prayer, Mass


# Create your views here.
class HomeView(View):
    def get(self, request):
        tributes = Tribute.objects.order_by('id')[:5]
        # profile = get_object_or_404(Profile, pk=1)
        # print(profile)
        hero = 'hero'
        form = TributeForm()
        api_key = os.environ.get('GOOGLE_API_KEY')

        event_date = datetime.date(2023, 9, 6)
        context = {
            'form': form,
            'tributes': tributes,
            'hero': hero,
            # 'profile': profile,
            'api_key': api_key,
            'mydate': event_date
        }
        return render(request, 'lonely/index.html', context)

    def post(self, request, email):
        tributes = Tribute.objects.filter(email=email)
        hero = 'hero'
        if request.method == 'POST':
            form = TributeForm(request.POST, files=request.FILES or None)
            print(form)
            if form.is_valid():
                file = request.FILES['image']
                status = request.POST['status']
                if status == 'DRAFT':
                    messages.success(request, 'Draft saved')
                else:
                    messages.success(request, 'Post Published')
                return HttpResponse('OK')
            else:
                print(form.errors)
                form = TributeForm(request.POST)
        else:
            form = TributeForm()
        context = {
            'form': form,
            'tributes': tributes,
            'hero': hero
        }
        return render(request, 'lonely/index.html', context)


def index(request):
    return render(request, 'lonely/index.html')


def read_tribute(request, _id):
    tribute = Tribute.objects.get(id=_id)
    return render(request, 'lonely/inner-page.html', {'tribute': tribute, 'view': 'tribute'})


def add_tribute(request):
    tributes = Tribute.objects.all()
    hero = 'hero'
    if request.method == 'POST':
        form = TributeForm(request.POST, files=request.FILES or None)
        print(form)
        if form.is_valid():
            # file = request.FILES['picture']
            status = request.POST['status']
            form.save()
            if status == 'DRAFT':
                messages.success(request, 'Draft saved')
            else:
                messages.success(request, 'Post Published')

            return HttpResponse('OK')
        else:
            messages.error(request, form.errors.as_data)
            print(form.errors)
            form = TributeForm(request.POST)
    else:
        form = TributeForm()
    context = {
        'tribute_form': form,
        'tributes': tributes,
        'hero': hero
    }
    return render(request, 'lonely/index.html', context)


def publish_post(request, _id, email, status):
    form = TributeForm(initial={'email': email})
    new_post = Tribute.objects.get(id=_id)
    new_post.status = status
    new_post.save()
    tribute = Tribute.objects.filter(email=email)
    context = {
        'article_form': form,
        'posts': tribute
    }
    return render(request, 'lonely/index.html', context)


def update_post(request, _id):
    tribute = Tribute.objects.get(id=_id)
    form = TributeForm(request.POST or None, request.FILES or None, instance=tribute)
    if form.is_valid():
        form.save()

        messages.success(request, 'Post Updated')
        return redirect('core:publish_news')

    tributes = Tribute.objects.filter(author=request.user)
    context = {
        'tribute_form': form,
        'tributes': tributes
    }
    return render(request, 'lonely/index.html', context)


def order_of_mass(request, mass):
    mass = Mass.objects.get(mass=mass)
    readings = Reading.objects.filter(mass=mass).order_by('id')
    hymns = Hymn.objects.filter(mass=mass).order_by('number')
    prayers = Prayer.objects.filter(mass=mass).order_by('number')
    context = {
        'readings': readings,
        'hymns': hymns,
        'prayers': prayers,
        'view': 'mass',
        'mass': mass
    }
    return render(request, 'lonely/inner-page.html', context)


def list_tribute(request):
    all_tributes = Tribute.objects.order_by('id')
    # tributes = all_tributes.order_by('id')[:4]
    tributes_count = all_tributes.count()
    page = request.GET.get('page', 1)
    paginator = Paginator(all_tributes, 20)
    try:
        tributes = paginator.page(page)
    except PageNotAnInteger:
        tributes = paginator.page(1)
    except EmptyPage:
        tributes = paginator.page(paginator.num_pages)
    pages = all_tributes[:tributes_count:20]
    return render(request, 'lonely/inner-page.html',
                  {'tributes': tributes, 'view': 'tributes list', 'pages': pages, 'page': page})


def countdown(request):
    return render(request, 'comingsoon/index.html')


def get_directions(request, location_key):
    return render(request, 'lonely/directions.html',
                  {'location_key': location_key})


# def imageupload(request):
#     form = PhotoForm(request.POST, request.FILES)
#     if request.method == 'POST':
#         pictures = request.FILES.getlist('picture')
#         for picture in pictures:
#             pic = Photo(picture=picture)
#             pic.save()
#         return redirect()
#     context = {'form': form}
#     return render(request, )
