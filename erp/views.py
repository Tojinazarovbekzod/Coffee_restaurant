from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, F
from .models import Mahsulot, Buyurtma, Xodim, MoliyaviyYozuv, BUYURTMA_HOLATLARI
from .forms import MahsulotForm, BuyurtmaForm, XodimForm, MoliyaviyYozuvForm


def erp_dashboard(request):
    daromad = MoliyaviyYozuv.objects.filter(tur='daromad').aggregate(jami=Sum('summa'))['jami'] or 0
    xarajat = MoliyaviyYozuv.objects.filter(tur='xarajat').aggregate(jami=Sum('summa'))['jami'] or 0
    context = {
        'jami_mahsulotlar': Mahsulot.objects.count(),
        'kam_qolgan': Mahsulot.objects.filter(miqdor__lte=F('minimal_miqdor')),
        'jami_buyurtmalar': Buyurtma.objects.count(),
        'yangi_buyurtmalar': Buyurtma.objects.filter(holat='yangi').count(),
        'jami_xodimlar': Xodim.objects.filter(faolmi=True).count(),
        'daromad': daromad,
        'xarajat': xarajat,
        'foyda': daromad - xarajat,
        'oxirgi_buyurtmalar': Buyurtma.objects.order_by('-sana')[:5],
    }
    return render(request, 'erp/dashboard.html', context)


# --- Mahsulotlar ---

def mahsulotlar(request):
    barcha = Mahsulot.objects.all()
    return render(request, 'erp/mahsulotlar.html', {
        'mahsulotlar': barcha,
        'kam_qolgan_soni': barcha.filter(miqdor__lte=F('minimal_miqdor')).count(),
    })


def mahsulot_yaratish(request):
    if request.method == 'POST':
        form = MahsulotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('erp:mahsulotlar')
    else:
        form = MahsulotForm()
    return render(request, 'erp/mahsulot_form.html', {'form': form, 'sarlavha': 'Yangi mahsulot'})


def mahsulot_tahrirlash(request, pk):
    mahsulot = get_object_or_404(Mahsulot, pk=pk)
    if request.method == 'POST':
        form = MahsulotForm(request.POST, instance=mahsulot)
        if form.is_valid():
            form.save()
            return redirect('erp:mahsulotlar')
    else:
        form = MahsulotForm(instance=mahsulot)
    return render(request, 'erp/mahsulot_form.html', {'form': form, 'sarlavha': 'Mahsulotni tahrirlash'})


def mahsulot_ochirish(request, pk):
    mahsulot = get_object_or_404(Mahsulot, pk=pk)
    if request.method == 'POST':
        mahsulot.delete()
        return redirect('erp:mahsulotlar')
    return render(request, 'erp/tasdiqlash.html', {'obyekt': mahsulot, 'tur': 'mahsulot'})


# --- Buyurtmalar ---

def buyurtmalar(request):
    holat = request.GET.get('holat', '')
    barcha = Buyurtma.objects.all()
    if holat:
        barcha = barcha.filter(holat=holat)
    return render(request, 'erp/buyurtmalar.html', {
        'buyurtmalar': barcha,
        'holat': holat,
        'holat_turlari': BUYURTMA_HOLATLARI,
    })


def buyurtma_detail(request, pk):
    buyurtma = get_object_or_404(Buyurtma, pk=pk)
    return render(request, 'erp/buyurtma_detail.html', {
        'buyurtma': buyurtma,
        'holat_turlari': BUYURTMA_HOLATLARI,
    })


def buyurtma_yaratish(request):
    if request.method == 'POST':
        form = BuyurtmaForm(request.POST)
        if form.is_valid():
            buyurtma = form.save()
            return redirect('erp:buyurtma_detail', pk=buyurtma.pk)
    else:
        form = BuyurtmaForm()
    return render(request, 'erp/buyurtma_form.html', {'form': form})


def buyurtma_holat(request, pk):
    buyurtma = get_object_or_404(Buyurtma, pk=pk)
    if request.method == 'POST':
        yangi_holat = request.POST.get('holat')
        holat_qiymatlari = [h[0] for h in BUYURTMA_HOLATLARI]
        if yangi_holat in holat_qiymatlari:
            buyurtma.holat = yangi_holat
            buyurtma.save()
    return redirect('erp:buyurtma_detail', pk=pk)


# --- Xodimlar ---

def xodimlar(request):
    barcha = Xodim.objects.filter(faolmi=True)
    return render(request, 'erp/xodimlar.html', {'xodimlar': barcha})


def xodim_yaratish(request):
    if request.method == 'POST':
        form = XodimForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('erp:xodimlar')
    else:
        form = XodimForm()
    return render(request, 'erp/xodim_form.html', {'form': form, 'sarlavha': 'Yangi xodim'})


def xodim_tahrirlash(request, pk):
    xodim = get_object_or_404(Xodim, pk=pk)
    if request.method == 'POST':
        form = XodimForm(request.POST, instance=xodim)
        if form.is_valid():
            form.save()
            return redirect('erp:xodimlar')
    else:
        form = XodimForm(instance=xodim)
    return render(request, 'erp/xodim_form.html', {'form': form, 'sarlavha': 'Xodimni tahrirlash'})


# --- Moliya ---

def moliya(request):
    yozuvlar = MoliyaviyYozuv.objects.all()
    daromad = yozuvlar.filter(tur='daromad').aggregate(jami=Sum('summa'))['jami'] or 0
    xarajat = yozuvlar.filter(tur='xarajat').aggregate(jami=Sum('summa'))['jami'] or 0
    return render(request, 'erp/moliya.html', {
        'yozuvlar': yozuvlar,
        'daromad': daromad,
        'xarajat': xarajat,
        'foyda': daromad - xarajat,
    })


def moliya_qoshish(request):
    if request.method == 'POST':
        form = MoliyaviyYozuvForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('erp:moliya')
    else:
        form = MoliyaviyYozuvForm()
    return render(request, 'erp/moliya_form.html', {'form': form})
