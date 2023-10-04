from enum import Enum

class UserRole(Enum):
    CUSTOMER = "customer"
    SELLER = "seller"
    
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
    