from django.db import models


class Mijoz(models.Model):
    ism = models.CharField(max_length=100)
    familiya = models.CharField(max_length=100)
    telefon = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    tugilgan_kun = models.DateField(null=True, blank=True)
    manzil = models.TextField(blank=True)
    izoh = models.TextField(blank=True)
    qoshilgan_sana = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Mijoz'
        verbose_name_plural = 'Mijozlar'
        ordering = ['-qoshilgan_sana']

    def __str__(self):
        return f"{self.ism} {self.familiya}"

    @property
    def tashriflar_soni(self):
        return self.muloqotlar.filter(tur='tashrif').count()


MULOQOT_TURLARI = [
    ('tashrif', 'Tashrif'),
    ('qongiroq', "Qo'ng'iroq"),
    ('email', 'Email'),
    ('izoh', 'Izoh'),
]


class Muloqot(models.Model):
    mijoz = models.ForeignKey(Mijoz, on_delete=models.CASCADE, related_name='muloqotlar')
    tur = models.CharField(max_length=20, choices=MULOQOT_TURLARI, default='izoh')
    sana = models.DateTimeField(auto_now_add=True)
    izoh = models.TextField()

    class Meta:
        verbose_name = 'Muloqot'
        verbose_name_plural = 'Muloqotlar'
        ordering = ['-sana']

    def __str__(self):
        return f"{self.mijoz} - {self.get_tur_display()}"
