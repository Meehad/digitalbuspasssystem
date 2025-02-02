# Generated by Django 5.1.1 on 2025-01-13 06:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='busnotification',
            old_name='BUSSSTAFF',
            new_name='BUSSROUTENUMBER',
        ),
        migrations.RenameField(
            model_name='complaint_table',
            old_name='STUDENT',
            new_name='LOGIN',
        ),
        migrations.RenameField(
            model_name='student_table',
            old_name='status',
            new_name='address',
        ),
        migrations.RemoveField(
            model_name='bussstaff_table',
            name='proof',
        ),
        migrations.RemoveField(
            model_name='complaint_table',
            name='BUSSSTAFF',
        ),
        migrations.RemoveField(
            model_name='student_table',
            name='BUSROUTE',
        ),
        migrations.RemoveField(
            model_name='student_table',
            name='balance',
        ),
        migrations.AddField(
            model_name='attendence_table',
            name='time',
            field=models.CharField(default=2, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student_table',
            name='QrCode',
            field=models.CharField(default=3, max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student_table',
            name='STOP',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to='myapp.stop_table'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attendence_table',
            name='BUSSSTAFF',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.bussstaff_table'),
        ),
        migrations.AlterField(
            model_name='attendence_table',
            name='attendence',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='attendence_table',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='busnotification',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='complaint_table',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='location_table',
            name='latitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='location_table',
            name='longitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='notification_table',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='payment_table',
            name='date',
            field=models.DateField(),
        ),
        migrations.CreateModel(
            name='balance_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.BigIntegerField()),
                ('date', models.DateField()),
                ('STUDENT', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.login_table')),
            ],
        ),
    ]
