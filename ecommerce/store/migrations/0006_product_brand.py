# Generated by Django 3.1.7 on 2023-05-04 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20230504_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(default='', help_text='Bắt buộc', max_length=255, verbose_name='Hãng sản phẩm'),
        ),
    ]