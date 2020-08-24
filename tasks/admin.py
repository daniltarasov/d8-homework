from django.contrib import admin
from tasks.models import TodoItem, Category, Priority


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'priority', 'is_completed', 'created')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'todos_count')
    fields = ('slug', 'name')

# @admin.register(Priority)
# class PriorityAdmin(admin.ModelAdmin):
#     list_display = ('name', 'prior_count')
#     fields = ('name',)

