from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator

# --- Metro Line Management ---

class MetroLine(models.Model):
    """Represents a single metro line (e.g., 'Blue Line')."""
    name = models.CharField(max_length=100, unique=True)
    is_purchasing_enabled = models.BooleanField(
        default=True,
        help_text="Controls the ability for passengers to buy new tickets on this line."
    )

    def __str__(self):
        return self.name

class Station(models.Model):
    """Represents a single metro station."""
    line = models.ForeignKey(MetroLine, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    # order_on_line is crucial for dynamic price calculation (distance).
    order_on_line = models.IntegerField(
        validators=[MinValueValidator(1)],
    )
    is_operational = models.BooleanField(
        default=True,
        help_text="Controls if this station is open for service."
    )

    class Meta:
        ordering = ['line', 'order_on_line']
        unique_together = ('line', 'name') 

    def __str__(self):
        return f"{self.name} ({self.line.name})"

class DailyFootfall(models.Model):
    """Tracks daily entries and exits for monitoring."""
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    entries = models.IntegerField(default=0)
    exits = models.IntegerField(default=0)

    class Meta:
        unique_together = ('station', 'date')

    def __str__(self):
        return f"{self.station.name} - {self.date}"