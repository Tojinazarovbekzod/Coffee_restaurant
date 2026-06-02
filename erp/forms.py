from django import forms
from .models import Mahsulot, Buyurtma, Xodim, MoliyaviyYozuv


class MahsulotForm(forms.ModelForm):
    class Meta:
        model = Mahsulot
        fields = ['nom', 'miqdor', 'birlik', 'minimal_miqdor', 'narx']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'miqdor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'birlik': forms.TextInput(attrs={'class': 'form-control'}),
            'minimal_miqdor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'narx': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        labels = {
            'nom': 'Nomi',
            'miqdor': 'Miqdori',
            'birlik': 'Birlik (kg, litr, dona...)',
            'minimal_miqdor': 'Minimal miqdor',
            'narx': "Narxi (so'm)",
        }


class BuyurtmaForm(forms.ModelForm):
    class Meta:
        model = Buyurtma
        fields = ['mijoz_ism', 'holat', 'izoh']
        widgets = {
            'mijoz_ism': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mijoz ismi'}),
            'holat': forms.Select(attrs={'class': 'form-select'}),
            'izoh': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'mijoz_ism': 'Mijoz ismi',
            'holat': 'Holat',
            'izoh': 'Izoh',
        }


class XodimForm(forms.ModelForm):
    class Meta:
        model = Xodim
        fields = ['ism', 'familiya', 'lavozim', 'telefon', 'email', 'maosh', 'faolmi']
        widgets = {
            'ism': forms.TextInput(attrs={'class': 'form-control'}),
            'familiya': forms.TextInput(attrs={'class': 'form-control'}),
            'lavozim': forms.Select(attrs={'class': 'form-select'}),
            'telefon': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'maosh': forms.NumberInput(attrs={'class': 'form-control', 'step': '1000'}),
            'faolmi': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'ism': 'Ism',
            'familiya': 'Familiya',
            'lavozim': 'Lavozim',
            'telefon': 'Telefon',
            'email': 'Email',
            'maosh': "Maosh (so'm)",
            'faolmi': 'Faol xodim',
        }


class MoliyaviyYozuvForm(forms.ModelForm):
    class Meta:
        model = MoliyaviyYozuv
        fields = ['tur', 'summa', 'tavsif']
        widgets = {
            'tur': forms.Select(attrs={'class': 'form-select'}),
            'summa': forms.NumberInput(attrs={'class': 'form-control', 'step': '1000'}),
            'tavsif': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tavsif...'}),
        }
        labels = {
            'tur': 'Tur',
            'summa': "Summa (so'm)",
            'tavsif': 'Tavsif',
        }
