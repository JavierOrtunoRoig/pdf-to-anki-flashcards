import genanki

# Definir el modelo de la tarjeta Anki utilizando la sintaxis cloze correctamente
anki_model = genanki.Model(
  1607392319,  # ID único del modelo
  "Cloze Model with Notes from PDF",
  fields=[{"name": "Questions"}, {"name": "Answers"}, {"name": "Notes"}],
  templates=[
    {
      "name": "Card 1",
      "qfmt": """
          <div class="note">
              <div class="front full-redounded">
                  <div class="question row center">
                      {{cloze:Questions}}
                  </div>
              </div>
          </div>
      """,
      "afmt": """
        <div class="note">
          <div class="front full-redounded">
              <div class="question row center">
                  {{cloze:Questions}}
              </div>
          </div>
        </div>

        <br>
        <br>

        <div style="display:flex; flex-direction: column; gap: 2em; justify-content: center; align-items: center">

            {{#Notes}}
                <div class="note">
                    <div class="back full-redounded center">
                    <div class="row">{{Notes}}</div>
                    </div>
                </div>
            {{/Notes}}

        </div>
      """,
    }
  ],
  css="""
    /* BODY */
html, body {
    background-color: black !important;
    margin: 0 !important;
    padding: 0;
    height: 100%;
    width: 100%;
    max-height: 100vh;
    max-width: 100vw;
    font-family: San Francisco, "Noto Sans KR", Helvetica, Arial;
    font-weight: 400;
    font-size: 24px;
    word-break: keep-all;
    text-align: left;
    overflow: auto;
}

.question span.cloze {
	color: powderblue;
}

.center {
	text-align: center
}

.flex-center {
	display: flex;
	justify-content: center;
}

.full-redounded {
    border-radius: 1em !important
}

/* CARD */
.note {
    border-radius: 1em;
    margin: 0 auto;
    width: 100%;
    box-sizing: border-box;
    padding: 0 2vh; 
    max-width: 55em;
}

.front, .back {
    padding: 1em 2em; 
    backdrop-filter: blur(10px);
    overflow: auto;
    box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
    margin: 1em; 
}

.front {
    line-height: 1.5;
    background-color: rgb(25, 26, 28);
    color: rgb(255, 255, 255);
    border-top-left-radius: 1.2em;
    border-top-right-radius: 1.2em;
    border-bottom-left-radius: 0; 
    border-bottom-right-radius: 0; 
    margin-bottom: 0; 
    border-bottom: none; 
}

.back {
    line-height: 1.5;
    background-color: rgb(35, 36, 41);
    color: rgb(255, 255, 255);
    border-top-left-radius: 0;
    border-top-right-radius: 0; 
    border-bottom-left-radius: 1.2em;
    border-bottom-right-radius: 1.2em;
    margin-top: -1em; 
    border-top: none; 
}

.row {
    padding: 0 0 0 0;
}

.row input {
	border-radius: 8px;
	border: none;
	padding: 6px;
}

/* TAGS */
.tags {
    margin-bottom: 0em;
}

.tag {
    font-size: 0.8em;
    padding: .4em .8em;
    display: inline-block;
    border-radius: 1.5em;
    border: 1.5px solid rgb(78, 78, 84);
    margin: .5em .5em .5em 0;
    color: rgb(109, 199, 255);
}

/* IMAGES */
img {
    object-fit: contain;
    margin: 0 auto;
    height: auto;
    width: auto;
    max-width: 100%;
}

/* ANKI TEMPLATE WIZARDRY */
.backtemplate .backonly {
    display: block;
}
""",
)

# Crear un mazo de Anki
# anki_deck = genanki.Deck(
#   2059400110,  # ID único del mazo
#   "Cloze Deck with Notes",
# )

# Crear algunas tarjetas de ejemplo
card_1 = genanki.Note(
  model=anki_model,
  fields=["This is the cloze {{c1::sentence}}", "This is the full sentence.", "Optional note for card 1"],
)

card_2 = genanki.Note(model=anki_model, fields=["Another cloze {{c1::example}}", "Another full sentence.", ""])

# Añadir las tarjetas al mazo
# anki_deck.add_note(card_1)
# anki_deck.add_note(card_2)

# Guardar el mazo en un archivo .apkg
# genanki.Package(anki_deck).write_to_file("output_deck.apkg")

# print("Anki deck created and saved as 'output_deck.apkg'")
