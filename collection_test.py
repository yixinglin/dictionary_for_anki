from tools.anki_tools import *
from anki import Collection
col = Collection("C:\\Users\\Yixing Lin\\AppData\\Roaming\\Anki2\\用户1\\collection.anki2")

# 牌组名字，desk, 雅思5-6分，墨墨雅思，雅思真词汇-4&3频率
# 字段名字

print(col.decks.allNames())  #show all deck names
# decks = col.decks.decks
# print(decks.items())  # show all decks
#


# deck_name = "墨墨雅思::雅思真词汇-4&3频率"
deck_name = "英语句型/语法"

decknames = col.decks.allNames()
print("This is a valid deck name? ", deck_name in decknames)
print("Deck name: ", deck_name)

cids = find_cards_by_deckname(col, deck_name)
card_count = len(cids)
print("Card count: ", card_count)

# the first card
card = col.getCard(cids[0])
print("First card id: ", card.nid)

# get the field names
model = col.getNote(card.nid).model()
fields = col.models.fieldNames(model)
print("Fields", fields)

# read notes
notes = []
for cid in cids:
    note = get_note_by_cid(col, cid)
    notes.append(note)

# read first note

# note = notes[0]
note = col.getNote(1565094328757)
print("First note: ", note[fields[1]], note)


# write note
print(note[fields[1]], fields[1])
note[fields[1]] += "hello"
print(note[fields[1]])
note.flush()
col.close()





