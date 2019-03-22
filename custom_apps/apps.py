import os, django

script_path = os.path.dirname(os.path.realpath(__file__))
def get_app_names():
    print ([(f[:2], f[-2:]) for f in os.listdir(script_path)])
    return [f for f in os.listdir(script_path) if os.path.isdir(os.path.join(script_path,f)) and not (f[:2] == '__' and f[-2:] == '__')]


def get_custom_apps():
    return ['custom_apps.' + x for x in get_app_names()]
