import fitz  # PyMuPDF


def extract_highlights_from_pdf(pdf_path):
  """Extrae los subrayados de un archivo PDF y clasifica el texto por color."""
  doc = fitz.open(pdf_path)

  cloze_cards = []
  writing_cards = []

  for page_num in range(doc.page_count):
    page = doc[page_num]
    annotations_by_color = process_page_annotations(page)

    # Proceso de las tarjetas Cloze
    if annotations_by_color["yellow"]:
      green_annotations_for_cloze = annotations_by_color["green"].copy()  # Copiamos para evitar problemas
      for yellow_text in annotations_by_color["yellow"]:
        cloze_applied_text, used_greens = apply_cloze_to_text(yellow_text, green_annotations_for_cloze)
        if cloze_applied_text:
          cloze_cards.append((cloze_applied_text, used_greens))  # Asociar con las partes verdes usadas

    # Proceso de las tarjetas de escritura
    if annotations_by_color["blue"]:
      green_annotations_for_writing = annotations_by_color["green"].copy()  # Copiamos para evitar problemas
      for blue_text in annotations_by_color["blue"]:
        writing_applied_text, used_greens = apply_writing_card(blue_text, green_annotations_for_writing)
        if writing_applied_text:
          writing_cards.append((writing_applied_text, used_greens))  # Asociar con las partes verdes usadas

  return cloze_cards, writing_cards


def process_page_annotations(page):
  """Procesa las anotaciones de subrayado en una página y las clasifica por color."""
  annotations_by_color = {"green": [], "yellow": [], "blue": []}

  for annot in page.annots():
    if annot.type[0] == 8:  # Resalto/Subrayado
      color = annot.colors["stroke"]
      quads = annot.vertices
      subrayado_texto = extract_highlighted_text(page, quads)
      classify_annotation_by_color(subrayado_texto, color, annotations_by_color)

  return annotations_by_color


def extract_highlighted_text(page, quads):
  """Extrae el texto subrayado de los quads en una página."""
  subrayado_texto = ""

  for i in range(0, len(quads), 4):
    rect = fitz.Rect(quads[i][0], quads[i][1], quads[i + 3][0], quads[i + 3][1])
    subrayado_texto += page.get_text("text", clip=rect).strip() + " "

  return subrayado_texto.strip()


def classify_annotation_by_color(text, color, annotations_by_color):
  """Clasifica las anotaciones de subrayado por color."""
  r, g, b = color[0], color[1], color[2]

  is_green = r < 0.5 and g > 0.9 and b < 0.5
  is_yellow = r > 0.9 and g > 0.9 and b < 0.5
  is_blue = r < 0.6 and g > 0.5 and b > 0.9  # Detectamos si el color es azul

  if is_green:
    annotations_by_color["green"].append(text)
  elif is_yellow:
    annotations_by_color["yellow"].append(text)
  elif is_blue:
    annotations_by_color["blue"].append(text)


def apply_cloze_to_text(yellow_text, green_annotations):
  """Aplica las anotaciones de cloze (verde) dentro del texto amarillo dado y registra las partes en verde."""
  applied_cloze = False  # Para controlar si aplicamos algún cloze
  used_greens = []  # Almacenar las partes verdes usadas en esta tarjeta

  for green_text in green_annotations.copy():  # Hacemos copia para evitar modificar mientras iteramos
    if green_text in yellow_text:
      yellow_text = yellow_text.replace(green_text, f"{{{{c1::{green_text}}}}}")
      used_greens.append(green_text)  # Guardamos las partes verdes usadas en esta tarjeta
      green_annotations.remove(green_text)  # Eliminamos la anotación verde ya usada
      applied_cloze = True

  return yellow_text if applied_cloze else None, used_greens


def apply_writing_card(blue_text, green_annotations):
  """Genera una tarjeta de escritura si el texto azul contiene partes verdes."""
  applied_writing = False  # Para controlar si aplicamos alguna escritura
  used_greens = []  # Almacenar las partes verdes usadas en esta tarjeta

  for green_text in green_annotations.copy():  # Hacemos copia para evitar modificar mientras iteramos
    if green_text in blue_text:
      # Aquí podemos crear una instrucción para que el usuario escriba el texto verde
      blue_text = blue_text.replace(green_text, f"{{{{c1::{green_text}}}}}")
      used_greens.append(green_text)  # Guardamos las partes verdes usadas en esta tarjeta
      green_annotations.remove(green_text)  # Eliminamos la anotación verde ya usada
      applied_writing = True

  return f"Escribe: {blue_text}" if applied_writing else None, used_greens


# Función principal
def main(pdf_path):
  cloze_cards, writing_cards = extract_highlights_from_pdf(pdf_path)

  # Formateamos el output
  print("\nCloze Cards:")
  for cloze_card, green_texts in cloze_cards:
    print(f"{cloze_card} | Partes en verde: {green_texts}")

  print("\nWriting Cards:")
  for writing_card, green_texts in writing_cards:
    print(f"{writing_card} | Partes en verde: {green_texts}")


# Ejecutar el programa con el archivo PDF
pdf_file = "./Francés para dummies.pdf"
main(pdf_file)
