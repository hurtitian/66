from django.db import models
from django.conf import settings
# Create your models here.

class UserInfo(models.Model):
    nickname = models.TextField(max_length=20)
    emailaddr = models.TextField(max_length=30)
    passwd = models.TextField(max_length=20)

    createdata = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.nickname

class Comment(models.Model):

    comment = models.TextField(max_length=120)

    createdata = models.DateTimeField(auto_now_add=True)

    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

class UserAddr(models.Model):

    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    addr = models.TextField(max_length=256)

    def __str__(self):
        return  self.addr



class Recommend(models.Model):

    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    createdata = models.DateTimeField(auto_now_add=True)

    # like csv
    word_list = models.TextField(max_length=256)

class BookInfo(models.Model):

    isbn = models.TextField(max_length=256)
    press = models.TextField(max_length=256)
    classify = models.TextField(max_length=128)
    name = models.TextField(max_length=128)
    other = models.TextField(max_length=256)
    authors = models.TextField(max_length=256)
    price = models.IntegerField(default=8848996)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name

def upload_to_of_detail_img(instance, fielname):

    return '/'.join([settings.MEDIA_ROOT, str(instance.book_id.id), str(instance.book_id.id)+'-'+'detail.svg'])

def upload_to_of_cover_img(instance, fielname):

    return '/'.join([settings.MEDIA_ROOT, str(instance.book_id.id), str(instance.book_id.id)+'-'+'cover.svg'])




class BookImgs(models.Model):
    book_id = models.OneToOneField(BookInfo,on_delete=models.CASCADE)
    detail_img = models.FileField(upload_to=upload_to_of_detail_img)
    cover_img = models.FileField(upload_to=upload_to_of_cover_img)



class Order(models.Model):

    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    book_id = models.ForeignKey(BookInfo,on_delete=models.CASCADE)
    book_price = models.IntegerField(default=88489)
    createdata = models.DateTimeField(auto_now_add=True)
    recv_addr = models.TextField(max_length=256)
    express_no = models.TextField(max_length=256)


class China(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40, blank=True, null=True)
    pid = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'china'




















