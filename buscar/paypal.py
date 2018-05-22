from paypalrestsdk import CreditCard
import logging
logging.basicConfig(level=logging.INFO)

import paypalrestsdk
paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AX2Di4-q9p1qKXaWrCyebInnmHsU9rrE36cJr2f1kIcIEzQAga9DEXQO5iTYfMv8U5d0kDs3_iq5dU0-",
  "client_secret": "EOut2Ke5Vk7UP9rFyB-KIMHKzdY1X1dRGpjtiJIOMqAXDar86Dd6MMO6F5rcmsI1ymTi44fEcPnU7Lpk" })
credit_card = CreditCard({
    # CreditCard
    # A resource representing a credit card that can be
    # used to fund a payment.
    "type": "visa",
    "number": "4924897140074588",
    "expire_month": "04",
    "expire_year": "2022",
    "cvv2": "969",
    "first_name": "Joe",
    "last_name": "Shopper",

    # Address
    # Base Address object used as shipping or billing
    # address in a payment. [Optional]
    "billing_address": {
        "line1": "52 N Main ST",
        "city": "Johnstown",
        "state": "OH",
        "postal_code": "43210",
        "country_code": "US"}})

# Make API call & get response status
# Save
# Creates the credit card as a resource
# in the PayPal vault.
if credit_card.create():
    print("CreditCard[%s] created successfully" % (credit_card.id))
else:
    print("Error while creating CreditCard:")
print(credit_card.error)