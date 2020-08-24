from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from tasks.models import TodoItem, Category, Priority
from collections import Counter


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_added(sender, instance, action, model, pk_set, **kwargs):
    if action != "post_add" or model != Category:
        return
    """
    замена счетчика задач работой с моделью
    """
    for pk in pk_set:
        cat = Category.objects.get(id=pk)
        cat.todos_count+=1
        cat.save()

    # for cat in instance.category.all():
    #     slug = cat.slug

    #     new_count = 0
    #     for task in TodoItem.objects.all():
    #         new_count += task.category.filter(slug=slug).count()

    #     Category.objects.filter(slug=slug).update(todos_count=new_count)


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_removed(sender, instance, action, model, pk_set, **kwargs):
    if action != "post_remove" or model != Category:
        return
    
    """
    замена счетчика задач работой с моделью
    """
    for pk in pk_set:
        cat = Category.objects.get(id=pk)
        cat.todos_count-=1
        cat.save()
    
    # cat_counter = Counter()
    # for t in TodoItem.objects.all():
    #     for cat in t.category.all():
    #         cat_counter[cat.slug] += 1
    """
    УСТРАНЯЕМ ОШИБКУ В КОДЕ (ЕСЛИ КОЛИЧЕСТВО ЗАДАЧ В КАТЕГОРИИ СТАЛО РАВНО НУЛЮ)
    """
    # for c in Category.objects.all():
    #     if c.slug not in cat_counter.keys():
    #         cat_counter[c.slug] = 0


    # for slug, new_count in cat_counter.items():
    #     Category.objects.filter(slug=slug).update(todos_count=new_count)


@receiver(post_save, sender=TodoItem)
def priority_chahged(sender, instance, **kwargs):

    pr = instance.priority
    try:
        obj = Priority.objects.get(name=pr)
    except Priority.DoesNotExist:
        obj = Priority.objects.create(name=pr, prior_count=0)

    prior_counter = Counter()
    for t in TodoItem.objects.all():
        prior_counter[t.priority] += 1

    for p in Priority.objects.all():
        if p.name not in prior_counter.keys():
            p.delete()

    for prior, new_count in prior_counter.items():
        Priority.objects.filter(name=prior).update(prior_count=new_count)
