# Generated by Django 4.1.5 on 2023-02-26 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("job", "0007_apply"),
    ]

    operations = [
        migrations.AddField(
            model_name="apply",
            name="username",
            field=models.CharField(max_length=50, null=True),
        ),
    ]
