from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .forms import TributeForm
from .models import Tribute


# Create your views here.
class HomeView(View):
    def get(self, request):
        tributes = Tribute.objects.all()
        hero='hero'
        form = TributeForm()
        context = {
            'form': form,
            'tributes': tributes,
            'hero':hero
        }
        return render(request, 'lonely/index.html', context)

    def post(self, request, email):
        tributes = Tribute.objects.filter(email=email)
        hero='hero'
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
            'hero':hero
        }
        return render(request, 'lonely/index.html', context)


def index(request):
    return render(request, 'lonely/index.html')


def read_tribute(request, _id):
    tribute = Tribute.objects.get(id=_id)
    return render(request, 'lonely/inner-page.html', {'tribute': tribute})


def add_tribute(request):
    tributes = Tribute.objects.all()
    hero='hero'
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
        'hero':hero
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
