from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext as _
from adminsortable2.admin import SortableInlineAdminMixin
# from mptt.admin import DraggableMPTTAdmin

from pages.models import Pages, Redirect, Domain, Feedback, Block, PagesBlock, IndexBlock, PagesBlockGrammeme, Grammeme


class BlockInline(SortableInlineAdminMixin, admin.TabularInline):
    model = PagesBlock


@admin.register(Pages)
class PagesAdmin(admin.ModelAdmin):
    # class PagesAdmin(DraggbleMPTTAdmin):
    list_display = ('name', 'status', 'clear_cache',)
    # list_display = ('tree_actions', 'indented_title', 'status', 'clear_cache')
    inlines = (BlockInline,)

    actions = ['select_domain']

    def select_domain(modeladmin, request, queryset):
        queryset.update(domain=settings.DOMAINS[0][0])
    select_domain.short_description = _('Select first domain')

    list_filter = ('created_at',)
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'h1', 'parent', 'text', 'status', 'is_link', 'domain')
        }),
        (_('Meta'), {
            'fields': ('alias', 'replace', 'title', 'meta_d')
        }),
        (_('Дополнительно'), {
            'fields': ('template', 'address', 'ymap')
        }),
    )

    class Media:
        css = {
            'all': ('admin/css/translation.css',)
        }


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = ('domain', 'fr', 'to', 'code')
    search_fields = ('fr', 'to')


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    pass


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'update_at', 'created_at')
    list_display_links = ('id', 'name')


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(IndexBlock)
class IndexBlockAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_display_links = ('name', )


@admin.register(PagesBlockGrammeme)
class PagesBlockGrammemeAdmin(admin.ModelAdmin):
    list_display = ['page', 'active', 'block_type', 'prepend', 'show_gramms', 'number', 'transform']
    list_filter = ['page__level', 'block_type']


@admin.register(Grammeme)
class GrammemeAdmin(admin.ModelAdmin):
    list_display = ['name', 'gramm']
    list_display_links = ['name', 'gramm']
