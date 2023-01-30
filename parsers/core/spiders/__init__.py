class SpiderNameMixin:
    @classmethod
    def get_spidername(cls):
        return '.'.join(cls.__module__.split('.')[2:-1])
