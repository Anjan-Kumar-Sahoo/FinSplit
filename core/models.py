from django.db import models

class User(models.Model):
    upi_id = models.CharField(max_length=50,unique=True)
    full_name = models.CharField(max_length=100)
    creadted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.upi_id})"
    
class Pool(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class PoolMember(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    pool = models.ForeignKey(Pool,on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'pool')