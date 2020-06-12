from django.db import models
from django.conf import settings
# Create your models here.
from time import timezone
from django.utils import timezone

from django.db import models

# Create your models here.

class User(models.Model):
 
    user_id = models.CharField(max_length=3, default=0)
    name = models.CharField('社員名前', max_length=20, default='社員名前')
    user_number = models.CharField('社員番号', max_length=10, default='社員番号')
    user_tel = models.CharField('電話番号', max_length=13, default='電話番号')
    user_ad = models.CharField('社員住所', max_length=48, default='社員住所')
    class Meta:
        verbose_name = "社員"
        verbose_name_plural = "社員管理"
    def __str__(self):
        return self.name

class Duty_m(models.Model):
 
    date = models.DateField('出勤日付',default=timezone.now)
    #user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    duty_status = (
        (0, '出勤'),
        (1, '祝日'),
        (2, '早退'),
        (3, '遅刻'),
        (4, 'シフト'),
        (5, '休出'),
        (6, '欠勤'),
        (7, '年休'),
        (8, '振休'),
    )
    duty = models.IntegerField(choices=duty_status, verbose_name='出勤状态', default=0)
    start_time =  models.TimeField('開始時刻',default='09:00')
    end_time = models.TimeField('終了時刻', default='18:00')
    working_time = models.DateTimeField(verbose_name='実働時間', auto_now=True)

    rest_time = (
        (0, models.TimeField(default='0.00')),
        (1, models.TimeField(default='1.00')),
    )
    rest = models.TimeField('休憩時間', default='1:00')

    # contents_status = (
    #     (0, '保守作業'),
    #     (1, '開発作業'),
    #     (2, '本番前準備作業'),
    #     (3, '顧客指示によるシフト勤務'),
    #     (4, '体調不良にため'),
    # )
    contents = models.TextField(max_length=48, verbose_name='作業概要', default='開発作業')

    status_c = (
        (0, '未提出'),
        (1, '提出済み'),
        (2, '承認済み'),
    )
    status = models.IntegerField(choices=status_c, verbose_name='ステイタス', default=0)

    user_id = models.CharField(max_length=3, default=0)
    name = models.CharField('社員名前', max_length=20, default=0)

    class Meta:
        verbose_name = "勤務"
        verbose_name_plural = "勤務管理"