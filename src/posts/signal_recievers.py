from .utils import create_slug, get_read_time


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    super_class = type(instance)   # super = Post(models.Model)
    number = super_class.objects.filter(title=instance.title).count()
    if not instance.slug:
        instance.slug = create_slug(instance.title, number)

    try:
        if instance.content:
            html_string = instance.content                           # TODO: Replace by get markdown
            read_time = get_read_time(html_string)
            instance.read_time = read_time

    except AttributeError:
        pass
