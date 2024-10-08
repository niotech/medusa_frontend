from django.db import models
from django.urls import reverse
from tinymce import models as tinymce_models


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

    # custom page content
    loyalty_progam_overview_content = models.ForeignKey('Page', on_delete=models.CASCADE, blank=True, null=True)

    # other
    xmr_fixed_address = models.CharField(max_length=100, blank=True, null=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"


class FooterNav(models.Model):
    title = models.CharField(max_length=50)
    page = models.ForeignKey("Page", blank=True, null=True, on_delete=models.CASCADE)
    custom_url = models.CharField(max_length=200, blank=True, null=True, help_text="optional if you set a page")
    display_order = models.IntegerField(default=999)

    class Meta:
        ordering =['display_order']

    def clean(self):
        if not self.page and self.custom_url:
            raise ValidationError('You need to assign a page or set custom URL!')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_url(self):
        if self.custom_url:
            return self.custom_url

        return reverse('page_detail', kwargs={'slug': self.page.slug})
    get_url.short_description = 'URL'


class Page(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, help_text="Unique URL for this page")
    content = tinymce_models.HTMLField()


    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"
