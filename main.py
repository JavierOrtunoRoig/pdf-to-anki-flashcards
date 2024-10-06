import fitz  # PyMuPDF
import genanki
from anki import anki_model
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import font as tkFont


pdf_path = None


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
  iteration = 1

  for green_text in green_annotations.copy():  # Copy to avoid modifying while iterating
    if green_text in yellow_text:
      yellow_text = yellow_text.replace(green_text, f"{{{{c{iteration}::{green_text}}}}}")
      used_greens.append(green_text)  # Store the green parts used in this card
      green_annotations.remove(green_text)  # Remove the used green annotation
      applied_cloze = True
      iteration += 1

  return yellow_text if applied_cloze else None, used_greens


def apply_writing_card(blue_text, green_annotations):
  """Generates a writing card if the blue text contains green parts."""
  applied_writing = False  # To track if any writing card is applied
  used_greens = []  # Store the green parts used in this card
  iteration = 1

  for green_text in green_annotations.copy():  # Copy to avoid modifying while iterating
    if green_text in blue_text:
      blue_text = blue_text.replace(green_text, f"{{{{c{iteration}::{green_text}}}}}")
      used_greens.append(green_text)  # Store the green parts used in this card
      green_annotations.remove(green_text)  # Remove the used green annotation
      applied_writing = True
      iteration += 1

  return f"Write: {blue_text}" if applied_writing else None, used_greens


def upload_pdf():
  global pdf_path  # Use the global variable to store the file path
  pdf_path = filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF Files", "*.pdf")])
  if pdf_path:
    file_label.config(text=f"Selected file: {pdf_path}")
  return pdf_path


def save_file():
  if not pdf_path:
    messagebox.showwarning("Warning", "Please upload a PDF file first.")
    return

  file_name = name_entry.get()
  new_file_path = filedialog.askdirectory(title="Select Destination Folder")

  if new_file_path and file_name:
    full_path = f"{new_file_path}/{file_name}.apkg"

    cloze_cards, writing_cards = extract_highlights_from_pdf(pdf_path)

    anki_deck = genanki.Deck(
      2059400111,  # ID único del mazo
      "Cloze Deck with Notes",
    )

    # Formatting the output
    for cloze_card, green_texts in cloze_cards:
      card = genanki.Note(model=anki_model, fields=[cloze_card, "", ""])
      anki_deck.add_note(card)

    genanki.Package(anki_deck).write_to_file(full_path)

    messagebox.showinfo("File Saved", f"The file will be saved at: {full_path}")
    # Here you can use pdf_path and full_path to work with the files
    # Example: generate or manipulate files
  else:
    messagebox.showwarning("Warning", "Please select a folder and provide a file name.")


# Create main window
window = tk.Tk()
window.title("PDF to Anki Flashcards")
window.geometry("600x250")
window.configure(bg="#f0f4f5")  # Light background color

# Custom fonts
title_font = tkFont.Font(family="Helvetica", size=14, weight="bold")
label_font = tkFont.Font(family="Helvetica", size=10)

# Title label
title_label = tk.Label(window, text="PDF to Anki Flashcards", font=title_font, bg="#f0f4f5")
title_label.pack(pady=10)

# Button to upload PDF file
upload_button = tk.Button(window, text="Select PDF File", command=upload_pdf, bg="#4CAF50", fg="white", width=20)
upload_button.pack(pady=10)

# Label to show selected file
file_label = tk.Label(window, text="No file selected.", font=label_font, bg="#f0f4f5")
file_label.pack(pady=5)

# Field to enter the generated file name
name_label = tk.Label(window, text="Enter name for .apkg file:", font=label_font, bg="#f0f4f5")
name_label.pack(pady=5)

name_entry = tk.Entry(window, width=40)
name_entry.pack(pady=5)

# Button to save file
save_button = tk.Button(
  window, text="Generate and Save Anki Deck", command=save_file, bg="#2196F3", fg="white", width=25
)
save_button.pack(pady=10)

# Run the application
window.mainloop()
