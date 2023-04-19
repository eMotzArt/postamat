from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from core.models import Comment, Post, User

# Register your models here.


class CustomPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'link_to_author', 'short_text')
    list_filter = ('created_at',)
    def short_text(self, obj):
        if len(obj.text) > 50:
            return f"{obj.text[:50]}..."
        return obj.text
    short_text.short_description = "Текст"

    def link_to_author(self, obj):
        url = reverse("admin:core_user_change", args=[obj.author.id])
        link = f'<a href="{url}">{obj.author}</a>'

        return mark_safe(link)
    link_to_author.short_description = 'Автор'


admin.site.register(User)
admin.site.register(Post, CustomPostAdmin)
admin.site.register(Comment)
