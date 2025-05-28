import argparse
import os

class EnvDefault(argparse.Action):
    def __init__(self, env_var, required=True, default=None, **kwargs):
        if env_var and env_var in os.environ:
            default = os.environ[env_var]
        if required and default:
            required = False
        super(EnvDefault, self).__init__(default=default, required=required, **kwargs)

    def __call__(self, parse, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)