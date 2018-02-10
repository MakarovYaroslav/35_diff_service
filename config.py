class BaseConfig(object):
    CONFIG = {
        "add_class": "green",
        "add_element": "span",
        "remove_class": "red",
        "remove_element": "span",
        "moved_class": "yellow",
        "moved_element": "span",
    }
    ALLOWED_EXTENSIONS = {'.html'}


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
