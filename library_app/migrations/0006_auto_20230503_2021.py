# Generated by Django 3.2.16 on 2023-05-03 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0005_remove_cancelledbook_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='cancelledbook',
            name='request',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='library_app.requestbook'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='returnbook',
            name='penalty_reason',
            field=models.CharField(blank=True, choices=[('overdue', 'Overdue'), ('expired', 'Expired'), ('damage', 'Damage'), ('loss', 'Loss'), ('other', 'Other')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='returnbook',
            name='fine_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
