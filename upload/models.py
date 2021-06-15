from django.db import models
import os
from login_app.models import User



class SoundManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['ftitle'])<2:
            errors["title"] = "Title must be at least 2 chars"

class CatManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['ftitle'])<2:
            errors["title"] = "Title must be at least 1 chars"
        for x in Category.objects.all():
            if postData['ftitle'] == x.title:
                errors['ftitle'] = "The category with the same name already exists!"
        return errors

class Category(models.Model):
    title = models.CharField(max_length=55)
    slug = models.SlugField(max_length=128)
    objects = CatManager() #added

    def __str__(self):
        return self.title

class Sound(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="sounds_created",on_delete=models.CASCADE,)
    def get_upload_path(instance, filename): #creates a dynamic file path
        return os.path.join(
        "sound_%s" % instance.category, filename)
        

    soundfile = models.FileField(upload_to=get_upload_path,
    null=True, blank=True, verbose_name = "")
    fans = models.ManyToManyField(User, related_name='faves')

    def extension(self): #gets the extension
        title, extension = os.path.splitext(self.soundfile.name)
        return extension.replace(".","")
    
    # def play(self):
    #     winsound.PlaySound(get_upload_path(), winsound.SND_FILENAME | winsound.SND_ASYNC)
    def file_name(self):
        o_name = os.path.split(self.soundfile.name)
        return o_name[1]
    objects = SoundManager() #added

    
    def __str__(self):
        return str(self.soundfile.name) #was am jor bug 8.25.2020
        # a semicolon(:) was breaking the aboth "url" path variable
    

