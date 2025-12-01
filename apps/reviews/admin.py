from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'recipient', 'trip', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('author__username', 'recipient__username', 'comment')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Informations de l\'avis', {
            'fields': ('author', 'recipient', 'trip')
        }),
        ('Évaluation', {
            'fields': ('rating', 'comment')
        }),
        ('Date', {
            'fields': ('created_at',)
        }),
    )
    
    readonly_fields = ('created_at',)
