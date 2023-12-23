from django.db import models
from django.utils.text import slugify
# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    feature_image = models.ImageField(upload_to='blog/',verbose_name="Feature Image")
    status = models.CharField(max_length=20,choices=(('public','Public'),('draft','Draft')),default='draft')
    published_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        super(Blog,self).save(*args,**kwargs)