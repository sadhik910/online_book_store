# Generated by Django 2.2 on 2019-04-23 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20190423_2119'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book_comments',
            options={'verbose_name_plural': 'Book_comments'},
        ),
        migrations.AlterModelOptions(
            name='books',
            options={'verbose_name_plural': 'Books'},
        ),
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name_plural': 'Cart'},
        ),
        migrations.AlterModelOptions(
            name='categories',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='rating',
            options={'verbose_name_plural': 'Rating'},
        ),
    ]
