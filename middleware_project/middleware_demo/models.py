from django.db import models


class StatisticsLog(models.Model):
    request_path = models.CharField(max_length=255)
    # user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    ip_address = models.GenericIPAddressField()
    response_time = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
