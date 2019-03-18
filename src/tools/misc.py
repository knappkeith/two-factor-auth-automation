import os


def get_environment_variable(variable_name, default=None, **kwargs):
    '''Return an environment variable from os, or default

    ``variable_name`` string of the variable name
    ``default`` will return the default
    ``kwargs`` func(**funcargs) if not found and default None
    '''
    try:
        return os.environ[variable_name]
    except KeyError:
        print("Environment Varaible '{}' not defined".format(variable_name))

    # Return Default if defined
    if default:
        return default

    # Try func(funcargs) from kwargs
    if kwargs.get('func') and callable(kwargs['func']):
        if kwargs.get('funcargs'):
            return kwargs['func'](**kwargs['funcargs'])
        else:
            return kwargs['func']()

    # Return None because nothing else worked
    return default
