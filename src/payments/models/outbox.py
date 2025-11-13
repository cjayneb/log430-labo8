"""
Outbox class (value object)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from sqlalchemy import Column, Integer, Float, JSON
from orders.models.base import Base

class Outbox(Base):
    __tablename__ = 'outbox'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    order_id = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    order_items = Column(JSON, nullable=False)
    payment_id = Column(Integer, nullable=True)