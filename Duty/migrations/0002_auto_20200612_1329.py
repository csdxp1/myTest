# Generated by Django 3.0.6 on 2020-06-12 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Duty', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='duty_m',
            name='duty',
            field=models.IntegerField(choices=[(0, '出勤'), (1, '祝日'), (2, '早退'), (3, '遅刻'), (4, '夏休'), (5, '半休'), (6, 'シフト'), (7, '半休'), (8, '休出'), (9, '欠勤'), (10, '年休'), (11, '振休')], default=0, verbose_name='出勤状态'),
        ),
        migrations.AlterField(
            model_name='duty_m',
            name='rest',
            field=models.IntegerField(choices=[(0, models.TimeField(default='0.00')), (1, models.TimeField(default='1.00'))], default=1, verbose_name='休憩'),
        ),
    ]
