from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator

class Post(models.Model):
    # Choices
    CATEGORY_CHOICES = [
        ("general", "General"),
        ("news", "News"),
        ("tech", "Tech"),
        ("sport", "Sport"),
    ]

    title = models.CharField(max_length=2048, validators=[MinLengthValidator(3)])
    content = models.TextField(validators=[MinLengthValidator(10)])
    image = models.ImageField(upload_to='posts_images/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="general")
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
