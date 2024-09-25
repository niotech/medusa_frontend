from django.contrib import admin
from .models import SiteSettings, Page, Contact, FooterNav


class SiteSettingsAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['xmr_fixed_address']
        return []

    list_display = ('website_title', 'xmr_fixed_address', 'updated_at')

    fieldsets = [
        (
            'Site Wide Config',
            {
                'fields': ['website_title', 'logo', 'currency_code', 'currency_symbol']
            },
        ),
        (
            'Header',
            {
                'fields': ['banner', 'banner_headline', 'banner_subheading', 'banner_button_text', 'banner_button_url']
            },
        ),
        (
            'Landing Page',
            {
                'fields': [
                    'display_sale_text_lines', 
                    'sale_text_line_1', 
                    'sale_text_line_1_url', 
                    'sale_text_line_2', 
                    'sale_text_line_2_url',
                    'left_collection_title',
                    'left_collection_sub_title',
                    'left_collection_image',
                    'left_collection_url',
                    'right_collection_title',
                    'right_collection_sub_title',
                    'right_collection_image',
                    'right_collection_url',
                ]
            },
        ),
        (
            'Contact Info',
            {
                'fields': ['display_contact_info', 'contact_address', 'contact_phone', 'contact_email']
            },
        ),
        (
            'Social Profiles',
            {
                'fields': ['display_social_links', 'instagram', 'facebook']
            },
        ),
        (
            'Custom Page Content',
            {
                'fields': ['loyalty_progam_overview_content']
            },
        ),
        (
            'Other',
            {
                'fields': ['xmr_fixed_address']
            },
        ),
    ]

admin.site.register(SiteSettings, SiteSettingsAdmin)


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    prepopulated_fields = {'slug': ('title',)}  # Automatically generate slug from title
    search_fields = ('title',)  # Enable search by title
    ordering = ('title',)  # Default ordering by title


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
    search_fields = ('name', 'email')  # Enable search by name or email
    ordering = ('submitted_at',)  # Default ordering by submission date


class FooterNavAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_url', 'display_order')
    ordering = ('display_order',)
    list_editable = ['display_order']



# Register the models with the admin site
admin.site.register(Page, PageAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(FooterNav, FooterNavAdmin)
