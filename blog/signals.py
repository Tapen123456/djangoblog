from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Post


@receiver(post_delete, sender=Post)
def delete_post_image(sender, instance, **kwargs):
    """Delete the cover image file when a Post is deleted."""
    if instance.cover_image:
        instance.cover_image.delete(save=False)


@receiver(pre_save, sender=Post)
def delete_old_image_on_change(sender, instance, **kwargs):
    """Delete the old cover image file when a Post's image is replaced."""
    if not instance.pk:
        return  # New Post, so there is no old image

    try:
        old_post = Post.objects.get(pk=instance.pk)
    except Post.DoesNotExist:
        return

    if old_post.cover_image and old_post.cover_image != instance.cover_image:
        old_post.cover_image.delete(save=False)
        DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']