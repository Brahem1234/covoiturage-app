from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'payer', 'recipient', 'amount', 
                    'payment_method', 'status', 'payment_date')
    list_filter = ('status', 'payment_method', 'payment_date')
    search_fields = ('payer__username', 'payer__email', 'recipient__username', 
                     'transaction_id', 'booking__id')
    date_hierarchy = 'payment_date'
    ordering = ('-payment_date',)
    
    fieldsets = (
        ('Informations de paiement', {
            'fields': ('booking', 'payer', 'recipient', 'amount')
        }),
        ('Méthode et statut', {
            'fields': ('payment_method', 'status', 'transaction_id')
        }),
        ('Dates', {
            'fields': ('payment_date', 'completed_date')
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('payment_date',)
    
    actions = ['mark_as_completed', 'mark_as_failed', 'refund_payment']
    
    def mark_as_completed(self, request, queryset):
        for payment in queryset:
            payment.mark_as_completed()
        self.message_user(request, f"{queryset.count()} paiement(s) marqué(s) comme complété(s).")
    mark_as_completed.short_description = "Marquer comme complété"
    
    def mark_as_failed(self, request, queryset):
        for payment in queryset:
            payment.mark_as_failed()
        self.message_user(request, f"{queryset.count()} paiement(s) marqué(s) comme échoué(s).")
    mark_as_failed.short_description = "Marquer comme échoué"
    
    def refund_payment(self, request, queryset):
        for payment in queryset:
            payment.refund()
        self.message_user(request, f"{queryset.count()} paiement(s) remboursé(s).")
    refund_payment.short_description = "Rembourser"
