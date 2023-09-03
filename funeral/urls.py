from django.urls import path

from .views import HomeView, index, add_tribute, read_tribute, order_of_mass, list_tribute, get_map, get_directions

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('add_tribute', add_tribute, name='add_tribute'),
    path('tribute/<_id>', read_tribute, name='read_tribute'),
    path('mass/<mass>', order_of_mass, name='mass'),
    path('tributes', list_tribute, name='list_tributes'),
    path('map/<location>/<lat>/<lng>/<location_key>', get_map, name='get_map'),
    path('directions/<location_key>', get_directions, name='get_directions'),
]