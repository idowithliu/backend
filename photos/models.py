from django.db import models
from django.conf import settings

def unique_filename(path):
    import os, base64, datetime
    def _func(instance, filename):
        name, ext = os.path.splitext(filename)
        # name = base64.urlsafe_b64encode(name.encode("utf-8") + str(datetime.datetime.now()).encode("utf-8"))
        name = name + '-' + datetime.datetime.now().isoformat().replace(':', '-').replace('.', '-')
        # return os.path.join(path, base64.b64decode(name).decode() + ext)
        # return os.path.join(path, name + ext)
        return name + ext
    return _func

# Create your models here.
class Photo(models.Model):
    id = models.IntegerField(verbose_name="Photo ID", primary_key=True)
    image = models.ImageField(verbose_name="Image Data", upload_to=unique_filename(settings.MEDIA_ROOT))

    def __str__(self):
        return self.image.name