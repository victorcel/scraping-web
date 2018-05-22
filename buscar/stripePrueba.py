import os
import stripe
import mysql
from mysql.connector import Error

#print os.environ["USERNAME"]

cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='card')
try:

    cursor = cnx.cursor()
    query = ("SELECT * from card.tarjetas")
    cursor.execute(query)
    stripe.api_key = "sk_test_vZWR8mehe5hYWVFTpR6jKP7b"
    for resp in cursor:
        # print 'INSERT INTO checker (tarjeta_id,respuesta) VALUES ('+str(resp[0])+','+"mes"+')'
        try:
            #print resp
            token = stripe.Token.create(
                card={
                    "number": resp[1],
                    "exp_month": resp[2],
                    "exp_year": resp[3],
                    "cvc": resp[4]
                },
                # card={
                #     "number": resp[1],
                #     "exp_month": resp[4],
                #     "exp_year": resp[5],
                #     "cvc": resp[3]
                # },
            )
            # print token.id
            dato =create = stripe.Charge.create(
                amount=100,
                currency="usd",
                description="Charge for ethan.thomas@example.com",
                source=token.id  # obtained with Stripe.js
            )

            #cursor.commit()
        except stripe.error.CardError as e:  # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            print "Message is: %s" % err.get('message')
            idd=int(resp[1])
            try:
                cnx1 = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='card')
                insertar = cnx1.cursor()
                insertar.execute("INSERT INTO checker(tarjeta_id,respuesta) VALUES (%s,%s)", (idd, err.get('message')))
                cnx1.commit()
                cnx1.close()
            except Error as e:
                pass
            # resp = "INSERT INTO checker (tarjeta_id,respuesta) VALUES ('34','hola');"#%(idd,'hola')
            # print resp


except stripe.error.CardError as e:  # Since it's a decline, stripe.error.CardError will be caught
    body = e.json_body
    err = body.get('error', {})

    # print "Status is: %s" % e.http_status
    # print "Type is: %s" % err.get('type')
    # print "Code is: %s" % err.get('code')
    # # param is '' in this case
    # print "Param is: %s" % err.get('param')
    #print "Message is: %s" % err.get('message')

except stripe.error.RateLimitError as e:  # Too many requests made to the API too quickly
    pass
except stripe.error.InvalidRequestError as e:  # Invalid parameters were supplied to Stripe's API
    pass
except stripe.error.AuthenticationError as e:  # Authentication with Stripe's API failed
    # (maybe you changed API keys recently)
    pass
except stripe.error.APIConnectionError as e:  # Network communication with Stripe failed
    pass
except stripe.error.StripeError as e:  # Display a very generic error to the user, and maybe send
    # yourself an email
    pass
except Exception as e:  # Something else happened, completely unrelated to Stripe
    pass

