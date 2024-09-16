from django.db import models


class SiteSettings(models.Model):
    # site wide config
    website_title = models.CharField(max_length=100, blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    currency_code = models.CharField(default='usd', max_length=5, help_text="need to match currecy_code found in query result of product->variant->prices")
    currency_symbol = models.CharField(default='$', max_length=5)

    # header
    banner = models.ImageField(upload_to='banners/', blank=True, null=True)
    banner_headline = models.CharField(max_length=255, blank=True, null=True)
    banner_subheading = models.CharField(max_length=255, blank=True, null=True)
    banner_button_text = models.CharField(max_length=50, blank=True, null=True)
    banner_button_url = models.URLField(blank=True, null=True)
    
    
    # landing page
    display_sale_text_lines = models.BooleanField(default=False)
    sale_text_line_1 = models.CharField(max_length=100, blank=True, null=True)
    sale_text_line_1_url = models.URLField(max_length=200, blank=True, null=True)
    sale_text_line_2 = models.CharField(max_length=100, blank=True, null=True)
    sale_text_line_2_url = models.URLField(max_length=200, blank=True, null=True)
    
    left_collection_title = models.CharField(max_length=50, blank=True, null=True)
    left_collection_sub_title = models.CharField(max_length=50, blank=True, null=True)
    left_collection_image = models.ImageField(upload_to='collections/', blank=True, null=True)
    left_collection_url = models.URLField(blank=True, null=True)

    right_collection_title = models.CharField(max_length=50, blank=True, null=True)
    right_collection_sub_title = models.CharField(max_length=50, blank=True, null=True)
    right_collection_image = models.ImageField(upload_to='collections/', blank=True, null=True)
    right_collection_url = models.URLField(blank=True, null=True)

    # contact information
    display_contact_info = models.BooleanField(default=True)
    contact_address = models.CharField(max_length=200, blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    contact_email = models.EmailField(max_length=254, blank=True, null=True)

    # social profiles
    display_social_links = models.BooleanField(default=True)
    instagram = models.URLField(max_length=200, blank=True, null=True)
    facebook = models.URLField(max_length=200, blank=True, null=True)

    # other
    xmr_fixed_address = models.CharField(max_length=100, blank=True, null=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"


class Page(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, help_text="Unique URL for this page")
    content = models.TextField()

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"
