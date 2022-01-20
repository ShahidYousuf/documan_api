# Generated by Django 4.0.1 on 2022-01-19 10:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='shared_with',
            field=models.ManyToManyField(blank=True, null=True, related_name='shared_documents', to=settings.AUTH_USER_MODEL),
        ),
    ]