import csv

from lib import get_sorted_note_ids_generator


def get_notes_generator(fpath):
    with open(fpath, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            yield row

get_sorted_note_ids_generator(get_notes_generator('/workspace/src/deck.csv'))