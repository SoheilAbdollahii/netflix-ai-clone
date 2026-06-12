from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)  # ژانرها را با کاما جدا می‌کنیم، مثل: Action, Sci-Fi
    year = models.IntegerField()
    director = models.CharField(max_length=255, blank=True, null=True)
    cast = models.TextField(blank=True, null=True)  # لیست بازیگران
    plot = models.TextField()  # خلاصه داستان (مهم‌ترین فیلد برای هوش مصنوعی)
    poster_url = models.URLField(max_length=500, blank=True, null=True)  # لینک عکس فیلم برای فرانت
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.title} ({self.year})"