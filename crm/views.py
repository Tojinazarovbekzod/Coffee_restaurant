from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Mijoz, Muloqot
from .forms import MijozForm, MuloqotForm


def crm_dashboard(request):
    context = {
        'jami_mijozlar': Mijoz.objects.count(),
        'yangi_mijozlar': Mijoz.objects.order_by('-qoshilgan_sana')[:5],
        'oxirgi_muloqotlar': Muloqot.objects.select_related('mijoz').order_by('-sana')[:10],
        'jami_muloqotlar': Muloqot.objects.count(),
    }
    return render(request, 'crm/dashboard.html', context)


def mijozlar_royxati(request):
    qidiruv = request.GET.get('q', '')
    mijozlar = Mijoz.objects.all()
    if qidiruv:
        mijozlar = mijozlar.filter(
            Q(ism__icontains=qidiruv) |
            Q(familiya__icontains=qidiruv) |
            Q(telefon__icontains=qidiruv) |
            Q(email__icontains=qidiruv)
        )
    return render(request, 'crm/mijozlar.html', {'mijozlar': mijozlar, 'qidiruv': qidiruv})


def mijoz_detail(request, pk):
    mijoz = get_object_or_404(Mijoz, pk=pk)
    muloqotlar = mijoz.muloqotlar.all()
    muloqot_form = MuloqotForm()
    return render(request, 'crm/mijoz_detail.html', {
        'mijoz': mijoz,
        'muloqotlar': muloqotlar,
        'muloqot_form': muloqot_form,
    })


def mijoz_yaratish(request):
    if request.method == 'POST':
        form = MijozForm(request.POST)
        if form.is_valid():
            mijoz = form.save()
            return redirect('crm:mijoz_detail', pk=mijoz.pk)
    else:
        form = MijozForm()
    return render(request, 'crm/mijoz_form.html', {'form': form, 'sarlavha': "Yangi mijoz qo'shish"})


def mijoz_tahrirlash(request, pk):
    mijoz = get_object_or_404(Mijoz, pk=pk)
    if request.method == 'POST':
        form = MijozForm(request.POST, instance=mijoz)
        if form.is_valid():
            form.save()
            return redirect('crm:mijoz_detail', pk=mijoz.pk)
    else:
        form = MijozForm(instance=mijoz)
    return render(request, 'crm/mijoz_form.html', {'form': form, 'sarlavha': 'Mijozni tahrirlash', 'mijoz': mijoz})


def mijoz_ochirish(request, pk):
    mijoz = get_object_or_404(Mijoz, pk=pk)
    if request.method == 'POST':
        mijoz.delete()
        return redirect('crm:mijozlar')
    return render(request, 'crm/tasdiqlash.html', {'obyekt': mijoz, 'tur': 'mijoz'})


def muloqot_qoshish(request, mijoz_pk):
    mijoz = get_object_or_404(Mijoz, pk=mijoz_pk)
    if request.method == 'POST':
        form = MuloqotForm(request.POST)
        if form.is_valid():
            muloqot = form.save(commit=False)
            muloqot.mijoz = mijoz
            muloqot.save()
    return redirect('crm:mijoz_detail', pk=mijoz_pk)
