

from django.shortcuts import redirect, render
from .models import *
from .forms import *

def create(request):
    form=PersonForm()
    if request.method=='POST':
        form=PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show')

    return render(request,'Customer_Address.html',{'form':form})

def update(request,id):
    record=Person.objects.get(id=id)
    form=PersonForm(instance=record)
    if request.method=='POST':
        form=PersonForm(request.POST,instance=record)
        if form.is_valid():
            form.save()
            return redirect('show')

    return render(request,'Customer_Address.html',{'form':form})

def delete(request,id):
    record=Person.objects.get(id=id)
    record.delete()
    redirect('show')

def show(request):
    record=Person.objects.all()
    return render(request,'Show_Customer_Address.html',{'record':record})


def load_states(request):
    country_id = request.GET.get('country')
    print(country_id)
    states = State.objects.filter(country_id=country_id).order_by('state_name')
    print([s for s in states])
    return render(request, 'StateList.html', {'states': states})

def load_cities(request):
    state_id = request.GET.get('state')
    print(state_id)
    cities = City.objects.filter(state_id=state_id).order_by('city_name')
    print([city for city in cities])
    return render(request, 'CityList.html', {'cities': cities})