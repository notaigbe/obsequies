from django.urls import path

from .views import HomeView, index, add_tribute, read_tribute, order_of_mass, list_tribute

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('add_tribute', add_tribute, name='add_tribute'),
    path('tribute/<_id>', read_tribute, name='read_tribute'),
    path('mass/<mass>', order_of_mass, name='mass'),
    path('tributes', list_tribute, name='list_tributes'),
]