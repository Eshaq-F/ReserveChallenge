# Generated by Django 4.1.5 on 2023-01-28 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('number', models.AutoField(primary_key=True, serialize=False, verbose_name='room number')),
            ],
        ),
        migrations.CreateModel(
            name='Reserve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_fullname', models.CharField(max_length=500, verbose_name='customer fullname')),
                ('from_dt', models.DateTimeField()),
                ('to_dt', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='reservation.room', verbose_name='related room')),
            ],
        ),
        migrations.AddConstraint(
            model_name='reserve',
            constraint=models.CheckConstraint(check=models.Q(('to_dt__gt', models.F('from_dt'))), name='to_dt > from_dt'),
        ),
    ]