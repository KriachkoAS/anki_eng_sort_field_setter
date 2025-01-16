from aqt.utils import showInfo
import aqt

from .learning_priority_estimators import learning_priority_estimators
from .number_of_definitions_estimators import number_of_definitions_estimators


def assert_config(config) -> bool:
    attributes = {
        'note_type': str,
        'deck': str,
        'number_of_known_words': int,
        'word_field': str,
        'learning_priority_estimator': str,
        'number_of_definitions_estimator': str,
        'definitions_field': str,
        'sort_field': str,
    }
    for attribute, dtype in attributes.items():
        if attribute not in config:
            showInfo('Error: Attribute "{}" not specified'.format(attribute))
            return False
        if not isinstance(config[attribute], dtype):
            showInfo('Error: Attribute "{}" need to be appropriate format ({}) (current format is {})'.format(attribute, dtype, type(config[attribute])))
            return False
    note_type = aqt.mw.col.models.by_name(config['note_type'])
    if note_type is None:
        showInfo('Error: note_type need to be existing note type'.format(attribute, dtype))
        return False
    note_type_filed_names = set([fld['name'] for fld in note_type['flds']])
    for field_name in ['word_field', 'definitions_field', 'sort_field', ]:
        if config[field_name] not in note_type_filed_names:
            showInfo('Error: Attribute "{}" need to represent existing field of note_type. Existing fields: {}'.format(field_name, note_type_filed_names))
            return False
        
    if config['number_of_known_words'] < 0:
        showInfo('Error: number_of_known_words is less then 0')
        return False
    if config['number_of_known_words'] > 16_000:
        showInfo('Warning: number_of_known_words is greater then 16 000. 16 000 will be used as a value')
    if config['number_of_known_words'] % 100 != 0:
        showInfo('Warning: number_of_known_words is not divieded by 100. Nearest appropriate value will be used')
    
    if config['learning_priority_estimator'] not in learning_priority_estimators:
        showInfo('Error: Attribute "learning_priority_estimator" need to represent existing learning_priority_estimator. Existing estimators: {}'.format(learning_priority_estimators.keys()))
    if config['number_of_definitions_estimator'] not in number_of_definitions_estimators:
        showInfo('Error: Attribute "number_of_definitions_estimator" need to represent existing number_of_definitions_estimator. Existing estimators: {}'.format(number_of_definitions_estimators.keys()))
    
    return True