import tkinter as tk
from PIL import ImageTk, Image
from APP_import import AppImport


class AppStart:
    def __init__(self):
        self.root = tk.Tk()
        self.main_window = tk.Canvas(self.root, width=500, height=500, bg='#C0FFC0')
        self.root.title("Apartmentos LTD")
        self.root.resizable(False, False)

        # First page user guiding
        self.main_window.create_text(250, 25, text="WELCOME", font=("Courier New", 30, "bold"))
        self.main_window.create_text(250, 60, text="Predictions For Your Prices", font=("Courier New", 15))
        self.main_window.create_text(250, 90, text="Press The Button To Start", font=("Courier New", 15))
        
        # Button to continue to the next window
        image = Image.open("images/start_button_up.png")
        image = image.resize((128, 64))
        self.start_button_image = ImageTk.PhotoImage(image)
        self.first_button = tk.Button(self.main_window, 
                                image=self.start_button_image,
                                command=self.start_button,
                                width=120, height=55)
        
        self.main_window.pack()
        self.first_button.place(x=190, y=300) # Place > Pack, pack messes things up


    # Function removes widgets and goes to the next window (when button pressed)
    def start_button(self):
        self.main_window.destroy()
        
        app_import_instance = AppImport(self.root)
        app_import_instance.main()

    def main(self):
        self.root.mainloop()





if __name__ == "__main__":
    app_instance = AppStart()
    app_instance.main()
