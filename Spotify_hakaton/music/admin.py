from django.contrib import admin
from .models import MusicInfo, Rating, Like


class RatingInline(admin.TabularInline):
    model = Rating


@admin.register(MusicInfo)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'get_rating')
    inlines = [RatingInline]
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title', )}
    ordering = ['-created_at']
    list_filter = ['title']

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