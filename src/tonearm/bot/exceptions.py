from tonearm.utils import Translatable


class TranslatableException(Exception, Translatable):
    def __init__(self, msgid: str, /, **kwargs):
        Exception.__init__(self, msgid.format(**kwargs))
        Translatable.__init__(self, msgid, **kwargs)
