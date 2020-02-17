from django.db import models
from django.conf import settings
from paytmpg import PaymentStatusDetailBuilder
import requests
import json
from payment import paytm


class Transaction(models.Model):
    made_by = models.ForeignKey('registration.Profile', related_name='transactions',
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)
    reason = models.CharField(max_length=256, default='not specified')

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('ABHISARGA%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)

    def retrieve_status(self):
        # initialize a dictionary
        paytmParams = dict()

        # body parameters
        paytmParams["body"] = {

            # Find your MID in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
            "mid": settings.PAYTM_MERCHANT_ID,

            # Enter your order id which needs to be check status for
            "orderId": self.order_id,
        }

        # Generate checksum by parameters we have in body
        # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
        checksum = paytm.generate_checksum_by_str(json.dumps(paytmParams["body"]), settings.PAYTM_SECRET_KEY)

        # head parameters
        paytmParams["head"] = {

            # put generated checksum value here
            "signature": self.checksum
        }

        # prepare JSON string for request
        post_data = json.dumps(paytmParams)

        # for Staging
        url = "https://securegw-stage.paytm.in/merchant-status/api/v1/getPaymentStatus"

        # for Production
        # url = "https://securegw.paytm.in/merchant-status/api/v1/getPaymentStatus"

        response = requests.post(url, data=post_data, headers={"Content-type": "application/json"}).json()
        print(response)
        print(dict(response))
        return response["body"]["resultCode"] == '01'

#
# class Order(models.Model):
#     txn = models.OneToOneField('Transaction', null=True, blank=True, on_delete=models.SET_NULL)

