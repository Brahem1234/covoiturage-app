from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_verified', 'verification_status', 'is_staff')
    list_filter = ('is_verified', 'verification_status', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    ordering = ('-date_joined',)
    
    actions = ['verify_users', 'reject_verification']

    def verify_users(self, request, queryset):
        queryset.update(is_verified=True, verification_status='verified')
        self.message_user(request, "Les utilisateurs sélectionnés ont été vérifiés.")
    verify_users.short_description = "Marquer comme VÉRIFIÉ"

    def reject_verification(self, request, queryset):
        queryset.update(is_verified=False, verification_status='rejected')
        self.message_user(request, "La vérification pour les utilisateurs sélectionnés a été rejetée.")
    reject_verification.short_description = "REJETER la vérification"

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('phone_number', 'bio', 'profile_picture', 'date_of_birth', 'gender')
        }),
        ('Vérification d\'identité', {
            'fields': ('identity_document', 'identity_type', 'verification_status', 'is_verified')
        }),
        ('Préférences Conducteur', {
            'fields': ('car_model', 'car_color', 'license_plate')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('email', 'phone_number', 'first_name', 'last_name')
        }),
    )
