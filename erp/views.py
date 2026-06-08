import json
from datetime import datetime, time
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Sum, F
from django.utils import timezone
from .models import Mahsulot, Buyurtma, BuyurtmaQatori, Xodim, MoliyaviyYozuv, BUYURTMA_HOLATLARI
from crm.models import Mijoz, Muloqot
from .forms import MahsulotForm, BuyurtmaForm, XodimForm, MoliyaviyYozuvForm

OY_QISQA_NOMLARI = ['Yan', 'Fev', 'Mar', 'Apr', 'May', 'Iyun', 'Iyul', 'Avg', 'Sen', 'Okt', 'Noy', 'Dek']

HOLAT_RANGLARI = {
    'yangi': '#3b82f6',
    'jarayonda': '#f59e0b',
    'bajarildi': '#22c55e',
    'bekor': '#ef4444',
}


def _oxirgi_oylar_daromadi(oylar_soni=6):
    bugun = timezone.now().date()
    natija = []
    yil, oy = bugun.year, bugun.month
    for _ in range(oylar_soni):
        summa = MoliyaviyYozuv.objects.filter(
            tur='daromad', sana__year=yil, sana__month=oy
        ).aggregate(jami=Sum('summa'))['jami'] or 0
        natija.append({'oy': OY_QISQA_NOMLARI[oy - 1], 'summa': float(summa)})
        oy -= 1
        if oy == 0:
            oy = 12
            yil -= 1
    natija.reverse()
    return natija


def _faollik_tarixi(limit=6):
    yozuvlar = []
    for b in Buyurtma.objects.order_by('-sana')[:5]:
        yozuvlar.append({'matn': f"Yangi buyurtma qabul qilindi: #{b.pk} — {b.mijoz_ism}", 'vaqt': b.sana, 'ikon': 'fa-file-invoice'})
    for m in Mijoz.objects.order_by('-qoshilgan_sana')[:5]:
        yozuvlar.append({'matn': f"Yangi mijoz qo'shildi: {m}", 'vaqt': m.qoshilgan_sana, 'ikon': 'fa-user-plus'})
    for mu in Muloqot.objects.select_related('mijoz').order_by('-sana')[:5]:
        yozuvlar.append({'matn': f"{mu.mijoz} bilan {mu.get_tur_display().lower()} qayd etildi", 'vaqt': mu.sana, 'ikon': 'fa-comments'})
    for y in MoliyaviyYozuv.objects.order_by('-sana')[:5]:
        vaqt = timezone.make_aware(datetime.combine(y.sana, time.min))
        yozuvlar.append({'matn': f"{y.get_tur_display()} qayd etildi: {y.tavsif}", 'vaqt': vaqt, 'ikon': 'fa-wallet'})
    yozuvlar.sort(key=lambda x: x['vaqt'], reverse=True)
    return yozuvlar[:limit]


def _top_mijozlar(limit=5):
    qs = (
        BuyurtmaQatori.objects
        .values(mijoz=F('buyurtma__mijoz_ism'))
        .annotate(jami=Sum(F('miqdor') * F('narx')))
        .order_by('-jami')[:limit]
    )
    natija = list(qs)
    eng_katta = natija[0]['jami'] if natija else 0
    for item in natija:
        item['jami'] = float(item['jami'])
        item['foiz'] = round(item['jami'] / float(eng_katta) * 100) if eng_katta else 0
    return natija


@login_required(login_url='/login/')
@require_POST
def buyurtma_qabul(request):
    try:
        cart = json.loads(request.POST.get('cart', '[]'))
    except (json.JSONDecodeError, ValueError):
        cart = []

    if not cart:
        messages.error(request, "Savat bo'sh — avval mahsulot tanlang.")
        return redirect('menu')

    mijoz_ism = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
    buyurtma = Buyurtma.objects.create(mijoz_ism=mijoz_ism, holat='yangi')

    for item in cart:
        try:
            BuyurtmaQatori.objects.create(
                buyurtma=buyurtma,
                mahsulot_nomi=item['name'],
                miqdor=int(item.get('qty', 1)),
                narx=float(item['price']),
            )
        except (KeyError, ValueError):
            continue

    messages.success(request, f"Buyurtma #{buyurtma.pk} muvaffaqiyatli qabul qilindi!")
    return redirect('menu')


@login_required
def erp_dashboard(request):
    daromad = MoliyaviyYozuv.objects.filter(tur='daromad').aggregate(jami=Sum('summa'))['jami'] or 0
    xarajat = MoliyaviyYozuv.objects.filter(tur='xarajat').aggregate(jami=Sum('summa'))['jami'] or 0

    barcha_buyurtmalar = Buyurtma.objects.all()
    jami_buyurtmalar = barcha_buyurtmalar.count()
    yetkazilgan_soni = barcha_buyurtmalar.filter(holat='bajarildi').count()
    kutilayotgan_soni = barcha_buyurtmalar.filter(holat__in=['yangi', 'jarayonda']).count()

    summalar = [float(b.jami_summa) for b in barcha_buyurtmalar]
    ortacha_chek = sum(summalar) / len(summalar) if summalar else 0

    holat_taqsimoti = []
    for kod, nom in BUYURTMA_HOLATLARI:
        soni = barcha_buyurtmalar.filter(holat=kod).count()
        foiz = round(soni / jami_buyurtmalar * 100) if jami_buyurtmalar else 0
        holat_taqsimoti.append({'kod': kod, 'nom': nom, 'soni': soni, 'foiz': foiz, 'rang': HOLAT_RANGLARI[kod]})

    oylik_daromad = _oxirgi_oylar_daromadi()

    context = {
        'jami_mahsulotlar': Mahsulot.objects.count(),
        'kam_qolgan': Mahsulot.objects.filter(miqdor__lte=F('minimal_miqdor')),
        'jami_buyurtmalar': jami_buyurtmalar,
        'yangi_buyurtmalar': Buyurtma.objects.filter(holat='yangi').count(),
        'yetkazilgan_soni': yetkazilgan_soni,
        'kutilayotgan_soni': kutilayotgan_soni,
        'ortacha_chek': ortacha_chek,
        'jami_mijozlar': Mijoz.objects.count(),
        'jami_xodimlar': Xodim.objects.filter(faolmi=True).count(),
        'daromad': daromad,
        'xarajat': xarajat,
        'foyda': daromad - xarajat,
        'oxirgi_buyurtmalar': barcha_buyurtmalar.order_by('-sana')[:5],
        'top_mijozlar': _top_mijozlar(),
        'faollik_tarixi': _faollik_tarixi(),
        'holat_taqsimoti': holat_taqsimoti,
        'oylik_daromad': oylik_daromad,
    }
    return render(request, 'erp/dashboard.html', context)


# --- Mahsulotlar ---

@login_required
def mahsulotlar(request):
    barcha = Mahsulot.objects.all()
    return render(request, 'erp/mahsulotlar.html', {
        'mahsulotlar': barcha,
        'kam_qolgan_soni': barcha.filter(miqdor__lte=F('minimal_miqdor')).count(),
    })


@login_required
def mahsulot_yaratish(request):
    if request.method == 'POST':
        form = MahsulotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('erp:mahsulotlar')
    else:
        form = MahsulotForm()
    return render(request, 'erp/mahsulot_form.html', {'form': form, 'sarlavha': 'Yangi mahsulot'})


@login_required
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


@login_required
def mahsulot_ochirish(request, pk):
    mahsulot = get_object_or_404(Mahsulot, pk=pk)
    if request.method == 'POST':
        mahsulot.delete()
        return redirect('erp:mahsulotlar')
    return render(request, 'erp/tasdiqlash.html', {'obyekt': mahsulot, 'tur': 'mahsulot'})


# --- Buyurtmalar ---

@login_required
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


@login_required
def buyurtma_detail(request, pk):
    buyurtma = get_object_or_404(Buyurtma, pk=pk)
    return render(request, 'erp/buyurtma_detail.html', {
        'buyurtma': buyurtma,
        'holat_turlari': BUYURTMA_HOLATLARI,
    })


@login_required
def buyurtma_yaratish(request):
    if request.method == 'POST':
        form = BuyurtmaForm(request.POST)
        if form.is_valid():
            buyurtma = form.save()
            return redirect('erp:buyurtma_detail', pk=buyurtma.pk)
    else:
        form = BuyurtmaForm()
    return render(request, 'erp/buyurtma_form.html', {'form': form})


@login_required
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

@login_required
def xodimlar(request):
    barcha = Xodim.objects.filter(faolmi=True)
    return render(request, 'erp/xodimlar.html', {'xodimlar': barcha})


@login_required
def xodim_yaratish(request):
    if request.method == 'POST':
        form = XodimForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('erp:xodimlar')
    else:
        form = XodimForm()
    return render(request, 'erp/xodim_form.html', {'form': form, 'sarlavha': 'Yangi xodim'})


@login_required
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

@login_required
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


@login_required
def moliya_qoshish(request):
    if request.method == 'POST':
        form = MoliyaviyYozuvForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('erp:moliya')
    else:
        form = MoliyaviyYozuvForm()
    return render(request, 'erp/moliya_form.html', {'form': form})
