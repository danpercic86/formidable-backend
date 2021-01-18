from django.contrib.admin import ModelAdmin


class BaseModelAdmin(ModelAdmin):
    list_filter = ('created', 'modified')
    readonly_fields = ('created', 'modified')


class SlugableModelAdmin(ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


CREATED_MODIFIED = (
    'Created / Modified',
    {
        'fields': ('created', 'modified'),
        'description': 'Info about the time this entry was added here or updated',
    },
)
