from haystack import indexes
from itemManagement.models import Item

#  https://django-haystack.readthedocs.io/en/master/tutorial.html
#   Haystack uses this class to index models. Anything in a text field is searchable text.
#   Any other fields can be used as filters
#   To check if models are being indexed properly, you can use this link: https://stackoverflow.com/a/13022937

class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    deleted = indexes.BooleanField(model_attr='deleted')
    lastUsed = indexes.DateTimeField(model_attr="lastUsed")
    title = indexes.CharField(model_attr="title")

    def get_model(self):
        return Item
