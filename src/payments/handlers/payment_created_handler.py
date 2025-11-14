"""
Handler: Payment Created
SPDX-License-Identifier: LGPL-3.0-or-later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from typing import Dict, Any
import config
from event_management.base_handler import EventHandler
from orders.commands.order_event_producer import OrderEventProducer
from orders.commands.write_order import modify_order

class PaymentCreatedHandler(EventHandler):
    """Handles PaymentCreated events"""
    
    def __init__(self):
        self.order_producer = OrderEventProducer()
        super().__init__()
    
    def get_event_type(self) -> str:
        """Get event type name"""
        return "PaymentCreated"
    
    def handle(self, event_data: Dict[str, Any]) -> None:
        """Execute every time the event is published"""
        try:
            payment_link = event_data['payment_link']
            payment_id = str(payment_link).split('/')[-1]

            modified = modify_order(event_data['order_id'], event_data['is_paid'], payment_id)

            if modified:
                event_data['payment_link'] = payment_link
                self.logger.debug(f"payment_link={event_data['payment_link']}")
            else:
                event_data['error'] = "Le lien de paiement n'a pas été ajoutée à la commande."

        except Exception as e:
            # TODO: Si l'operation a échoué, déclenchez l'événement adéquat selon le diagramme.
            self.logger.debug(str(e))
            event_data['error'] = str(e)
        finally:
            event_data['event'] = "SagaCompleted"
            OrderEventProducer().get_instance().send(config.KAFKA_TOPIC, value=event_data)


