"""
Handler: Order Cancelled
SPDX-License-Identifier: LGPL-3.0-or-later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from typing import Dict, Any
import config
from event_management.base_handler import EventHandler
from orders.commands.order_event_producer import OrderEventProducer


class OrderCancelledHandler(EventHandler):
    """Handles OrderCancelled events"""
    
    def __init__(self):
        self.order_producer = OrderEventProducer()
        super().__init__()
    
    def get_event_type(self) -> str:
        """Get event type name"""
        return "OrderCancelled"
    
    def handle(self, event_data: Dict[str, Any]) -> None:
        """Execute every time the event is published"""
        # La commande a été annullé, il n'y a donc rien d'autre à faire. Déclenchez l'événement SagaCompleted.
        event_data['event'] = "SagaCompleted"
        OrderEventProducer().get_instance().send(config.KAFKA_TOPIC, value=event_data)


