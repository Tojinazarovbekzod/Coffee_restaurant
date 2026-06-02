from django import forms
from .models import Mijoz, Muloqot


class MijozForm(forms.ModelForm):
    class Meta:
        model = Mijoz
        fields = ['ism', 'familiya', 'telefon', 'email', 'tugilgan_kun', 'manzil', 'izoh']
        widgets = {
            'ism': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ism'}),
            'familiya': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Familiya'}),
            'telefon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998 90 123 45 67'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.com'}),
            'tugilgan_kun': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'manzil': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'izoh': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'ism': 'Ism',
            'familiya': 'Familiya',
            'telefon': 'Telefon',
            'email': 'Email',
            'tugilgan_kun': "Tug'ilgan kun",
            'manzil': 'Manzil',
            'izoh': 'Izoh',
        }


class MuloqotForm(forms.ModelForm):
    class Meta:
        model = Muloqot
        fields = ['tur', 'izoh']
        widgets = {
            'tur': forms.Select(attrs={'class': 'form-select'}),
            'izoh': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Muloqot haqida...'}),
        }
        labels = {
            'tur': 'Muloqot turi',
            'izoh': 'Izoh',
        }
