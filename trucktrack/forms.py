from .models import Orders
from django.forms import ModelForm, TextInput,Textarea,NumberInput
from django import forms

class OrdersForm(ModelForm):
    class Meta:
        model = Orders
        fields = ['title','text','bid','tonnage']
        widgets = {
            'title': TextInput(attrs={"class": "form-control", "placeholder":"Write your title"}),
            'text': Textarea(attrs={"class": "form-control","placeholder":"Write your text"}),
            'bid':NumberInput(attrs={"class":"form-control","placeholder":"Write your price"}),
            'tonnage':NumberInput(attrs={"class":"form-control","placeholder":"Write your tonnage"}),
        }
        labels ={
            "title":"",
            "text":"",
            "bid":"",
            "tonnage":""
        }

