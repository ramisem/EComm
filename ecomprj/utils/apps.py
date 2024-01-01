from django.apps import AppConfig
from utils.encrypt_decrypt import EncryptDecrypt


class UtilsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'utils'
    encrypt_decrypt_instance = None

    def ready(self):
        self.encrypt_decrypt_instance = EncryptDecrypt(first_call=True)