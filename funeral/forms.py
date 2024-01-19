from django.forms import ModelForm, Select, TextInput, Textarea, URLInput, FileInput, DateInput, EmailInput

from .models import Tribute


class TributeForm(ModelForm):
    class Meta:
        model = Tribute
        fields = ['title', 'author', 'email', 'message', 'picture', 'status', 'relation']
        widgets = {'title': TextInput(
            attrs={'class': "form-control w-100 p-2", 'placeholder': 'Title', 'required': 'required'}),
            'message': Textarea(
                attrs={'class': "form-control w-100 p-2", 'placeholder': 'Tribute Message', 'required': 'required'}),
            'author': TextInput(
                attrs={'class': "form-control w-100 p-2", 'placeholder': 'Name', 'required': 'required'}),
            'email': EmailInput(
                attrs={'class': "form-control w-100 p-2", 'placeholder': 'Email', 'required': 'required'}),
            'picture': FileInput(
                attrs={'class': "form-control form-control-lg", 'type': 'file'}),
            'relation': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Relationship', 'required': 'required'}),
            'status': Select(attrs={'class': 'form-control'})

        }


# class PhotoForm(ModelForm):
#     class Meta:
#         model = Photo
#         fields = ['picture']
#         widgets = {
#             'picture': FileInput(
#                 attrs={'class': "form-control form-control-lg", 'type': 'file', 'multiple': 'True', 'name': 'photos'})
#         }
