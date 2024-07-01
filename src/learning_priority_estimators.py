learning_priority_estimators = {}


def onetime_func():
    add_learning_priority_estimator = lambda f: learning_priority_estimators.setdefault(f.__name__, f)

    @add_learning_priority_estimator
    def linear_nuber_of_definitions_impact_learn_all(ffreq: float, known_probability: float, number_of_definitions: int):
        return ffreq * (1 - known_probability) / number_of_definitions


onetime_func()
del onetime_func