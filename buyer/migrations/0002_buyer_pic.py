# Generated by Django 4.1 on 2022-09-23 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("buyer", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="buyer",
            name="pic",
            field=models.FileField(default="sad.jpg", upload_to="media"),
        ),
    ]
