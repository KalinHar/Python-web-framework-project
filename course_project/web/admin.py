from django.contrib import admin

from course_project.web.models import Client, Taxes, OldDebts, Notice, Archive, Master


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('names', 'phone', 'old_debts', 'username')


@admin.register(Taxes)
class TaxesAdmin(admin.ModelAdmin):
    list_display = ('price', 'tax')


@admin.register(Archive)
class ArchiveAdmin(admin.ModelAdmin):
    pass


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')


@admin.register(OldDebts)
class OldDebtsAdmin(admin.ModelAdmin):
    pass


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    pass