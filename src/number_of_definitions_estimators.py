number_of_definitions_estimators = {}


def onetime_func():
    import re
    add_number_of_definitions_estimator = lambda f: number_of_definitions_estimators.setdefault(f.__name__, f)

    @add_number_of_definitions_estimator
    def slovaronline(definitions: str, expression = re.compile(r'(<br/>|<br>)(<b>)?(I(I|V|X)+|VI*|X(V)?I*)(</b>)?(<br/>|<br>|\s)|(<br/>|<br>)(<b>)?([0-9][0-9]+|[02-9])\.|(<br/>|<br>)([0-9][0-9]+|[02-9])\)')):
        return 1 + len(list(re.finditer(expression, definitions)))


onetime_func()
del onetime_func