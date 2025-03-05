from flask import jsonify
from .models.Order import Order
from .models.Shipping_information import ShippingInformation
from .models.CreditCard import CreditCard

#======== PUT ========
# Description: Redirect to the correct function
@classmethod
def update(id, data, Session):
    if 'order' in data and 'credit_card' in data:
        return {"errors": {
                    "order": {
                        "code": "Bad Request",
                        "name": "Un seul type d'information peut être modifier à la fois"
                        }
                    }
                }, 400

    if 'order' in data:
        return update_order_shipping(id, data, Session)
    elif 'credit_card' in data:
        return update_order_card(id, data, Session)
    else:
        return {"error": "tea - how did you end up here"}, 418

# Description: Only update the shipping info and the email
@classmethod
def update_order_shipping(id, data, session):
    db_session = session()

    order = db_session.query(Order).get(id)
    if not order:
        return jsonify({"error": f"Order {id} not found"}), 404

    order_data = data.get('order')
    if not order_data:
        return jsonify({
            "errors": {
                "order": {
                    "code": "missing-fields",
                    "name": "Il manque un ou plusieurs champs qui sont obligatoires",
                }
            }
        }), 422
    
    email = order_data.get('email')
    shipping_data = order_data.get('shipping_information')
    
    if shipping_data is None or  email is None:
        return jsonify({
            "errors": {
                "order": {
                    "code": "missing-fields",
                    "name": "Il manque un ou plusieurs champs qui sont obligatoires",
                }
            }
        }), 422

    required_fields = ['country', 'address', 'postal_code', 'city', 'province']
    missing_fields = [field for field in required_fields if not shipping_data.get(field)]

    if missing_fields:
        return jsonify({
            "errors": {
                "order": {
                    "code": "missing-fields",
                    "name": "Il manque un ou plusieurs champs qui sont obligatoires",
                }
            }
        }), 422

    order.email = email
    if order.shipping_info:
        order.shipping_info.country = shipping_data.get("country")
        order.shipping_info.address = shipping_data.get("address")
        order.shipping_info.postal_code = shipping_data.get("postal_code")
        order.shipping_info.city = shipping_data.get("city")
        order.shipping_info.province = shipping_data.get("province")
    else:
        new_shipping_info = ShippingInformation(
            country=shipping_data.get("country"),
            address=shipping_data.get("address"),
            postal_code=shipping_data.get("postal_code"),
            city=shipping_data.get("city"),
            province=shipping_data.get("province"),
            order_id=order.id
        )
        db_session.add(new_shipping_info)

    db_session.commit()
    return jsonify(order.to_dict()), 200

#Description: Only update the credit card info
@classmethod
def update_order_card(id, data, session):
    db_session = session()

    order = db_session.query(Order).get(id)
    if not order:
        return jsonify({"error": f"Order {id} not found"}), 404
    else:
        credit_card = data.get('credit_card')
        if not credit_card:
            return jsonify({
                "errors": {
                    "order": {
                        "code": "missing-fields",
                        "name": "Les informations du client sont nécessaire avant d'appliquer une carte de crédit"
                        }
                    }
                }), 422
        required_fields = ['name', 'number', 'expiration_year', 'cvv', 'expiration_month']
        missing_fields = [field for field in required_fields if not credit_card.get(field)]
        if missing_fields:
            return jsonify({
                "errors": {
                    "order": {
                        "code": "missing-fields",
                        "name": "Les informations du client sont nécessaire avant d'appliquer une carte de crédit"
                        }
                    }
                }), 422
        
        if order.paid is True:
            return {
                "errors" : {
                    "order": {
                        "code": "already-paid",
                        "name": "La commande a déjà été payée."
                    }
                }
            }, 422

        #TO DO SEND CREDIT CARDS INFO TO SERVICE
        # if error:
            #return msg

        if order.creditCard:
            order.creditCard.name = credit_card.get("name")
            order.creditCard.number = credit_card.get("number")
            order.creditCard.expiration_year = credit_card.get("expiration_year")
            order.creditCard.cvv = credit_card.get("cvv")
            order.creditCard.exp_month = credit_card.get("exp_month")
        else:
            # If the credit card doesn't exist, create a new one
            credit_card = CreditCard(
                name=credit_card['name'],
                number=credit_card['number'],
                expiration_year=credit_card['expiration_year'],
                cvv=credit_card['cvv'],
                exp_month=credit_card['expiration_month'],
                order_id=order.id
            )
            db_session.add(credit_card)

        order.paid = True
        db_session.commit()
        return jsonify(order.to_dict()), 200