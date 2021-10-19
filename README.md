

# Dependency Chain using Ajax in Django

Here we are going to discuss how we can implement A Dependency Chain using Ajax in Django, but for this we need to have a little bit knowledge of Ajax and JQuery.

AJAX stands for Asynchronous JavaScript And XML, which allows web pages to update asynchronously by exchanging data to and from the server. 
This means you can update parts of a web page without reloading the complete web page. It involves a combination of a browser built-in XMLHttpRequest object, 
JavaScript, and HTML DOM

jQuery is one of the most popular libraries of JavaScript. Many advanced frameworks like Angular JS, React, etc are based on jQuery. It is a very useful library providing functions with DOM of web pages. To use bootstrap’s JavaScript part, jQuery is essential.

Here We have done with introduction aof AJAX and JQuery, now move towadrs the actual implementation of Dependency Chain


## Implementation

As the name Suggests Dependency chain works on previously selected field or output,

For ex:-

We have to create address of a person, for this we are using country,state, and city 
when user selects the country, accordingly State list will shown in dropdown list and after that according to that state City list will be shown to user,


Perform the following operations step by step for implementing Dependency Chain


  
## models.py:

1. Country
2. State(one-to-many relation with Country)
3. City(one-to-many relation with city)
4. Person(one-to-many relation with Country,State,City)



## forms.py:

Create ModelForm of Person Model and override the __init__ method in forms.py for avoiding the dropdown of State and city untill and unless the higher level field is not Selected ,
do this as per i have implemented in forms.py



## views.py:

Now, in views.py create basic views for performing CRUD for that Person Model. 
Additionally, you have to create two views , one for loading states as per selected country and one for loading cities as per selected State,



## urls.py:

create all the urls for the views you have created in views.py.
Dont forget to create url for load states and load cities
  


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
I'm using JQuery to create Asynchronous request

