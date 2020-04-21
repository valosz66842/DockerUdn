import json
import os
import datetime
from WebNews.models import Udn
from channels.layers import get_channel_layer
import asyncio
from django.forms.models import model_to_dict
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
class ScrapyudnPipeline(object): #存進MModel
    def process_item(self, item, spider):
        item.save()
        channel_layer = get_channel_layer()
        news = Udn.objects.get(id=item['id'])  #避免傳送錯誤的資料
        loop = asyncio.get_event_loop()
        loop.create_task(channel_layer.group_send("UdnNews_Group", {"type": "Add_news",
                                                                    "text_data": json.dumps(model_to_dict(news),
                                                                                            default=default)}))
        return item

