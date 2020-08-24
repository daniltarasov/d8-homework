from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from tasks.models import TodoItem, Category, Priority
from django.views.decorators.cache import cache_page
# import datetime
# from django.utils import timezone
from django.utils import timezone, dateformat
from datetime import datetime



def index(request):

    from django.db.models import Count

    # counts = Category.objects.annotate(total_tasks=Count(
    #     'todoitem')).order_by("-total_tasks")

    """
    вывод количества категорий прямо из объекта:
    """
    cat = Category.objects.all()
    counts = {c.name: c.todos_count for c in cat}

    prior = Priority.objects.all().order_by('name')
    counts_pr = {pr.get_name_display(): pr.prior_count for pr in prior}

    data = {
        "categories": counts,
        "priority": counts_pr
    }

    return render(request, "tasks/index.html", data)

# def filter_tasks(tags_by_task):
#     return set(sum(tags_by_task, []))

def tasks_by_cat(request, cat_slug=None):
    u = request.user
    tasks = TodoItem.objects.filter(owner=u).all().order_by('priority', 'description')

    cat = None
    categories = []
    if cat_slug:
        cat = get_object_or_404(Category, slug=cat_slug)
        tasks = tasks.filter(category__in=[cat]).order_by('priority', 'description')
        categories.append(cat)
    else:
        for t in tasks:
            for categ in t.category.all():
                if categ not in categories:
                    categories.append(categ)

    return render(
        request,
        "tasks/list_by_cat.html",
        {"category": cat, "tasks": tasks, "categories": categories},
    )

"""
вместо этой вьюшки использую tasks_by_cat
"""
# class TaskListView(ListView):
#     model = TodoItem
#     context_object_name = "tasks"
#     template_name = "tasks/list.html"

#     def get_queryset(self):
#         u = self.request.user
#         qs = super().get_queryset()
#         return qs.filter(owner=u)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         user_tasks = self.get_queryset()
#         tags = []
#         categories = []
#         for t in user_tasks:
#             tags.append(list(t.category.all()))


#             for cat in t.category.all():
#                 if cat not in categories:
#                     categories.append(cat)
#             context["categories"] = categories

#         return context


class TaskDetailsView(DetailView):
    model = TodoItem
    template_name = "tasks/details.html"


@cache_page(300)
def date_view(request):
    # date_time = timezone.now()
    # во всех этих форматах на хероку при кэшировании шалят секунды (прыгают 
    # вверх-вниз на несколько значений при обновлении страницы):
    date_time = datetime.strftime(timezone.localtime(timezone.now()), '%d.%m.%Y %H:%M:%S')
    # date_time = dateformat.format(timezone.localtime(timezone.now()), 'd.m.Y H:i:s')
    data = {
        "date_time": date_time,
    }
    return render(request, "tasks/date.html", data)


    

