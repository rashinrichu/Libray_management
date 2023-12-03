# Generated by Django 3.2.16 on 2023-04-27 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='penalty',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='penalty_reason',
            field=models.CharField(blank=True, choices=[('none', 'No penalty'), ('damage', 'Damage'), ('overdue', 'Overdue'), ('other', 'Other')], max_length=255, null=True),
        ),
    ]
