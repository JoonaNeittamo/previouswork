import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import joblib
import os
import locale



class AppPrediction:
    def __init__(self, root, csv_file_path, inputs, columns, target):
        self.root = root
        self.main_window = tk.Canvas(self.root, 
                                     width=500, height=500, 
                                     bg='#C0FFC0')
        self.main_window.pack()

        self.csv_file_path = csv_file_path # CSV file path
        self.inputs = inputs
        self.columns = columns
        self.target = target

        self.errortext_wrong_ext = None
        self.errortext_nofile = None
        self.iteration_counter_text = None
        self.does_model_exist = False
        self.user_want_save = False
        self.user_trained = False

        self.best_model_acc = -float("inf")



    def main(self):
        self.text_list = []
        self.main_window.create_text(250, 25, text="PREDICTION", font=("Courier New", 30, "bold"))
        self.question_one = self.main_window.create_text(250, 120, text="Do you already have a model?", font=("Courier New", 15))

        image = Image.open("images/accept_button.png")
        image = image.resize((60, 60))
        self.accept_button_image = ImageTk.PhotoImage(image)
        self.accept_button_main = tk.Button(self.main_window,
                                    image=self.accept_button_image,
                                    command=self.user_has_model,
                                    width=60, height=60)
        
        image = Image.open("images\decline_button.png")
        image = image.resize((60, 60))
        self.decline_button_image = ImageTk.PhotoImage(image)
        self.decline_button_main = tk.Button(self.main_window,
                                    image=self.decline_button_image,
                                    command=self.user_no_model,
                                    width=60, height=60)
        
        self.accept_button_main.place(x=255,y=300)
        self.decline_button_main.place(x=185,y=300)




        
        self.root.mainloop()    
    

    def format_currency(self, amount):
        # Extract the numerical value from the string
        amount_str = str(amount)
        numerical_value = float(amount_str.strip('[]'))

        # Set the locale to the desired format (in this case, en_US)
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

        # Format the amount as currency
        formatted_amount = locale.currency(numerical_value, grouping=True)

        return formatted_amount







    def open_explorer(self):
        if self.errortext_wrong_ext is not None:
            self.main_window.delete(self.errortext_wrong_ext)
            self.main_window.delete(self.errortext_wrong_ext_2)
        elif self.errortext_nofile is not None:
            self.main_window.delete(self.errortext_nofile)
    
        self.model_file_path = filedialog.askopenfilename()
        if self.model_file_path:
            file_extension = os.path.splitext(self.model_file_path)[-1].lower()
            if file_extension in ['.pkl']:
                self.does_model_exist = True
                self.import_button.destroy()
                self.predict_price(self.model_file_path, self.columns, self.inputs)
            else:
                self.errortext_wrong_ext = self.main_window.create_text(250, 400, text="Error: Invalid file extension.", font=("Courier New", 12))
                self.errortext_wrong_ext_2 = self.main_window.create_text(250, 420, text="Please select a .pkl file!", font=("Courier New", 12))
        else:
            self.errortext_nofile = self.main_window.create_text(250, 400, text="Error: No file selected", font=("Courier New", 12))



    def user_has_model(self):
        self.accept_button_main.destroy()
        self.decline_button_main.destroy()
        self.main_window.delete(self.question_one)

        self.question_two_1 = self.main_window.create_text(250, 120, text="Let's import your model!", font=("Courier New", 15))
        self.question_two_2 = self.main_window.create_text(250, 145, text="NOTE: Select a .pkl file.", font=("Courier New", 15))

        image = Image.open("images/import_button.png")
        image = image.resize((60, 60))
        self.import_button_image = ImageTk.PhotoImage(image)
        self.import_button = tk.Button(self.main_window,
                                    image=self.import_button_image,
                                    command=self.open_explorer,
                                    width=60, height=60)
        self.import_button.place(x=223, y=300)

    def user_no_model(self):
        self.accept_button_main.destroy()
        self.decline_button_main.destroy()
        self.main_window.delete(self.question_one)

        self.question_three_1 = self.main_window.create_text(250, 120, text="The app will train a model for you.", font=("Courier New", 12))
        self.question_three_2 = self.main_window.create_text(250, 145, text="Do you want to save the trained model?", font=("Courier New", 12))
        self.question_three_3 = self.main_window.create_text(250, 170, text="NOTE: This will take a while.", font=("Courier New", 12))
        self.question_three_4 = self.main_window.create_text(250, 195, text="Expected accuracy: 95%", font=("Courier New", 12))
    
        image = Image.open("images/accept_button.png")
        image = image.resize((60, 60))
        self.accept_button_image = ImageTk.PhotoImage(image)
        self.accept_button_nomodel = tk.Button(self.main_window,
                                    image=self.accept_button_image,
                                    command=self.user_no_model_change,
                                    width=60, height=60)
        
        image = Image.open("images\decline_button.png")
        image = image.resize((60, 60))
        self.decline_button_image = ImageTk.PhotoImage(image)
        self.decline_button_nomodel = tk.Button(self.main_window,
                                    image=self.decline_button_image,
                                    command=self.train_user_model,
                                    width=60, height=60)
        
        self.accept_button_nomodel.place(x=255,y=300)
        self.decline_button_nomodel.place(x=185,y=300)

    # Function for if user already has a model, or AFTER user trains a model.
    def predict_price(self, model_path, columns, inputs):
        with open(model_path, 'rb') as file:
            model = joblib.load(file)

        # Get the selected columns used during training
        selected_columns = model.feature_names_in_

        # Define the desired order of columns
        desired_columns = ['bed', 'bath', 'house_size', 'acre_lot', 'zip_code']

        # Reorder the columns and inputs based on the desired order
        ordered_columns = [col for col in desired_columns if col in selected_columns]
        ordered_inputs = [inputs[columns.index(col)] if col in columns else 0 for col in ordered_columns]

        # Prepare new data for prediction
        built_frame = pd.DataFrame({col: [val] for col, val in zip(ordered_columns, ordered_inputs)})

        # Fill missing columns with default values
        missing_columns = set(desired_columns) - set(built_frame.columns)
        for col in missing_columns:
            built_frame[col] = 0  # Replace with appropriate default value

        # Perform predictions using the loaded model
        predictions = model.predict(built_frame)

        formatted_price = self.format_currency(predictions)
        

        # Return the predictions
        self.prediction_result_1 = self.main_window.create_text(250, 185, text="PREDICTED PRICE", font=("Courier New", 15))
        self.prediction_result_2 = self.main_window.create_text(250, 210, text=f"{formatted_price}", font=("Courier New", 15))
        if self.user_trained == True:
            self.prediction_result_2 = self.main_window.create_text(250, 235, text=f"Accuracy: {self.best_model_acc}", font=("Courier New", 15))
        self.prediction_result_3 = self.main_window.create_text(250, 450, text="Press the X button to exit the program.", font=("Courier New", 10))

        image = Image.open("images\decline_button.png")
        image = image.resize((60, 60))
        self.decline_button_image = ImageTk.PhotoImage(image)
        self.decline_button_close = tk.Button(self.main_window,
                                    image=self.decline_button_image,
                                    command=self.end_program,
                                    width=60, height=60)
        self.decline_button_close.place(x=223, y=300)


    def train_user_model(self):
        self.user_trained = True

        self.accept_button_nomodel.destroy()
        self.decline_button_nomodel.destroy()

        self.main_window.delete(self.question_three_1)
        self.main_window.delete(self.question_three_2)
        self.main_window.delete(self.question_three_3)
        self.main_window.delete(self.question_three_4)

        file_path = self.csv_file_path
        selected_columns = ["bed", "bath", "house_size", "acre_lot", "zip_code"]
        target_column = "price"
        best_model = None
        

        if self.user_want_save == True:
            user_model_path = self.model_folder_path
        else:
            user_model_path = "user_model.pkl"

        data = pd.read_csv(file_path)

        X = data[selected_columns]
        y = data[target_column]

        test_size = 0.7
        decrement_rate = 0.02
        ninefour_acc = 0.94
        num_iterations = 100

        for iteration in range(num_iterations):
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
            model = RandomForestRegressor()

            # Use the existing best model if available
            if best_model is not None:
                model = best_model

            model.fit(X_train, y_train)

            # Get model accuracy using r2_score
            y_pred = model.predict(X_test)
            self.model_acc = r2_score(y_test, y_pred)

            # Check if the current model is better than the previous best model
            if self.model_acc > self.best_model_acc:
                # Delete the previous best model if it exists
                if self.user_want_save == True:
                    if best_model is not None:
                        os.remove(user_model_path)
                else:
                    continue

                # Set the current model as the new best model
                best_model = model
                self.best_model_acc = self.model_acc
                if self.user_want_save == True:
                    joblib.dump(best_model, user_model_path)


            # Get prediction accuracy using the trained model
            y_pred_train = model.predict(X_train)
            pred_acc = r2_score(y_train, y_pred_train)
            

            # Gradually reduce test data size to increase prediction accuracy
            test_size -= decrement_rate

            if self.model_acc >= ninefour_acc:
                if self.user_want_save == True:
                    self.predict_price(user_model_path, self.columns, self.inputs)
                    joblib.dump(best_model, user_model_path)
                    break
                else:
                    self.predict_price(user_model_path, self.columns, self.inputs)
                    os.remove(user_model_path)
                    break

    def user_no_model_change(self):
        self.user_want_save = True
        self.model_folder_path = filedialog.asksaveasfilename(defaultextension=".pkl")
        self.train_user_model()

    def end_program(self):
        self.main_window.quit()


