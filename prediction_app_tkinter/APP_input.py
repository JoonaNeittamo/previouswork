import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import os
from APP_prediction import AppPrediction

class AppInput:
    def __init__(self, root, file_path, columns, target):
        self.root = root
        self.main_window = tk.Canvas(self.root, 
                                width=500, 
                                height=500, 
                                bg='#C0FFC0')
        self.main_window.pack()

        self.file_path = file_path
        self.columns = columns
        self.target = target

        for column in self.columns:
            if column in self.target:
                self.columns.remove(column)
        
    def main(self):
        self.entry_errortext_list = []

        self.main_window.create_text(250, 25, text="INPUT", font=("Courier New", 30, "bold"))
        self.main_window.create_text(250, 60, text="Enter your information", font=("Courier New", 15))

        self.create_userinput_box(self.columns)

        self.choose_inputboxes = tk.Button(self.main_window,
                                          text="USE",
                                          command=self.use_entry_inputs,
                                          width=8, height=4)
        self.choose_inputboxes.place(x=225,y=430)
        
        self.root.mainloop()  

    # Create the input boxes where user inputs numbers to their chosen columns
    def create_userinput_box(self, amount):
        x_text=205
        y_text=160
        x_entry=255
        y_entry=150

        self.entry_list = []

        for i in range(0,len(amount)):
            self.main_window.create_text(x_text, y_text, text=f"{amount[i]}:", font=("Courier New", 10, "bold"))

            self.entry = tk.Entry(self.main_window)
            self.entry.place(x=x_entry,y=y_entry)
            self.entry_list.append(self.entry)

            y_text+=30
            y_entry+=30

    def use_entry_inputs(self):
        self.predictor_inputs = [] # Way to clear the list if user presses the button again

        # Delete previous errors texts caused by missing inputs
        for errortext in self.entry_errortext_list:
            self.main_window.delete(errortext)

        lpc = 0
        y_error=320
        acceptable_entries = True
        for entry in self.entry_list:
            entry_text = entry.get()
            if entry_text == '':
                self.errortext_inputmissing = self.main_window.create_text(250,y_error, text=f"Error: {self.columns[lpc]} not specified.", font=("Courier New", 10))
                self.entry_errortext_list.append(self.errortext_inputmissing)
                y_error+=25
                acceptable_entries = False
            else:
                self.predictor_inputs.append(entry_text)
            lpc+=1

        # If entries are acceptable, add buttons to accept or decline choices
        if acceptable_entries == True:
            # Destroy to make room for 2 other buttons
            self.choose_inputboxes.destroy()

            image = Image.open("images/accept_button.png")
            image = image.resize((60, 60))
            self.accept_button_image = ImageTk.PhotoImage(image)
            self.accept_button = tk.Button(self.main_window,
                                        image=self.accept_button_image,
                                        command=self.click_accept,
                                        width=60, height=60)
            
            image = Image.open("images\decline_button.png")
            image = image.resize((60, 60))
            self.decline_button_image = ImageTk.PhotoImage(image)
            self.decline_button = tk.Button(self.main_window,
                                        image=self.decline_button_image,
                                        command=self.click_decline,
                                        width=60, height=60)
            
            self.accept_button.place(x=255,y=300)
            self.decline_button.place(x=185,y=300)

        else:
            pass
            
    def click_accept(self):
        self.main_window.destroy()
        app_prediction_instance = AppPrediction(self.root, self.file_path, self.predictor_inputs, self.columns, self.target)
        app_prediction_instance.main()

    def click_decline(self):
        self.accept_button.destroy()
        self.decline_button.destroy()
        self.main()
                 