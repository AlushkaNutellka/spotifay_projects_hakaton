from django.contrib import admin
from .models import MusicInfo, Rating, Like, Comment, Basket
from django.utils.safestring import mark_safe


class RatingInline(admin.TabularInline):
    model = Rating


@admin.register(MusicInfo)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'get_rating', 'image', 'image_show')
    inlines = [RatingInline]
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title', )}
    ordering = ['-created_at']
    list_filter = ['title']

    def image_show(self, obj):
        if obj.image:
            return mark_safe("<img src='{}' width='60 />".format(obj.image.url))
        return 'None'

    image_show.__name__ = 'Картинка'

    def get_rating(self, obj):
        from django.db.models import Avg
        result = obj.ratings.aggregate(Avg('rating'))
        return result['rating__avg']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('author', 'like', 'is_liked')
    search_fields = ['author', 'like']
    ordering = ['-is_liked']
    list_filter = ['author']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'rating')
    search_fields = ['author', 'post']
    ordering = ['-rating']
    list_filter = ['author']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'post', 'created_at', 'author')
    search_fields = ['comment', 'author']
    ordering = ['-created_at']
    list_filter = ['comment']


# class ImageAdmin(admin.TabularInline):
#     model = Image
#     readonly_fields = ('get_image',)
#
#     def get_image(self, obj):
#         return mark_safe(f'<img src="{obj.image.url}" width="60" height="60" />')
#
#     get_image.short_description = 'Картинка'

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('basket',)
    search_fields = ['basket', 'author']
    # ordering = ['-created_at']
    list_filter = ['basket']