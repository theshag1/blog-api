# Generated by Django 4.2 on 2023-05-24 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_interesting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='interesting',
            field=models.CharField(choices=[('art', 'Art'), ('busines', 'Busines'), ('danger', 'Danger'), ('internet', 'Internet'), ('songs', 'Songs'), ('artist', 'Artist'), ('sport', 'Sport'), ('river', 'River'), ('travel', 'Travel')], default='persional'),
        ),
    ]
