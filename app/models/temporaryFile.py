import json
import requests
import app

def make_payment(credit_card, amount_charged):
    #app.logger.info('Start p')
    url = "https://dimensweb.uqac.ca/~jgnault/shops/pay/"
    payload = {
        "credit_card": credit_card,
        "amount_charged": amount_charged
    }
    response = requests.post(url, json=payload)

    return response.json()