"""
Event Handler base class
SPDX-License-Identifier: LGPL-3.0-or-later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from logger import Logger

class EventHandler(ABC):
    """Base class for all event handlers"""

    def __init__(self):
        """ Constructor method """
        self.logger = Logger.get_instance('Handler')
    
    @abstractmethod
    def handle(self, event_data: Dict[str, Any]) -> None:
        """Process the event data"""
        pass
    
    @abstractmethod
    def get_event_type(self) -> str:
        """Return the event type this handler processes"""
        pass