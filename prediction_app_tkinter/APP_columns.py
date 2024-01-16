import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from APP_input import AppInput
import pandas as pd
import os


# Beware: This window has some incredibly horrible error check bloat
# I could have just put all of the errors into their own function
# But it was too late because I was already done
class AppColumns:
    def __init__(self, root, file_path):
        self.root = root
        self.file_path = file_path

        self.errortext_target_exists = False # Check if Error is on screen
        self.errortext_cant_continue = False
        self.error_columns_empty = True # If columns empty, cant CONTINUE
        self.error_zipcode_notselected = True # If 'zip_code' column not selected, cant CONTINUE
        
        

        
    def main(self):
        self.chosen_columns_list = []
        self.chosen_target_list = []
        self.target_exists = False # Check if target has been chosen (add_chosen_target func) 
        self.continue_error = None # If 
        
        self.dataframe = pd.read_csv(self.file_path)
        self.dataframe_columns = self.dataframe.columns.tolist()

        # Canvas not in __init__ because it needs to be reset each time
        self.canvas = tk.Canvas(self.root, 
                                width=500, 
                                height=500, 
                                bg='#C0FFC0')
        self.canvas.pack()

        self.canvas.create_text(250, 25, text="COLUMNS", font=("Courier New", 30, "bold"))
        self.canvas.create_text(250, 70, text="Choose the columns for predicting", font=("Courier New", 12))
        self.canvas.create_text(250, 90, text="NOTE: Remember to select a TARGET column!", font=("Courier New", 12, "bold"))


        ### RESET USER CHOICES (resets the whole window, kinda janky but works!)
        self.reset_button = tk.Button(self.root,
                                      text="RESET",
                                      command=self.reset_columns,
                                      width=6, height=3)
        
        ### SET CHOSEN COLUMN AS THE TARGET FOR PREDICTING
        self.target_button = tk.Button(self.root,
                                    text="TARGET",
                                    command=self.add_chosen_target,
                                    width=6, height=3)

        ### SET CHOSEN COLUMN INTO ENTRIES USER WILL INPUT
        self.add_button = tk.Button(self.root,
                                    text="ADD",
                                    command=self.add_chosen_columns,
                                    width=6, height=3)

        ### CONTINUE WITH CHOSEN COLUMNS
        self.continue_button = tk.Button(self.root,
                                    text="CONTINUE",
                                    command=self.continue_button_function,
                                    width=6, height=3)

        self.reset_button.place(x=5,y=443)
        self.target_button.place(x=225,y=443)
        self.add_button.place(x=445,y=443)
        self.continue_button.place(x=5,y=5)

        self.current_option = tk.StringVar(self.root)
        self.dropdown_menu = tk.OptionMenu(self.root,
                                           self.current_option,
                                           *self.dataframe_columns)
        
        self.dropdown_menu.place(x=100,y=100)

        self.root.mainloop()

    # Dropdown menu option into predictors
    def add_chosen_columns(self):
        if self.errortext_target_exists == True: # Incase error text already exists
            self.canvas.delete(self.target_error1, self.target_error2)
            self.errortext_target_exists = False

        if self.current_option.get() == '':
            pass
        else:
            selected_option_dropdown = self.current_option.get()
            self.chosen_columns_list.append(selected_option_dropdown)
            self.chosen_columns_list = list(set(self.chosen_columns_list)) # Remove duplicates    
            self.error_columns_empty = False      
            if 'zip_code' in self.chosen_columns_list:
                self.error_zipcode_notselected = False
            else:
                pass

    # Takes dropdown menu choice and makes it the target, target will be the one predicted
    def add_chosen_target(self):
        if self.errortext_target_exists == True: # Incase error text already exists
                self.canvas.delete(self.target_error1, self.target_error2)
                self.errortext_target_exists = False

        elif self.errortext_cant_continue == True: # Incase error text already exists
            self.canvas.delete(self.continue_error1, self.continue_error2, self.continue_error3)
            self.errortext_cant_continue = False

        if self.current_option.get() == '': # Incase user hasnt selected anything but presses the button
            pass
        else:
            if self.target_exists == False:
                selected_option_dropdown = self.current_option.get()
                self.chosen_target_list.append(selected_option_dropdown)
                self.target_exists = True
            else:
                self.target_error1 = self.canvas.create_text(250, 300, text="Error: You have already selected a target column", font=("Courier New", 12))
                self.target_error2 = self.canvas.create_text(250, 320, text="Press RESET to reset your choices", font=("Courier New", 12))
                self.errortext_target_exists = True # Error text now exists, thus IF clause will trigger

    # Continue to the next window, 
    def continue_button_function(self):
        if self.errortext_target_exists == True: # Incase error text already exists
            self.canvas.delete(self.target_error1, self.target_error2)
            self.errortext_target_exists = False
        
        if self.errortext_cant_continue == True: # Incase error text already exists
            self.canvas.delete(self.continue_error1, self.continue_error2, self.continue_error3)
            self.errortext_cant_continue = False
            

        if self.error_zipcode_notselected == False and self.error_columns_empty == False and self.target_exists == True:    
            self.canvas.destroy()
            app_prediction_instance = AppInput(self.root, self.file_path, self.chosen_columns_list, self.chosen_target_list)
            app_prediction_instance.main()
        else:
            self.continue_error1 = self.canvas.create_text(250, 300, text="Error: You havent selected a target", font=("Courier New", 12))
            self.continue_error2 = self.canvas.create_text(250, 320, text="and choose atleast zipcode to columns", font=("Courier New", 12))
            self.continue_error3 = self.canvas.create_text(250, 340, text="Press RESET to reset your choices", font=("Courier New", 12))
            self.errortext_cant_continue = True


    def reset_columns(self):
        self.canvas.destroy()
        self.main()

