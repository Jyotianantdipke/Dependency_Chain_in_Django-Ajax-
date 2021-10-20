

# Dependency Chain using Ajax in Django

Here we are going to discuss how we can implement A DependencyChain using Ajax in Django, but for this we need to have a little bit knowledge of Ajax and JQuery.

AJAX stands for Asynchronous JavaScript And XML, which allows web pages to update asynchronously by exchanging data to and from the server. 
This means you can update parts of a web page without reloading the complete web page. It involves a combination of a browser built-in XMLHttpRequest object, 
JavaScript, and HTML DOM

jQuery is one of the most popular libraries of JavaScript. Many advanced frameworks like Angular JS, React, etc are based on jQuery. It is a very useful library providing functions with DOM of web pages. To use bootstrap’s JavaScript part, jQuery is essential.

Here We have done with introduction of AJAX and JQuery, now move towadrs the actual implementation of Dependency Chain



## Implementation


As the name Suggests Dependency chain works on previously selected field or output,

For ex:-

We have to create address of a person, for this we are using country,state, and city 
when user selects the country, accordingly State list will shown in dropdown list and after that according to that state, City list will be shown to user,


Perform the following operations step by step for implementing Dependency Chain


  
## models.py:

1. Country
2. State(one-to-many relation with Country)
3. City(one-to-many relation with city)
4. Person(one-to-many relation with Country,State,City)

```bash

from django.db import models


class Country(models.Model):
    country_name = models.CharField(max_length=32)

    def __str__(self):
        return self.country_name


class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state_name = models.CharField(max_length=32)

    def __str__(self):
        return self.state_name


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=32)

    def __str__(self):
        return self.city_name


class Person(models.Model):
    name=models.CharField(max_length=32)
    country=models.ForeignKey(Country,on_delete=models.CASCADE)
    state=models.ForeignKey(State,on_delete=models.CASCADE)
    city=models.ForeignKey(City,on_delete=models.CASCADE)
```



## forms.py:

Create ModelForm of Person Model and override the __init__ method in forms.py for avoiding the dropdown of State and city untill and unless the higher level field is not Selected ,
do this as per i have implemented in forms.py

```bash

from django import forms
from .models import State,City,Country,Person

class PersonForm(forms.ModelForm):
    class Meta:
        model=Person
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].queryset = State.objects.none()
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = State.objects.filter(country_id=country_id).order_by('state_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['state'].queryset = self.instance.country.State_set.order_by('country_name')

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('city_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.state.city_set.order_by('state_name')

    
        

```


## views.py:

Now, in views.py create basic views for performing CRUD for that Person Model. 
Additionally, you have to create two views , one for loading states as per selected country and one for loading cities as per selected State,

```bash
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

```

## urls.py:

create all the urls for the views you have created in views.py.
Dont forget to create url for load states and load cities
  
```bash
urlpatterns=[

    path('ajax/load-states/', load_states, name='ajax_load_states'),
    path('ajax/load-cities/', load_cities, name='ajax_load_cities'),

]
``` 


## Create HTML Pages for State And City:

StateList.html

```bash
<option value="">Select State</option>
{% for state in states %}
<option value="{{ state.pk }}">{{ state.state_name }}</option>
{% endfor %}
```


CityList.html

```bash
<option value="">Select City</option>
{% for city in cities %}
<option value="{{ city.pk }}">{{ city.city_name }}</option>
{% endfor %}
```


## Creating templates – ‘PersonForm.html’

Here's the point at which we have to deal with AJAX request.
I'm using JQuery to create Asynchronous request,

```bash

<html>
  <head>
    <!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  </head>
  <body>
  <h2>Person Form</h2>

  <form method="post" id="personForm" data-state-url="{% url 'ajax_load_states' %}" data-cities-url="{% url 'ajax_load_cities' %}" >
    {% csrf_token %}
    <table>
      {{ form}}
    </table>
    <button type="submit">Save</button>
  </form> 
  <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
  <script>
    $("#id_country").change(function () {
      var url = $("#personForm").attr("data-state-url");  // get the url of the `load_states` view
      var countryId = $(this).val();  // get the selected country ID from the HTML input
      console.log(countryId)
      console.log(url)
      $.ajax({                       // initialize an AJAX request
        url: url, // set the url of the request (= localhost:8000/hr/ajax/load-states/)
        data: {
          'country': countryId       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_states` view function
          $("#id_state").html(data);  // replace the contents of the state input with the data that came from the server
        console.log(data);
        }
      });
    });
    console.log('success');
    $("#id_state").change(function () {
      var url = $("#personForm").attr("data-cities-url");  // get the url of the `load_cities` view
      var stateId = $(this).val();  // get the selected state ID from the HTML input
      console.log(url);
      $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
        data: {
          'state': stateId       // add the state id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
          $("#id_city").html(data); 
          console.log(data); // replace the contents of the city input with the data that came from the server
        }
      });
    });
  </script>
</body>
</html>

```


## Contributing

Here We have done with implementation of Dependency Chain using Ajax,

Please feel free to fix bugs, improve things, Just send a pull request, Thanks!!!

