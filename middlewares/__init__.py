# It needs for relationships
from db.models.user import Users
from db.models.washer import Washer
from db.models.wash_company import WashCompany
from db.models.order import Order
from db.models.service import Service
from db.models.journal import Journal

__all__ = [Users, Washer, WashCompany, Order, Service, Journal]
