"""
Handler: Saga Completed
SPDX-License-Identifier: LGPL-3.0-or-later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from typing import Dict, Any
from event_management.base_handler import EventHandler
from orders.commands.order_event_producer import OrderEventProducer

class SagaCompletedHandler(EventHandler):
    """Handles SagaCompleted events (either for successful or failed completion) """
    
    def __init__(self):
        self.order_producer = OrderEventProducer()
        super().__init__()
    
    def get_event_type(self) -> str:
        """Get event type name"""
        return "SagaCompleted"
    
    def handle(self, event_data: Dict[str, Any]) -> None:
        """Execute every time the event is published"""
        # Réussi ou échoué, votre saga termine ici.
        if 'error' in event_data:
            self.logger.info("Saga terminée avec des erreurs. Veuillez consulter les données de l'événement pour plus d'informations.")
        else:
            self.logger.info(f"Saga terminée avec succès ! Votre order_id = {event_data['order_id']}. Votre payment_link = '{event_data['payment_link']}' .")
        self.logger.info(event_data)


