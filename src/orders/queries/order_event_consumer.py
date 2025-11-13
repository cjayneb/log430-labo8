"""
Kafka Consumer
SPDX-License-Identifier: LGPL-3.0-or-later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import json
import threading
from logger import Logger
from typing import Optional
from kafka import KafkaConsumer
from event_management.handler_registry import HandlerRegistry
from singleton import Singleton

logger = Logger.get_instance("OrderConsumer")

class OrderEventConsumer(metaclass=Singleton):
    """Main consumer class that receives processes Kafka events"""
    
    def __init__(
        self,
        bootstrap_servers: str,
        topic: str,
        group_id: str,
        registry: HandlerRegistry,
    ):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id
        self.registry = registry
        self.auto_offset_reset = 'latest'
        self.consumer: Optional[KafkaConsumer] = None
        self.running = False
        self.consumer_thread: Optional[threading.Thread] = None
    
    def start(self) -> None:
        """Start consuming messages from Kafka in a background thread so it does not prevent Flask from starting"""
        if self.running:
            return
            
        self.running = True
        self.consumer_thread = threading.Thread(target=self._consume_messages)
        self.consumer_thread.daemon = True 
        self.consumer_thread.start()
    
    def _consume_messages(self) -> None:
        """Continuously consume messages from Kafka"""
        logger.debug(f"Démarrer un consommateur pour le topic : {self.topic}")
        
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset=self.auto_offset_reset,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            enable_auto_commit=True,
            session_timeout_ms=30000,
            heartbeat_interval_ms=10000,
            max_poll_interval_ms=300000,
            max_poll_records=10
        )
        
        try:
            while self.running:
                messages = self.consumer.poll(timeout_ms=1000)
                
                for topic_partition, records in messages.items():
                    for message in records:
                        self._process_message(message.value)
                        
        except Exception as e:
            logger.error(f"Erreur : {e}", exc_info=True)
        finally:
            if self.consumer:
                self.consumer.close()
                logger.debug("Le consommateur a été arrêté !")
                self.stop()
    
    def _process_message(self, event_data: dict) -> None:
        """Process a single message"""
        event_type = event_data.get('event')
        
        if not event_type:
            logger.warning(f"Message missing 'event' field: {event_data}")
            return
        
        handler = self.registry.get_handler(event_type)
        
        if handler:
            try:
                logger.debug(f"Evenement : {event_type}")
                handler.handle(event_data)
            except Exception as e:
                logger.error(f"Error handling event {event_type}: {e}", exc_info=True)
        else:
            logger.debug(f"Aucun handler enregistré pour le type : {event_type}")
    
    def stop(self) -> None:
        """Stop the consumer gracefully"""
        self.running = False
        
        if self.consumer_thread and self.consumer_thread.is_alive():
            self.consumer_thread.join(timeout=10)
            
        logger.debug("Arrêter le consommateur!")
    