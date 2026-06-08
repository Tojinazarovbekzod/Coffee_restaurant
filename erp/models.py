from django.db import models


class Mahsulot(models.Model):
    nom = models.CharField(max_length=200)
    miqdor = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    birlik = models.CharField(max_length=20, default='dona')
    minimal_miqdor = models.DecimalField(max_digits=10, decimal_places=2, default=5)
    narx = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'
        ordering = ['nom']

    def __str__(self):
        return self.nom

    @property
    def kam_qolganmi(self):
        return self.miqdor <= self.minimal_miqdor


BUYURTMA_HOLATLARI = [
    ('yangi', 'Yangi'),
    ('jarayonda', 'Jarayonda'),
    ('bajarildi', 'Bajarildi'),
    ('bekor', 'Bekor qilindi'),
]


class Buyurtma(models.Model):
    mijoz_ism = models.CharField(max_length=200)
    sana = models.DateTimeField(auto_now_add=True)
    holat = models.CharField(max_length=20, choices=BUYURTMA_HOLATLARI, default='yangi')
    izoh = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'
        ordering = ['-sana']

    def __str__(self):
        return f"Buyurtma #{self.pk} - {self.mijoz_ism}"

    @property
    def jami_summa(self):
        return sum(q.jami for q in self.qatorlar.all())


class BuyurtmaQatori(models.Model):
    buyurtma = models.ForeignKey(Buyurtma, on_delete=models.CASCADE, related_name='qatorlar')
    mahsulot_nomi = models.CharField(max_length=200)
    miqdor = models.PositiveIntegerField(default=1)
    narx = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def jami(self):
        return self.miqdor * self.narx


XODIM_LAVOZIMLARI = [
    ('ombor_mudiri', 'Ombor mudiri'),
    ('omborchi', 'Omborchi'),
    ('savdo_vakili', 'Savdo vakili'),
    ('logist', 'Logist'),
    ('buxgalter', 'Buxgalter'),
    ('haydovchi', 'Haydovchi'),
]


class Xodim(models.Model):
    ism = models.CharField(max_length=100)
    familiya = models.CharField(max_length=100)
    lavozim = models.CharField(max_length=20, choices=XODIM_LAVOZIMLARI)
    telefon = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    maosh = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ishga_kirgan = models.DateField(auto_now_add=True)
    faolmi = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Xodim'
        verbose_name_plural = 'Xodimlar'
        ordering = ['familiya', 'ism']

    def __str__(self):
        return f"{self.ism} {self.familiya} ({self.get_lavozim_display()})"


MOLIYA_TURLARI = [
    ('daromad', 'Daromad'),
    ('xarajat', 'Xarajat'),
]


class MoliyaviyYozuv(models.Model):
    tur = models.CharField(max_length=20, choices=MOLIYA_TURLARI)
    summa = models.DecimalField(max_digits=12, decimal_places=2)
    sana = models.DateField(auto_now_add=True)
    tavsif = models.CharField(max_length=300)

    class Meta:
        verbose_name = 'Moliyaviy yozuv'
        verbose_name_plural = 'Moliyaviy yozuvlar'
        ordering = ['-sana']

    def __str__(self):
        return f"{self.get_tur_display()}: {self.summa} so'm ({self.sana})"
