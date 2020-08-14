from django.db import models

class QR(models.Model):
    record_id = models.CharField(max_length=32)
    qr_code = models.CharField(max_length=256)
    is_done = models.CharField(max_length=1)

    def __str__(self):
        return self.qr_code.__str__()
    
