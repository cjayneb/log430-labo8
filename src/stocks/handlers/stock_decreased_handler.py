"""
Handler: Stock Decreased
SPDX-License-Identifier: LGPL-3.0-or-later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from typing import Dict, Any

import requests
import config
from db import get_sqlalchemy_session
from event_management.base_handler import EventHandler
from orders.commands.order_event_producer import OrderEventProducer
from payments.models.outbox import Outbox
from payments.outbox_processor import OutboxProcessor


class StockDecreasedHandler(EventHandler):
    """Handles StockDecreased events"""
    
    def __init__(self):
        self.order_producer = OrderEventProducer()
        super().__init__()
    
    def get_event_type(self) -> str:
        """Get event type name"""
        return "StockDecreased"
    
    def handle(self, event_data: Dict[str, Any]) -> None:
        """Execute every time the event is published"""
        session = get_sqlalchemy_session()
        try: 
            new_outbox_item = Outbox(order_id=event_data['order_id'], 
                                    user_id=event_data['user_id'], 
                                    total_amount=event_data['total_amount'],
                                    order_items=event_data['order_items'])
            session.add(new_outbox_item)
            session.flush() 
            session.commit()
            OutboxProcessor().run(new_outbox_item)
        except Exception as e:
            session.rollback()
            self.logger.debug("La création d'une transaction de paiement a échoué : " + str(e))
            event_data['event'] = "PaymentCreationFailed"
            event_data['error'] = str(e)
            OrderEventProducer().get_instance().send(config.KAFKA_TOPIC, value=event_data)
        finally:
            session.close()

        # try:
        #     payment_transaction = {
        #         "user_id": event_data['user_id'],
        #         "order_id": event_data['order_id'],
        #         "total_amount": event_data['total_amount']
        #     }

        #     self.logger.debug("Requête à POST /payments")
        #     response_from_payment_service = requests.post(
        #         'http://api-gateway:8080/payments-api/payments',
        #         json=payment_transaction,
        #         headers={'Content-Type': 'application/json'}
        #     )
        #     if response_from_payment_service.ok:
        #         data = response_from_payment_service.json() 
        #         payment_id = data['payment_id']
        #         self.logger.debug(f"ID paiement: {payment_id}")
        #         event_data['event'] = "PaymentCreated"
        #         event_data['payment_link'] = f"http://api-gateway:8080/payments-api/payments/process/{payment_id}"
        #     else:
        #         self.logger.error("Erreur:", response_from_payment_service.status_code, response_from_payment_service.text)
        #         event_data['event'] = "PaymentCreationFailed"
        #         event_data['error'] = f"Erreur:{response_from_payment_service.status_code}, {response_from_payment_service.text}"

        # except Exception as e:
        #     # TODO: Si la transaction de paiement n'était pas crée, déclenchez l'événement adéquat selon le diagramme.
        #     event_data['error'] = str(e)
        #     event_data['event'] = "PaymentCreationFailed"
        # finally:
        #     OrderEventProducer().get_instance().send(config.KAFKA_TOPIC, value=event_data)