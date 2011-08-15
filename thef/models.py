from django.db import models
import jsonfield 

# Create your models here.
class theF (models.Model):
	the_data =jsonfield.JSONField(blank=True, null=True)
	the_data_text = models.TextField(blank=True)
	created = models.DateTimeField(auto_now_add=True)
	type = models.CharField(blank=True, max_length=128)

	def save(self, *args, **kwargs):
		self.the_data = self.the_data_text
		super(theF, self).save(*args, **kwargs)
