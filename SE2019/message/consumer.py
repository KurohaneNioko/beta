import json
from channels.generic.websocket import AsyncWebsocketConsumer
import time
from .models import *
from Software import models as sf_models
from django.db.models import Q


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 当 websocket 一链接上以后触发
        self.uid = self.scope['session'].get('uid')
        self.current_contact_id = self.scope['url_route']['kwargs']['uid']
        await self.channel_layer.group_add(
            str(self.uid),
            self.channel_name
        )
        await self.accept()
        current_user = sf_models.User.objects.get(id=self.uid)
        for item in current_user.my_recent_contacts.all():
            if item.user2.id == self.current_contact_id:
                self.messages = MessageRecord.objects.filter(Q(_from=current_user, to_id=item.user2.id,
                                                               ) | Q(
                    _from_id=item.user2.id, to=current_user,
                )).order_by('-send_time')
                messages = reversed(MessageRecord.objects.filter(Q(_from=current_user, to_id=item.user2.id,
                                                                   ) | Q(
                    _from_id=item.user2.id, to=current_user,
                )).order_by('-send_time')[:50])
                self.messages = self.messages[50:]
                for msg in messages:
                    await self.channel_layer.send(
                        self.channel_name,
                        {
                            'type': 'send_message',
                            'message': {'from_id': msg._from_id, "from_name": msg._from.name,
                                        "to_id": msg.to_id, "to_name": msg.to.name, "initial": True,
                                        "send_time": msg.send_time.timestamp(), "message": msg.msg,"avatar":msg._from.avatar.name}
                        }
                    )
            else:
                count = MessageRecord.objects.filter(_from=item.user2, to=current_user,
                                                     send_time__gt=item.last_view_time).count()
                try:
                    last_msg = MessageRecord.objects.filter(Q(_from=current_user, to_id=item.user2.id,
                                                              ) | Q(
                        _from_id=item.user2.id, to=current_user, )).order_by('-send_time').first().msg
                except AttributeError:
                    last_msg = ""

                await self.channel_layer.send(
                    self.channel_name,
                    {
                        'type': 'send_message',
                        'message': {'from_id': item.user2.id, "from_name": item.user2.name,
                                    "to_id": current_user.id, "to_name": current_user.name, "initial": True,
                                    "new_count": count, "message": last_msg}
                    }
                )

    async def disconnect(self, close_code):
        # 断开链接
        await self.channel_layer.group_discard(
            str(self.uid),
            self.channel_name
        )
        RecentContacts.objects.filter(user1_id=self.uid, user2_id=self.current_contact_id).update()

    async def get_more_message(self):
        messages = self.messages[:20]
        self.messages = self.messages[20:]
        for msg in messages:
            await self.channel_layer.group_send(
                str(self.uid),
                {
                    'type': 'send_message',
                    'message': {'from_id': msg._from_id, "from_name": msg._from.name,
                                "to_id": msg.to_id, "to_name": msg.to.name, "more_msg": True,
                                "send_time": msg.send_time.timestamp(), "message": msg.msg,"avatar":msg._from.avatar.name}
                }
            )

    async def get_new_message(self, text_data_json):
        text_data_json['send_time'] = time.time()
        text_data_json['initial'] = False
        to_id = text_data_json['to_id']
        from_id = text_data_json['from_id']
        text_data_json['avatar'] = sf_models.User.objects.get(id=from_id).avatar.name;
        RecentContacts.objects.get_or_create(user1_id=to_id, user2_id=from_id)
        MessageRecord.objects.create(_from_id=from_id, to_id=to_id,
                                     msg=text_data_json['message'])
        await self.channel_layer.group_send(
            str(to_id),
            {
                'type': 'send_message',
                'message': text_data_json
            }
        )

        await self.channel_layer.send(
            self.channel_name,
            {
                'type': 'send_message',
                'message': text_data_json
            }
        )

    async def receive(self, text_data):
        # 前端发送来消息时，通过这个接口传递
        text_data_json = json.loads(text_data)
        if text_data_json.get('more_msg'):
            await self.get_more_message()
            return
        elif text_data_json.get('delete'):
            RecentContacts.objects.filter(user1_id=self.uid, user2__name=text_data_json.get('delete_name')).delete()
            return
        await self.get_new_message(text_data_json)

    async def send_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
        # print(message)

