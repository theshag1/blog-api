# Generated by Django 4.2 on 2023-05-24 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_category_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='1', upload_to=''),
            preserve_default=False,
        ),
    ]