from django.db import models
from Software import models as sf_models


# Create your models here.
class MessageRecord(models.Model):
    _from = models.ForeignKey(
        sf_models.User,
        on_delete=models.DO_NOTHING,
        related_name='msg_send_from_me'
    )
    to = models.ForeignKey(
        sf_models.User,
        on_delete=models.DO_NOTHING,
        related_name='msg_send_to_me'
    )
    msg = models.TextField()
    send_time = models.DateTimeField(auto_now_add=True)


class RecentContacts(models.Model):
    user1 = models.ForeignKey(
        sf_models.User,
        on_delete=models.CASCADE,
        related_name='my_recent_contacts'
    )
    user2 = models.ForeignKey(
        sf_models.User,
        on_delete=models.CASCADE,
        related_name='+'
    )
    last_view_time = models.DateTimeField(auto_now=True)  # 最后一次查看user2发送的消息的时间

    class Meta:
        unique_together = ('user1', 'user2')
