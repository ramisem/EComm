from abc import ABC
from utils.product_exception import ProductException


class Service(ABC):
    def execute_service(self):
        # Get all attributes of the class
        all_attributes = dir(self)

        # Filter out methods
        all_services = [attr for attr in all_attributes if callable(getattr(self, attr)) and not attr.startswith("__")]

        if self.service_name is None:
            raise ProductException(message=f"Service name cannot be None.",
                                   custom_message=f"Service name cannot be None.",
                                   logoff=True,mode='redirect', page='userauths:sign-in',)

        if self.service_name in all_services:
            method = getattr(self, self.service_name)
            return method()
        else:
            raise ProductException(message=f"Method '{self.service_name}' does not exist in the Product service.",
                                   custom_message=f"Method '{self.service_name}' does not exist in the Product service.",
                                   logoff=True,mode='redirect', page='userauths:sign-in',)
