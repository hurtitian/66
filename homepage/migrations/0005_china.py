# Generated by Django 2.2.4 on 2019-09-14 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0004_delete_china'),
    ]

    operations = [
        migrations.CreateModel(
            name='China',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=40, null=True)),
            ],
            options={
                'db_table': 'china',
                'managed': False,
            },
        ),
    ]
