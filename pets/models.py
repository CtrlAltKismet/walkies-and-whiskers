from django.conf import settings
from django.db import models


class Pet(models.Model):
    """Store a pet profile belonging to a registered user."""
    
    
    SIZE_SMALL = "small"
    SIZE_MEDIUM = "medium"
    SIZE_LARGE = "large"
    
    
    SIZE_CHOICES = [
        (SIZE_SMALL, "Small"),
        (SIZE_MEDIUM, "Medium"),
        (SIZE_LARGE, "Large"),
    ]
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pets",
    )
    name = models.CharField(
        max_length=100,
    )
    species = models.CharField(
        max_length=100,
    )
    breed = models.CharField(
        max_length=100,
        blank=True,
    )
    age = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )
    size = models.CharField(
        max_length=10,
        choices=SIZE_CHOICES,
    )
    temperament = models.TextField()
    medical_notes = models.TextField(
        blank=True,
    )
    feeding_notes = models.TextField(
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    
    class Meta:
        ordering = ["name"]
        
    def __str__(self):
        """Return the pet's name for admin and debugging displays."""
        return self.name