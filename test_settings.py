import customtkinter
import tkinter as tk
from tkinter import font as tkFont # Used for Font, though customtkinter handles fonts internally

# Set a default theme for customtkinter (optional, but good practice)
customtkinter.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (default), "dark-blue", "green"

# --- YOUR PROVIDED SETTINGS DATA TEMPLATES ---
# This list defines the structure and types of settings to be displayed.
SETTINGS_DATA_TEMPLATES = [
    {
        "name": "Transform Settings", # Added a 'name' for grouping
        "pos": ['x','y'],
        "r_pos": [['x-from','x-to'],['y-from','y-to']],
        "r_scale": ['from','to'],
        "r_rot": ['from','to'],
        "center": None,
        "scale": None,
        "rot": None
    },
    {
        "name": "Image Settings", # Added a 'name' for grouping
        "path": None,
        "scale": None,
        "rot": None,
        "pos": ['x','y'],
        "center": None
    },
    {
        "name": "Shape Settings", # Added a 'name' for grouping
        "path": None,
        "scale": None,
        "rot": None,
        "color": ['R','G','B','A'],
        "ol_color": ['R','G','B','A'],
        "size": None,
        "pos": ['x','y'],
        "center": None
    }
]

# Placeholder for get_menu function.
# You will likely have a navigation menu here.
def get_menu(parent_frame, controller):
    """
    Placeholder for a navigation menu.
    In a real application, this would likely contain buttons to switch pages.
    """
    menu_frame = customtkinter.CTkFrame(parent_frame)
    # Example menu button
    # customtkinter.CTkButton(menu_frame, text="Go Home", command=lambda: controller.show_frame("HomePage")).pack(pady=10)
    customtkinter.CTkLabel(menu_frame, text="Navigation Menu Placeholder").pack(pady=10)
    return menu_frame

class Settings(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        # Initialize the customtkinter.CTkFrame
        super().__init__(parent)
        self.controller = controller # Store controller for potential navigation

        # Configure the grid for the main Settings frame
        self.grid_columnconfigure(1, weight=1) # Column for settings content
        self.grid_rowconfigure(0, weight=1)    # Row for content

        # Main container for the settings content (replaces W from original code)
        main_content_frame = customtkinter.CTkFrame(self)
        main_content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        main_content_frame.grid_columnconfigure(0, weight=1) # Make content column expandable

        # Assuming self.menu is a navigation menu, position it
        self.menu = get_menu(self, controller)
        self.menu.grid(row=0, column=0, sticky="nsew", padx=10, pady=10) # Position menu

        # Create Headers
        settings_header_frame = customtkinter.CTkFrame(main_content_frame, fg_color="transparent")
        settings_header = customtkinter.CTkLabel(settings_header_frame, text='Settings', font=customtkinter.CTkFont(size=24, weight="bold"))
        settings_header.pack(pady=10)
        settings_header_frame.pack(pady=(10, 0))

        # Create the Scrollable Frame for settings options
        self.scrollable_frame = customtkinter.CTkScrollableFrame(main_content_frame, label_text="Adjust Your Preferences")
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.scrollable_frame.grid_columnconfigure(0, weight=1) # Make scrollable frame column expandable

        # --- Dynamically create settings widgets based on SETTINGS_DATA_TEMPLATES ---
        self._create_settings_widgets()

    def _create_settings_widgets(self):
        """
        Iterates through SETTINGS_DATA_TEMPLATES and creates appropriate
        customtkinter widgets in the scrollable frame.
        """
        row_idx = 0
        for section_data in SETTINGS_DATA_TEMPLATES:
            section_name = section_data.get("name", "Unnamed Section")

            # Create a header for each section
            section_label = customtkinter.CTkLabel(
                self.scrollable_frame,
                text=section_name,
                font=customtkinter.CTkFont(size=18, weight="bold"),
                anchor="w" # Align text to the left
            )
            section_label.grid(row=row_idx, column=0, sticky="ew", pady=(15, 5), padx=5)
            row_idx += 1

            # Create a frame for the settings within this section for better grouping
            section_frame = customtkinter.CTkFrame(self.scrollable_frame)
            section_frame.grid(row=row_idx, column=0, sticky="ew", padx=5, pady=5)
            section_frame.grid_columnconfigure(1, weight=1) # Make value column expandable
            row_idx += 1

            # Iterate through the key-value pairs of the current section's data
            for key, value_template in section_data.items():
                if key == "name": # Skip the 'name' key as it's for the section label
                    continue

                label_text = key.replace('_', ' ').title() + ":" # Format key for display (e.g., "r_pos" -> "R Pos:")

                # Handle different types of settings fields
                if value_template is None:
                    # Simple single input field (e.g., center, scale, rot, size, path)
                    customtkinter.CTkLabel(section_frame, text=label_text, anchor="w").grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
                    entry = customtkinter.CTkEntry(section_frame, placeholder_text=f"Enter {key}")
                    entry.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=2)
                    # You would typically store references to these entry widgets to retrieve their values later
                    row_idx += 1
                elif isinstance(value_template, list) and not any(isinstance(i, list) for i in value_template):
                    # List of simple values (e.g., pos, color, ol_color, r_scale, r_rot)
                    # Create multiple entry fields for components like x, y, R, G, B, A
                    sub_labels = value_template # e.g., ['x', 'y'] or ['R', 'G', 'B', 'A']
                    
                    # Create a sub-frame for grouped inputs
                    input_group_frame = customtkinter.CTkFrame(section_frame, fg_color="transparent")
                    input_group_frame.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=2)
                    input_group_frame.grid_columnconfigure(0, weight=1) # Make columns expandable
                    input_group_frame.grid_columnconfigure(1, weight=1)
                    input_group_frame.grid_columnconfigure(2, weight=1)
                    input_group_frame.grid_columnconfigure(3, weight=1)


                    customtkinter.CTkLabel(section_frame, text=label_text, anchor="w").grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
                    
                    for i, sub_label_text in enumerate(sub_labels):
                        sub_entry = customtkinter.CTkEntry(input_group_frame, placeholder_text=sub_label_text.upper())
                        sub_entry.grid(row=0, column=i, sticky="ew", padx=2, pady=2)
                    row_idx += 1
                elif isinstance(value_template, list) and any(isinstance(i, list) for i in value_template):
                    # Nested list (e.g., r_pos: [['x-from','x-to'],['y-from','y-to']])
                    # This implies multiple pairs of inputs (e.g., x-range, y-range)
                    customtkinter.CTkLabel(section_frame, text=label_text, anchor="w").grid(row=row_idx, column=0, sticky="w", padx=5, pady=2)
                    
                    nested_input_frame = customtkinter.CTkFrame(section_frame, fg_color="transparent")
                    nested_input_frame.grid(row=row_idx, column=1, sticky="ew", padx=5, pady=2)
                    nested_input_frame.grid_columnconfigure(0, weight=1)
                    nested_input_frame.grid_columnconfigure(1, weight=1)

                    for i, range_pair in enumerate(value_template):
                        range_label_text = f"{chr(ord('X') + i)}-Range:" # X-Range, Y-Range etc.
                        customtkinter.CTkLabel(nested_input_frame, text=range_label_text, anchor="w").grid(row=i, column=0, sticky="w", padx=2, pady=2)
                        
                        range_entry_frame = customtkinter.CTkFrame(nested_input_frame, fg_color="transparent")
                        range_entry_frame.grid(row=i, column=1, sticky="ew", padx=2, pady=2)
                        range_entry_frame.grid_columnconfigure(0, weight=1)
                        range_entry_frame.grid_columnconfigure(1, weight=1)

                        entry_from = customtkinter.CTkEntry(range_entry_frame, placeholder_text=range_pair[0].replace('-', ' ').title())
                        entry_from.grid(row=0, column=0, sticky="ew", padx=2, pady=2)
                        entry_to = customtkinter.CTkEntry(range_entry_frame, placeholder_text=range_pair[1].replace('-', ' ').title())
                        entry_to.grid(row=0, column=1, sticky="ew", padx=2, pady=2)
                    row_idx += 1

# --- Example App to run the Settings menu ---
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Application Settings")
        self.geometry("800x600")

        # Configure grid layout for the main window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create an instance of the Settings frame
        # In a real app, 'controller' would be a class managing frame switching
        self.settings_frame = Settings(self, controller=self)
        self.settings_frame.grid(row=0, column=0, sticky="nsew")

    # Placeholder for a method that a controller might have
    def show_frame(self, page_name):
        print(f"Navigating to: {page_name}")
        # In a multi-frame app, you'd switch visible frames here.

if __name__ == "__main__":
    app = App()
    app.mainloop()
