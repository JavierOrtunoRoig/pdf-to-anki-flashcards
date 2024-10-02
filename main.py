import fitz  # PyMuPDF


def extract_highlights_from_pdf(pdf_path):
  """Extracts highlights from a PDF file and classifies the text by color."""
  doc = fitz.open(pdf_path)

  cloze_cards = []
  writing_cards = []

  for page_num in range(doc.page_count):
    page = doc[page_num]
    annotations_by_color = process_page_annotations(page)

    # Cloze card processing
    if annotations_by_color["yellow"]:
      green_annotations_for_cloze = annotations_by_color["green"].copy()  # Copy to avoid issues
      for yellow_text in annotations_by_color["yellow"]:
        cloze_applied_text, used_greens = apply_cloze_to_text(yellow_text, green_annotations_for_cloze)
        if cloze_applied_text:
          cloze_cards.append((cloze_applied_text, used_greens))  # Associate with used green parts

    # Writing card processing
    if annotations_by_color["blue"]:
      green_annotations_for_writing = annotations_by_color["green"].copy()  # Copy to avoid issues
      for blue_text in annotations_by_color["blue"]:
        writing_applied_text, used_greens = apply_writing_card(blue_text, green_annotations_for_writing)
        if writing_applied_text:
          writing_cards.append((writing_applied_text, used_greens))  # Associate with used green parts

  return cloze_cards, writing_cards


def process_page_annotations(page):
  """Processes the highlights on a page and classifies the text by color."""
  annotations_by_color = {"green": [], "yellow": [], "blue": []}

  for annot in page.annots():
    if annot.type[0] == 8:  # Highlight
      color = annot.colors["stroke"]
      quads = annot.vertices
      highlighted_text = extract_highlighted_text(page, quads)
      classify_annotation_by_color(highlighted_text, color, annotations_by_color)

  return annotations_by_color


def extract_highlighted_text(page, quads):
  """Extracts the highlighted text from the quads on a page."""
  highlighted_text = ""

  for i in range(0, len(quads), 4):
    rect = fitz.Rect(quads[i][0], quads[i][1], quads[i + 3][0], quads[i + 3][1])
    highlighted_text += page.get_text("text", clip=rect).strip() + " "

  return highlighted_text.strip()


def classify_annotation_by_color(text, color, annotations_by_color):
  """Classifies highlight annotations by color."""
  r, g, b = color[0], color[1], color[2]

  is_green = r < 0.5 and g > 0.9 and b < 0.5
  is_yellow = r > 0.9 and g > 0.9 and b < 0.5
  is_blue = r < 0.6 and g > 0.5 and b > 0.9  # Detect if the color is blue

  if is_green:
    annotations_by_color["green"].append(text)
  elif is_yellow:
    annotations_by_color["yellow"].append(text)
  elif is_blue:
    annotations_by_color["blue"].append(text)


def apply_cloze_to_text(yellow_text, green_annotations):
  """Applies the green (cloze) annotations within the yellow text and records the green parts used."""
  applied_cloze = False  # To track if any cloze is applied
  used_greens = []  # Store the green parts used in this card

  for green_text in green_annotations.copy():  # Copy to avoid modifying while iterating
    if green_text in yellow_text:
      yellow_text = yellow_text.replace(green_text, f"{{{{c1::{green_text}}}}}")
      used_greens.append(green_text)  # Store the green parts used in this card
      green_annotations.remove(green_text)  # Remove the used green annotation
      applied_cloze = True

  return yellow_text if applied_cloze else None, used_greens


def apply_writing_card(blue_text, green_annotations):
  """Generates a writing card if the blue text contains green parts."""
  applied_writing = False  # To track if any writing card is applied
  used_greens = []  # Store the green parts used in this card

  for green_text in green_annotations.copy():  # Copy to avoid modifying while iterating
    if green_text in blue_text:
      # Here we can create an instruction for the user to write the green text
      blue_text = blue_text.replace(green_text, f"{{{{c1::{green_text}}}}}")
      used_greens.append(green_text)  # Store the green parts used in this card
      green_annotations.remove(green_text)  # Remove the used green annotation
      applied_writing = True

  return f"Write: {blue_text}" if applied_writing else None, used_greens


pdf_path = "./Francés para dummies.pdf"
cloze_cards, writing_cards = extract_highlights_from_pdf(pdf_path)

# Formatting the output
print("\nCloze Cards:")
for cloze_card, green_texts in cloze_cards:
  print(f"{cloze_card} | Green parts: {green_texts}")

print("\nWriting Cards:")
for writing_card, green_texts in writing_cards:
  print(f"{writing_card} | Green parts: {green_texts}")
