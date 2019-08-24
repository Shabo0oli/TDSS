from import_export import resources
from .models import Tweet

class TweetResource(resources.ModelResource):
    class Meta:
        model = Tweet