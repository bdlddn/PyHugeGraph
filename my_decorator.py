from decorator import decorator
from requests.exceptions import ConnectTimeout, ConnectionError, ReadTimeout


@decorator
def decorator1(func, *args, **kwargs):
    parameter_holder = args[0].get_parameter_holder()
    if parameter_holder is None or "name" not in parameter_holder.get_keys():
        print('Parameters required, please set necessary parameters.')
        raise
    return func(*args, **kwargs)


@decorator
def decorator2(func, *args, **kwargs):
    parameter_holder = args[0].get_parameter_holder()
    if parameter_holder.get_value('not_exist') is False:
        return 'Create failed, "{}" already exists.'.format(parameter_holder.get_value('name'))
    return func(*args, **kwargs)


@decorator
def do_request(func, *args, **kwargs):
    flag = True
    while flag:
        try:
            func(*args, **kwargs)
            flag = False
        except (ConnectTimeout, ConnectionError, ReadTimeout) as e:
            flag = True
        except Exception as e:
            flag = False