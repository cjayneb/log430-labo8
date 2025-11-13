"""
Handler: Order Creation Failed
SPDX-License-Identifier: LGPL-3.0-or-later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from typing import Dict, Any
import config
from event_management.base_handler import EventHandler
from orders.commands.order_event_producer import OrderEventProducer


class OrderCreationFailedHandler(EventHandler):
    """Handles OrderCreationFailed events"""
    
    def __init__(self):
        self.order_producer = OrderEventProducer()
        super().__init__()
    
    def get_event_type(self) -> str:
        """Get event type name"""
        return "OrderCreationFailed"
    
    def handle(self, event_data: Dict[str, Any]) -> None:
        """Execute every time the event is published"""
        # La création de la commande a échoué au départ, il n'y a donc rien d'autre à faire. Déclenchez l'événement SagaCompleted.
        event_data['event'] = "SagaCompleted"
        OrderEventProducer().get_instance().send(config.KAFKA_TOPIC, value=event_data)


