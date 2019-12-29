from django.apps import AppConfig


class AcConfig(AppConfig):
    name = 'ac'


    def ready(self):
        import ac.signals

