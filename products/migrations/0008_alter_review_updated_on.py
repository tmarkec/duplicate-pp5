# Generated by Django 3.2 on 2023-05-03 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_review_updated_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='updated_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
