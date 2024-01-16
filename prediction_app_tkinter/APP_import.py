import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from APP_columns import AppColumns
import os

class AppImport:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(self.root, 
                                width=500, 
                                height=500, 
                                bg='#C0FFC0')
        self.canvas.pack()

        # Create the variable so you can have a check for it before it exists
        self.error_nofile = None
        self.error_notcsv = None
        self.file_path = None

        

        
    def main(self):
        
        self.canvas.create_text(250, 25, text="IMPORT", font=("Courier New", 30, "bold"))
        self.canvas.create_text(250, 70, text="Let's start by importing your CSV file", font=("Courier New", 12, "bold"))
        self.canvas.create_text(250, 90, text="NOTE: Remember to select a CSV file!", font=("Courier New", 12))

        
        image = Image.open("images\import_button.png")
        image = image.resize((60, 60))
        import_button_image = ImageTk.PhotoImage(image)
        self.import_button = tk.Button(self.canvas,
                                       image=import_button_image,
                                       command=self.import_button_click,
                                       width=60, height=60)
        
        self.import_button.place(x=223, y=300)

        self.root.mainloop()
    
    def import_button_click(self):

        # Problem: What is the best way to remove error text to not make them stackable?
        # Solution: Remove the error message when the button IS PRESSED... crazy.
        if self.error_notcsv is not None:
                self.canvas.delete(self.error_notcsv)
                self.error_notcsv = None
        if self.error_nofile is not None:
                self.canvas.delete(self.error_nofile)
                self.error_nofile = None

        self.file_path = filedialog.askopenfilename()

        if self.file_path:
            if self.file_path.lower().endswith(".csv"): 
                # Variable for only the filename
                self.filename = os.path.splitext(os.path.basename(self.file_path))[0]
                self.change_button_toacceptdecline()
            else:

                self.error_notcsv = self.canvas.create_text(250, 450, text="Error: The selected file is not a CSV file.", font=("Courier New", 10, "bold"))
        else:
            self.error_nofile = self.canvas.create_text(250, 450, text="Error: No file selected.", font=("Courier New", 10, "bold"))

    def change_button_toacceptdecline(self):    
        # Destroy to make room for 2 other buttons
        self.import_button.destroy()

        image = Image.open("images/accept_button.png")
        image = image.resize((60, 60))
        self.accept_button_image = ImageTk.PhotoImage(image)
        self.accept_button = tk.Button(self.canvas,
                                       image=self.accept_button_image,
                                       command=self.click_accept,
                                       width=60, height=60)

        image = Image.open("images\decline_button.png")
        image = image.resize((60, 60))
        self.decline_button_image = ImageTk.PhotoImage(image)
        self.decline_button = tk.Button(self.canvas,
                                       image=self.decline_button_image,
                                       command=self.click_decline,
                                       width=60, height=60)
        self.accept_button.place(x=255,y=300)
        self.decline_button.place(x=185,y=300)
        
        

        self.selected1 = self.canvas.create_text(250, 380, text="Do you want to use this file?", font=("Courier New", 12))
        self.selected2 = self.canvas.create_text(250, 405, text="You have selected:", font=("Courier New", 12))
        self.selected3 = self.canvas.create_text(250, 430, text=f"{self.filename}", font=("Courier New", 12, "bold"))

        
        
    # If user accepts chosen CSV, clear the window and move to APP_columns.py
    def click_accept(self):
        self.canvas.destroy()
        
        app_prediction_instance = AppColumns(self.root, self.file_path)
        app_prediction_instance.main()

    def click_decline(self):
        self.canvas.delete(self.selected1, self.selected2, self.selected3)
        self.accept_button.destroy()
        self.decline_button.destroy()
        self.main()

        