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

nids = find_notes_by_deckname(col, deck_name)
note_count = len(nids)
print("Note count: ", note_count)

# the first card
note = col.getNote(nids[0])
print("First note id: ", note.id)

# get the field names
# print("Fields", note.fields)
fields = list(note._fmap.keys())
print("fields", fields)

# read notes
notes = [col.getNote(id) for id in nids]
# read first note

note = notes[0]
print("First note: ", note[fields[1]], note)


# write note
print(note[fields[1]], fields[1])
note[fields[1]] += "hello"
print(note[fields[1]])
note.flush()
col.close()





