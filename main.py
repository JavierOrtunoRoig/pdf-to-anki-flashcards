from tkinter import filedialog, messagebox
import pdf_processing
import anki_generator
import gui

pdf_path = None


def upload_pdf():
  global pdf_path
  pdf_path = filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF Files", "*.pdf")])
  if pdf_path:
    gui.file_label.config(text=f"Selected file: {pdf_path}")
  return pdf_path


def save_file():
  if not pdf_path:
    messagebox.showwarning("Warning", "Please upload a PDF file first.")
    return

  file_name = gui.name_entry.get()
  new_file_path = filedialog.askdirectory(title="Select Destination Folder")

  if new_file_path and file_name:
    full_path = f"{new_file_path}/{file_name}.apkg"

    cloze_cards, writing_cards = pdf_processing.extract_highlights_from_pdf(pdf_path)
    anki_generator.generate_anki_deck(cloze_cards, writing_cards, full_path)

    messagebox.showinfo("File Saved", f"The file was saved at: {full_path}")
  else:
    messagebox.showwarning("Warning", "Please select a folder and provide a file name.")


# Inicializar la interfaz gráfica
gui.create_main_window(upload_pdf, save_file)
