from django.urls import path
from .views import show,delete,create,update,load_cities,load_states

urlpatterns=[
    path('show/',show,name='show'),
    path('update/',update,name='update'),
    path('create/',create,name='create'),
    path('delete/',delete,name='delete'),
    path('ajax/load-states/', load_states, name='ajax_load_states'),
    path('ajax/load-cities/', load_cities, name='ajax_load_cities'),

]