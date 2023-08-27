from django import forms
from .models import Dog, Parent


class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = '__all__'


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = '__all__'