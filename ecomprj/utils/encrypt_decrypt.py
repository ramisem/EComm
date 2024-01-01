from cryptography.fernet import Fernet
from urllib.parse import quote, unquote

from utils.logger import print_log
from utils.product_exception import ProductException
from django.apps import apps
from django.core.cache import cache


class EncryptDecrypt:
    __instance = None
    __key = None

    def __new__(cls, first_call=False):
        print_log.info('__new__ method of EncryptDecrypt class is getting called')
        try:
            if not first_call:
                return EncryptDecrypt.get_encrypt_decrypt_instance()
            if cls.__instance is None:
                cls.__instance = super(EncryptDecrypt, cls).__new__(cls)
                cached_key = cache.get('encryption_key', None)
                if cached_key is None:
                    cls.__instance.__key = Fernet.generate_key()
                    serialized_key = cls.__instance.__key.decode('utf-8')
                    cache.set('encryption_key', serialized_key)
                else:
                    cached_key = cache.get('encryption_key')
                    cls.__instance.__key = cached_key.encode('utf-8')

        except Exception as exp:
            raise ProductException(message=str(exp),
                                   custom_message='Error occurred at the time initializing of EncryptDecrypt class')
        finally:
            print_log.info('__new__ method of EncryptDecrypt class ends here')
            return cls.__instance

    @staticmethod
    def get_encrypt_decrypt_instance():
        userauths_config = apps.get_app_config('utils')
        encrypt_decrypt_instance = userauths_config.encrypt_decrypt_instance
        if encrypt_decrypt_instance is not None:
            print_log.info('EncryptDecrypt object got from the onload event of userauths module')
            return encrypt_decrypt_instance
        return EncryptDecrypt()

    def encrypt_parameter(self, parameter):
        print_log.info('Method encrypt_parameter of EncryptDecrypt class is getting invoked')
        encrypted_parameter = None
        try:
            cipher_suite = Fernet(self.__key)
            encrypted_parameter = cipher_suite.encrypt(parameter.encode())
        except Exception as exp:
            raise ProductException(message=str(exp),
                                   custom_message='Error occurred while encryption')
        finally:
            print_log.info('Method call of encrypt_parameter of EncryptDecrypt class ends here')
            if encrypted_parameter is not None:
                return quote(encrypted_parameter)
            else:
                return None

    def decrypt_parameter(self, encrypted_parameter):
        print_log.info('Method decrypt_parameter of EncryptDecrypt class is getting invoked')
        decrypted_parameter = None
        try:
            cipher_suite = Fernet(self.__key)
            decrypted_parameter = cipher_suite.decrypt(unquote(encrypted_parameter)).decode()
        except Exception as exp:
            raise ProductException(message=str(exp),
                                   custom_message='Error occurred while decryption')
        finally:
            print_log.info('Method call of decrypt_parameter of EncryptDecrypt class ends here')
            if decrypted_parameter is not None:
                return decrypted_parameter
            else:
                return None
