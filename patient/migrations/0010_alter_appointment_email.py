# Generated by Django 5.0.2 on 2024-03-06 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0009_rename_user_id_appointment_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]