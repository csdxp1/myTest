# Generated by Django 3.0.6 on 2020-06-12 04:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Duty_m',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='出勤日付')),
                ('duty', models.IntegerField(choices=[(0, '出勤'), (1, '退勤'), (2, '早退'), (3, '遅刻'), (4, '夏休'), (5, '半休'), (6, 'シフト'), (7, '半休'), (8, '休出'), (9, '欠勤'), (10, '年休'), (11, '振休'), (12, '祝日')], default=0, verbose_name='出勤状态')),
                ('start_time', models.TimeField(default='09:00', verbose_name='開始時刻')),
                ('end_time', models.TimeField(default='18:00', verbose_name='終了時刻')),
                ('working_time', models.DateTimeField(auto_now=True, verbose_name='実働時間')),
                ('rest', models.IntegerField(choices=[(0, '0.0'), (1, '1.00'), (2, '1.50'), (3, '2.00')], default=1, verbose_name='休憩')),
                ('contents', models.TextField(default='開発作業', max_length=48, verbose_name='作業概要')),
                ('status', models.IntegerField(choices=[(0, '未提出'), (1, '提出済み'), (2, '承認済み')], default=0, verbose_name='ステイタス')),
                ('user_id', models.CharField(default=0, max_length=3)),
                ('name', models.CharField(default=0, max_length=20, verbose_name='社員名前')),
            ],
            options={
                'verbose_name': '勤務',
                'verbose_name_plural': '勤務管理',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default=0, max_length=3)),
                ('name', models.CharField(default='社員名前', max_length=20, verbose_name='社員名前')),
                ('user_number', models.CharField(default='社員番号', max_length=10, verbose_name='社員番号')),
                ('user_tel', models.CharField(default='電話番号', max_length=13, verbose_name='電話番号')),
                ('user_ad', models.CharField(default='社員住所', max_length=48, verbose_name='社員住所')),
            ],
            options={
                'verbose_name': '社員',
                'verbose_name_plural': '社員管理',
            },
        ),
    ]
