from django.db import models

# Create your models here.
class BlockChain(models.Model):    
    blockchain_medical_data = models.CharField(max_length=1000)

    def save(self, *args, **kwargs):
        pass
        