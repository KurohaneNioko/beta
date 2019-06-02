import datetime
from haystack import indexes
from .models import Project
from django.utils import timezone

class ProjectIndex(indexes.SearchIndex, indexes.Indexable):  # 类名必须为需要检索的Model_name+Index，这里需要检索Note，所以创建NoteIndex
    text = indexes.CharField(document=True, use_template=True)  # 创建一个text字段

    # name = indexes.CharField(model_attr='name')  # 创建一个name字段
    # intro = indexes.CharField(model_attr='introduction')
    # detailed_intro = indexes.CharField(model_attr='detailed_introduction')
    
    creator_id = indexes.IntegerField(model_attr='creator__id')
    security = indexes.IntegerField(model_attr='security_level')

    def get_model(self):  # 重载get_model方法，必须要有！
        return Project

    def index_queryset(self, using=None):  # 重载index_..函数
        """Used when the entire index for model is updated."""
        return self.get_model().objects#.filter(published_date__lte=timezone.now())
