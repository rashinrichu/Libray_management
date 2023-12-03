# Generated by Django 3.2.16 on 2023-04-28 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0002_auto_20230427_1850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='member',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_date',
        ),
        migrations.AlterField(
            model_name='payment',
            name='penalty',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='penalty_reason',
            field=models.CharField(blank=True, choices=[('late_return', 'Late return'), ('damage', 'Damage'), ('loss', 'Loss'), ('overdue', 'Overdue')], max_length=200, null=True),
        ),
    ]
