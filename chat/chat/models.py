from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Message(models.Model):
    """
    Модель сообщений чата
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('author'),
        related_name='author_messages'
    )
    text = models.TextField(_('text'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    def __str__(self):
        if len(self.text) > 30:
            text = f'{self.text[:30]}...'
        else:
            text = self.text
        return f'{text} by {self.author} at {self.created_at}'

    class Meta:
        ordering = ('-created_at', )
        db_table = 'message'
        verbose_name = _('message')
        verbose_name_plural = _('messages')
