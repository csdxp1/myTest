import datetime
import xlrd
import xlwt 
import xlutils.copy

from django.contrib import admin, messages
from django.db import transaction
from django.shortcuts import render
from django.contrib.admin import actions
from django.urls import reverse
from django.contrib import admin
from django.contrib.auth import get_user

from xlutils.copy import copy 

from Duty.models import *
# from User.models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

class ProxyResource(resources.ModelResource):
    class Meta:
        model = User
        model = Duty_m

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    resource_class = ProxyResource
    #display
    list_display = ('name', 'user_number', 'user_tel', 'user_ad',)
    fieldsets = [(None,{'fields':['name', 'user_number', 'user_tel', 'user_ad',]})]
    ordering = ('name',)
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        obj.user_id = request.user.id
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user_id = request.user.id)


@admin.register(Duty_m)
class Spl3Admin(admin.ModelAdmin):

    actions = ['commit_button','export', 'delete_selected']
    admin.site.disable_action('delete_selected')
    resource_class = ProxyResource

    #display
    list_display = ('name', 'date', 'duty', 'start_time', 'end_time', 'rest', 'working_time', 'contents', 'status',)
    #list
    list_filter = ('status','date')
    #set search
    search_fields = ('name', 'date', 'duty', 'start_time', 'end_time', 'rest', 'working_time', 'contents', 'status',)
    #set field
    fieldsets = [(None,{'fields':['date', 'duty', 'start_time', 'end_time', 'rest', 'contents']})]
    ordering = ('date',)
    list_per_page = 10       


    def delete_selected(self, request, queryset):
        for obj in queryset:
            if not self.has_delete_permission(request, obj):
                messages.add_message(request, messages.ERROR, '権限なしまたは提出済のレコードのために、削除できません！')
                return
        return actions.delete_selected(self, request, queryset)

    def has_delete_permission(self, request, obj=None):
        if obj:
            if obj.status != 0:  
                return False
        return super().has_delete_permission(request)

    #user set
    def save_model(self, request, obj, form, change):
        if obj.status != 0:
            messages.add_message(request, messages.ERROR, '提出済记录が編集できません')
            return
        obj.user_id = request.user.id
        obj.name = User.objects.get(user_id=request.user.id).name
        super().save_model(request, obj, form, change)

    #user filter
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user_id = request.user.id)

    #commit
    def commit_button(self, request,queryset):
        if request.user.is_superuser:
            for obj in queryset:
                if obj.status != 1:
                    messages.add_message(request, messages.ERROR, '提出済记录を選択してください')
                    return
            queryset.update(status=2)
        else:
            for obj in queryset:
                if obj.status != 0:
                    messages.add_message(request, messages.ERROR, '未提出记录を選択してください')
                    return
            queryset.update(status=1)
    commit_button.short_description = '提出/承認'
    commit_button.type = 'success'
    commit_button.confirm = '提出よろしですか？'
    commit_button.icon = 'fas fa-user-check'



    def export(self, request,queryset):

        book = xlrd.open_workbook('C:/Users/USER/Documents/TEST/勤務表.xls', formatting_info=True) 
        # book_sheet = book.sheets()[0] 

        # copy
        copy_book = xlutils.copy.copy(book)
        copy_sheet = copy_book.get_sheet(0)

        timestyle = xlwt.easyxf("""
                    font:
                        name ＭＳ Ｐゴシック,
                        colour_index black,
                        bold off,
                        height 220;
                    align:
                        wrap off,
                        vert center,
                        horiz center;
                    pattern:
                        pattern solid,
                        fore-colour 0x2A;
                    borders:
                        left THIN,
                        right NO_LINE,
                        top THIN,
                        bottom THIN;
                    """)
        timestyle.num_format_str = 'h:mm'

        datastyle = xlwt.easyxf("""
                    font:
                        name ＭＳ Ｐゴシック,
                        colour_index black,
                        bold off,
                        height 220;
                    align:
                        wrap off,
                        vert center,
                        horiz center;
                    pattern:
                        pattern solid,
                        fore-colour 0x2A;
                    borders:
                        left THIN,
                        right NO_LINE,
                        top THIN,
                        bottom THIN;
                    """)


        # write
        data_row = 8
        for obj in queryset:
            # for case in switch(obj.duty):
            #     if case(0):
            #         copy_sheet.write(data_row + obj.date.day,10, '出勤',datastyle)
            #         break
            #     if case(1):
            #         copy_sheet.write(data_row + obj.date.day,10, '退勤',datastyle)
            #         break
            #     if case(2):
            #         copy_sheet.write(data_row + obj.date.day,10, '早退',datastyle)
            #         break
            #     if case():
            #         break

            if int(obj.duty) == 1:
                copy_sheet.write(data_row + obj.date.day,4, '祝日',datastyle)
            elif int(obj.duty) == 2:
                copy_sheet.write(data_row + obj.date.day,4, '早退',datastyle)
            elif int(obj.duty) == 3:
                copy_sheet.write(data_row + obj.date.day,4, '遅刻',datastyle)
            elif int(obj.duty) == 4:
                copy_sheet.write(data_row + obj.date.day,4, 'シフト',datastyle)
            elif int(obj.duty) == 5:
                copy_sheet.write(data_row + obj.date.day,4, '休出',datastyle)
            elif int(obj.duty) == 6:
                copy_sheet.write(data_row + obj.date.day,4, '欠勤',datastyle)
            elif int(obj.duty) == 7:
                copy_sheet.write(data_row + obj.date.day,4, '年休',datastyle)
            elif int(obj.duty) == 8:
                copy_sheet.write(data_row + obj.date.day,4, '振休',datastyle)
            elif int(obj.duty) == 0:
                copy_sheet.write(data_row + obj.date.day,4, '',datastyle)

            copy_sheet.write(data_row + obj.date.day, 6, obj.start_time, timestyle)
            copy_sheet.write(data_row + obj.date.day, 9, obj.end_time, timestyle)
            # copy_sheet.write(data_row + obj.date.day, 12, '1.0',datastyle)
            copy_sheet.write(data_row + obj.date.day, 17, obj.contents,datastyle)
            copy_sheet.write(data_row + obj.date.day,12, obj.rest,timestyle)

            # for case in switch(obj.rest):
            #     if case('0'):
            #         copy_sheet.write(data_row + obj.date.day,12, '0.0',datastyle)
            #         break
            #     if case('1'):
            #         copy_sheet.write(data_row + obj.date.day,12, '1.0',datastyle)
            #         break
            #     if case('2'):
            #         copy_sheet.write(data_row + obj.date.day,12, '1.5',datastyle)
            #         break
            #     if case('3'):
            #         copy_sheet.write(data_row + obj.date.day,12, '2.0',datastyle)
            #         break
            #     if case():
            #         break

            # if int(obj.rest) == 0:
            #     copy_sheet.write(data_row,12, '0.0',datastyle)
            # else if int(obj.rest) == 1:
            #     copy_sheet.write(data_row,12, '1.0',datastyle)
            # else if int(obj.rest) == 2:
            #     copy_sheet.write(data_row,12, '1.5',datastyle)
            # else if int(obj.rest) == 3:
            #     copy_sheet.write(data_row,12, '2.0',datastyle)
            # copy_sheet.write(data_row + obj.date.day, 12, obj.rest, timestyle)
            # copy_sheet.write(data_row + obj.date.day, 14, obj.date.day, datastyle)

        # save
        copy_book.save("C:/Users/USER/Documents/TEST/1111.xls")
        messages.add_message(request, messages.SUCCESS, '记录がエクスポートしました')
        return
            
    export.short_description = 'Excle'
  
    export.type = 'success'
    # fieldsets = [(None, {'fields': ['duty_date', 'duty_div', 'start_time', 'end_time',
    #                                 'rest_time', 'work_cmt', 'duty_sts']})]

# class switch(object):
#     def __init__(self, value):
#         self.value = value
#         self.fall = False

#     def __iter__(self):
#         """Return the match method once, then stop"""
#         yield self.match
#         raise StopIteration
    
#     def match(self, *args):
#         """Indicate whether or not to enter a case suite"""
#         if self.fall or not args:
#             return True
#         elif self.value in args: # changed for v1.5, see below
#             self.fall = True
#             return True
#         else:
#             return False

