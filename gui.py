import tkinter as tk
from tkinter import font as tkFont


def create_main_window(upload_pdf_callback, save_file_callback):
  window = tk.Tk()
  window.title("PDF to Anki Flashcards")
  window.geometry("600x250")
  window.configure(bg="#f0f4f5")

  title_font = tkFont.Font(family="Helvetica", size=14, weight="bold")
  label_font = tkFont.Font(family="Helvetica", size=10)

  title_label = tk.Label(window, text="PDF to Anki Flashcards", font=title_font, bg="#f0f4f5")
  title_label.pack(pady=10)

  upload_button = tk.Button(
    window, text="Select PDF File", command=upload_pdf_callback, bg="#4CAF50", fg="white", width=20
  )
  upload_button.pack(pady=10)

  global file_label
  file_label = tk.Label(window, text="No file selected.", font=label_font, bg="#f0f4f5")
  file_label.pack(pady=5)

  name_label = tk.Label(window, text="Enter name for .apkg file:", font=label_font, bg="#f0f4f5")
  name_label.pack(pady=5)

  global name_entry
  name_entry = tk.Entry(window, width=40)
  name_entry.pack(pady=5)

  save_button = tk.Button(
    window, text="Generate and Save Anki Deck", command=save_file_callback, bg="#2196F3", fg="white", width=25
  )
  save_button.pack(pady=10)

  window.mainloop()
