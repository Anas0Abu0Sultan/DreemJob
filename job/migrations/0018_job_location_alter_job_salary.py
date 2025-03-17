# Generated by Django 5.1.7 on 2025-03-17 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0017_remove_apply_unique_application_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='location',
            field=models.CharField(default='remot', max_length=50),
        ),
        migrations.AlterField(
            model_name='job',
            name='salary',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
    ]
