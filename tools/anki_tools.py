from anki import Collection

"""
Some useful methods

    col.decks.allNames()  show all deck names
    decks = col.decks.decks; decks.items();  show all decks
    deck = col.decks.byName(deck_name)   # return a dict
    cids = col.find_cards("deck:墨墨雅思::雅思真词汇-4&3频率")  # use query

"""
def find_cards_by_deckname(col: Collection, deck_name: str):
    """

    :param deck_name:
    :return:  a list of card ids
    """
    cids = col.find_cards("deck:{0}".format(deck_name))  # use query
    return cids


def get_note_by_cid(col:Collection, cid: int):
    """
    Get note object by card id
    :param cid: card id
    :return:
    """
    card = col.getCard(cid)
    note = col.getNote(card.nid)
    return note

def get_fieldname_by_nid(col:Collection, nid: int):
    """
    Get field names by note id
    :param col:
    :param nid: note id
    :return:
    """
    model = col.getNote(nid).model()
    fields = col.models.fieldNames(model)
    return fields

def find_notes_by_deckname(col: Collection, deck_name: str):
    """

    :param deck_name:
    :return:  a list of note ids
    """
    nids = col.find_notes("deck:{0}".format(deck_name))  # use query
    return nids