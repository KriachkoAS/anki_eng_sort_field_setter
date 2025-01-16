from aqt import mw
from aqt.qt import QAction
from aqt.utils import qconnect, showInfo

from .number_of_definitions_estimators import number_of_definitions_estimators
from .read_data import get_ffreq_data_iterator
from .learning_priority_estimators import learning_priority_estimators
from .assert_config import assert_config

from typing import NamedTuple



def escape_characters(val: str) -> str:
    return '"' + val.replace('"', '\\"') + '"' if ' ' in val else val

class NotePriorityProjection(NamedTuple):
    word: str
    priority: int

def set_sort_field():
    config = mw.addonManager.getConfig(__name__)
    if not assert_config(config):
        return

    note_priority_projections = []

    for word, ffreq, known_probability in get_ffreq_data_iterator(config['number_of_known_words']):
        notes = mw.col.find_notes('deck:{} {}:{}'.format(config['deck'], config['word_field'], word))
        if len(notes) != 1:
            continue
        note_priority_projections.append(NotePriorityProjection(
            word,
            learning_priority_estimators[config['learning_priority_estimator']](
                ffreq,
                known_probability,
                number_of_definitions_estimators[config['number_of_definitions_estimator']](mw.col.get_note(notes[0])[config['definitions_field']])
            )
        ))
    note_priority_projections.sort(key=lambda note_priority_projection: note_priority_projection.priority, reverse=True)
    for i, (word, _) in enumerate(note_priority_projections):
        notes = mw.col.find_notes('deck:{} {}:{}'.format(config['deck'], config['word_field'], word))
        if len(notes) != 1:
            continue
        note = mw.col.get_note(notes[0])
        note[config['sort_field']] = "{:6}".format(i)
        mw.col.update_note(note)



action = QAction("set sort field", mw)
qconnect(action.triggered, set_sort_field)
mw.form.menuTools.addAction(action)