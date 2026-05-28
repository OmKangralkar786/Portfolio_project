from django.contrib import admin
from .models import Portfolio
from .models import Feedback  # Import the Feedback model
from .models import Company

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user')  # Show name and user in admin panel
    search_fields = ('full_name', 'user__username')  # Enable search by name or username

# Register Feedback model
admin.site.register(Feedback)


admin.site.register(Company)