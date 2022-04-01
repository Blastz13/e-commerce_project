from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Comment
from .models import Feed
from .models import OurBrand
from .models import Tag
from .models import CategoryFeed
from .models import ContactForm
from .models import ContactAddress

@admin.register(OurBrand)
class AdminOurBrand(admin.ModelAdmin):
    list_display = ['title', 'get_image', 'order']
    list_display_links = ['title', 'get_image', 'order']
    search_fields = ('title',)

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width="320" height="180"')

    get_image.short_description = "Фото"


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = ['title', 'slug']
    list_display_links = ['title', 'slug']
    search_fields = ('title',)


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ['email', 'name', 'text', 'date_publicate']
    list_display_links = ['email', 'name', 'text', 'date_publicate']
    search_fields = ('email', 'name', 'text', 'date_publicate',)
    readonly_fields = ('date_publicate',)

class СommentItemInline(admin.TabularInline):
    model = Comment
    list_display = ['email', 'name', 'text', 'date_publicate']
    list_display_links = ['email', 'name', 'text', 'date_publicate']
    search_fields = ('email', 'name', 'text', 'date_publicate',)
    extra = 1


@admin.register(Feed)
class AdminFeed(admin.ModelAdmin):
    list_display = ['title', 'slug', 'body', 'get_image', 'is_slider', 'is_blog', 'is_publish', 'date_publicate']
    list_display_links = ['title', 'slug', 'body', 'get_image']
    search_fields = ('title', 'slug', 'body', 'date_publicate')
    inlines = [СommentItemInline]

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width="640" height="360"')

    get_image.short_description = "Фото"


@admin.register(CategoryFeed)
class AdminCategoryFeed(admin.ModelAdmin):
    list_display = ['title', 'slug']
    list_display_links = ['title', 'slug']
    search_fields = ('title', 'slug')


@admin.register(ContactForm)
class AdminContactForm(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'date_send']
    list_display_links = ['name', 'email', 'subject', 'date_send']
    search_fields = ('name', 'email', 'subject', 'date_send')
    readonly_fields = ('date_send',)


@admin.register(ContactAddress)
class AdminContactForm(admin.ModelAdmin):
    list_display = ['address', 'email', 'phone', 'order']
    list_display_links = ['address', 'email', 'phone', 'order']
    search_fields = ('address', 'email', 'phone', 'order')

