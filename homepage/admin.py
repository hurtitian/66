from django.contrib import admin
from homepage.models import *

# Register your models here.

@admin.register(BookInfo)
class BookInfoAdmin(admin.ModelAdmin):
    list_display=('id', 'isbn', 'press','name', 'classify','price','stock','authors')\

@admin.register(BookImgs)
class BookImgsAdmin(admin.ModelAdmin):
    list_display=('id', 'book_id', 'detail_img','cover_img')\

@admin.register(UserAddr)
class BookImgsAdmin(admin.ModelAdmin):
    list_display=('id', 'addr', 'user_id_id')

@admin.register(UserInfo)
class BookImgsAdmin(admin.ModelAdmin):
    list_display=('id', 'nickname', 'emailaddr','createdata')



