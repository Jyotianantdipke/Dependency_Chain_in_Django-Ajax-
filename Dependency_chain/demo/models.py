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