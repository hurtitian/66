# Generated by Django 2.2.4 on 2019-09-14 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_order_book_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddr',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.UserInfo'),
        ),
    ]