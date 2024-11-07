import customtkinter as ctk
import json

# Create a class for the settings
class Settings(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Settings")
        self.geometry("800x600")

        # Load settings from JSON file (if it doesn't exist, create it)
        with open("settings.json", "r") as file:
            settings = json.load(file)
            self.font = settings.get("Font", "Arial")
            self.font_size = settings.get("Font size", 12)
            self.color_mode = settings.get("Color mode", "Light")
            self.colour_palette = settings.get("Colour palette", "Default")
            self.volume = settings.get("Volume", 50)
            self.icon_size = settings.get("Icon size", 24)

        # Apply color mode
        ctk.set_appearance_mode(self.color_mode)

        self.create_widgets()

    def create_widgets(self):
        # Apply font and size multiplier to label
        ctk.CTkLabel(self, text="Settings", font=(self.font, int(2 * self.font_size))).pack(pady=20)

        # Font selection dropdown
        def optionmenu_callback(choice):
            print("Font changed to:", choice)
            self.font = choice

        optionmenu_var = ctk.StringVar(value=self.font)
        optionmenu = ctk.CTkOptionMenu(self, values=["Arial", "Times New Roman", "Comic Sans MS", "Courier New", "Impact", "Georgia"], command=optionmenu_callback, variable=optionmenu_var)
        optionmenu.pack(pady=20)

        # Color mode selection dropdown
        def color_mode_callback(choice):
            print("Color mode changed to:", choice)
            self.color_mode = choice
            ctk.set_appearance_mode(choice)  # Apply color mode

        color_var = ctk.StringVar(value=self.color_mode)
        color_menu = ctk.CTkOptionMenu(self, values=["Light", "Dark", "System"], command=color_mode_callback, variable=color_var)
        color_menu.pack(pady=20)

        # Save button
        save = ctk.CTkButton(self, text="Save", command=self.save)
        save.pack(pady=20)

    def refresh(self):
        self.destroy()
        self.__init__()

    def save(self):
        # Save settings back to the JSON file
        settings = {
            "Font": self.font,
            "Font size": self.font_size,
            "Color mode": self.color_mode,
            "Volume": self.volume,
            "Icon size": self.icon_size
        }
        with open("settings.json", "w") as file:
            json.dump(settings, file)
        self.refresh()

if __name__ == "__main__":
    settings = Settings()
    settings.mainloop()
