import genanki
from anki import anki_model


def generate_anki_deck(cloze_cards, writing_cards, output_path):
  anki_deck = genanki.Deck(
    2059400111,  # ID único del mazo
    "Cloze Deck with Notes",
  )

  for cloze_card, green_texts in cloze_cards:
    card = genanki.Note(model=anki_model, fields=[cloze_card, "", ""])
    anki_deck.add_note(card)

  genanki.Package(anki_deck).write_to_file(output_path)
