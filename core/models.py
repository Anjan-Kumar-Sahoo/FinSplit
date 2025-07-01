from django.db import models

class User(models.Model):
    upi_id = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.upi_id})"

class Pool(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PoolMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'pool')

class Bill(models.Model):
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - ₹{self.amount} in {self.pool.name}"

class BillSplit(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    owed_by = models.ForeignKey(User, related_name='owes', on_delete=models.CASCADE)
    owed_to = models.ForeignKey(User, related_name='gets', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_settled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.owed_by} owes {self.owed_to} ₹{self.amount}"
