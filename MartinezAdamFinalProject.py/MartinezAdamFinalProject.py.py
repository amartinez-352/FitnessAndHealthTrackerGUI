"""
Author:  Adam Martinez
Date written: 12/09/24
Assignment: Final Project Application
Short Desc: File name (MartinezAdamFinalProject) - Fitness and Health Tracker GUI

This application provides a GUI for tracking fitness activities, logging nutrition, and setting personal health goals.
It uses a local SQLite database to store activities, nutrition entries, and goals.

Main Features:
- Activity Tracking: Log activities with name, duration, and intensity.
- Nutrition Logging: Record daily food items with calorie and macro information.
- Goal Setting: Set weekly exercise hours and daily calorie limits.
- View Summary: Display current goals in a separate window.
- Exit Button: Close the application safely.

Validation:
- The code ensures required fields are not empty.
- Numeric fields are validated to ensure correct data types.
- Error and success messages guide the user through data entry.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # For handling images
import sqlite3

# ---------------------- Database Setup ----------------------
def setup_database():
    """
    Initializes the SQLite database with tables for activities, nutrition, and goals if they don't already exist.
    This ensures the database is ready before the GUI runs.
    """
    conn = sqlite3.connect('fitness_tracker.db')  # Connect to SQLite database
    cursor = conn.cursor()  # Create a cursor to execute SQL commands

    # Create 'activities' table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_name TEXT NOT NULL,
            duration INTEGER NOT NULL,
            intensity TEXT NOT NULL,
            date DATE DEFAULT (DATE('now'))
        )
    """)

    # Create 'nutrition' table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nutrition (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_item TEXT NOT NULL,
            calories INTEGER NOT NULL,
            carbs INTEGER,
            protein INTEGER,
            fats INTEGER,
            date DATE DEFAULT (DATE('now'))
        )
    """)

    # Create 'goals' table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            weekly_exercise_goal INTEGER,
            daily_calorie_limit INTEGER
        )
    """)

    conn.commit()  # Save changes
    conn.close()    # Close connection


# ---------------------- Main Application Class ----------------------
class FitnessApp(tk.Tk):
    """
    Main application class that sets up the GUI, including tabs for activity tracking, nutrition logging, and goal setting.
    Inherits from tk.Tk to represent the main application window.
    """
    def __init__(self):
        super().__init__()  # Initialize the parent tk.Tk class
        self.title("Fitness and Health Tracker")  # Set window title
        self.geometry("800x600")  # Set window size

        # Define color scheme for the application
        self.base_bg = "#1e3d59"    # Dark navy background color
        self.fg_color = "white"     # White text foreground color
        self.highlight_color = "#aed581"  # Green highlight color
        self.frame_bg = "#2c5f77"   # Lighter frame background for contrast

        self.configure(bg=self.base_bg)  # Apply base background color to main window

        # Call method to initialize the UI
        self.init_ui()

    def init_ui(self):
        """
        Initializes the application user interface. This method:
        - Sets up a ttk.Notebook with three tabs.
        - Calls initialization methods for each tab.
        - Applies a custom style for a consistent look.
        """
        # Configure the style for the notebook and its tabs
        style = ttk.Style()
        style.theme_use("clam")  # Use the 'clam' theme for a clean look
        style.configure("TNotebook", background=self.base_bg, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.base_bg, foreground=self.fg_color, font=('Arial', 12, 'bold'))
        style.map("TNotebook.Tab",
                  background=[("selected", self.highlight_color)],
                  foreground=[("selected", "black")])

        # Create a notebook widget to hold tabs
        notebook = ttk.Notebook(self)  # 'self' is the main window
        notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Create frames for each tab
        self.activity_tab = tk.Frame(notebook, bg=self.frame_bg)   # Activity Tracking tab frame
        self.nutrition_tab = tk.Frame(notebook, bg=self.frame_bg)  # Nutrition Logging tab frame
        self.goal_tab = tk.Frame(notebook, bg=self.frame_bg)       # Goal Setting tab frame

        # Add tabs to the notebook
        notebook.add(self.activity_tab, text="Activity Tracking")
        notebook.add(self.nutrition_tab, text="Nutrition Logging")
        notebook.add(self.goal_tab, text="Goal Setting")

        # Load images for Activity and Nutrition tabs
        self.load_activity_image()
        self.load_nutrition_image()

        # Initialize each tab's content and functionality
        self.init_activity_tab()
        self.init_nutrition_tab()
        self.init_goal_tab()

    def load_activity_image(self):
        """
        Loads and displays the activity image in the Activity Tracking tab.
        If the image is not found, prints an error message.
        """
        try:
            img = Image.open(r"E:\guiImages\fitnessgui1.jpg").resize((200, 150), Image.Resampling.LANCZOS)  # Load and resize image
            self.activity_image = ImageTk.PhotoImage(img)  # Convert PIL image to Tkinter image
            # Create a label to hold the image
            img_label = tk.Label(self.activity_tab, image=self.activity_image, bg=self.frame_bg)
            img_label.grid(row=0, column=2, rowspan=4, padx=20, pady=20, sticky="n")
        except Exception as e:
            print("Error loading activity image:", e)  # Print error if image not found

    def load_nutrition_image(self):
        """
        Loads and displays the nutrition image in the Nutrition Logging tab.
        If the image is not found, prints an error message.
        """
        try:
            img = Image.open(r"E:\guiImages\fitnessgui2.jpg").resize((200, 150), Image.Resampling.LANCZOS)  # Load and resize image
            self.nutrition_image = ImageTk.PhotoImage(img)  # Convert PIL image to Tkinter-compatible format
            # Create a label to hold the image
            img_label = tk.Label(self.nutrition_tab, image=self.nutrition_image, bg=self.frame_bg)
            img_label.grid(row=0, column=2, rowspan=5, padx=20, pady=20, sticky="n")
        except Exception as e:
            print("Error loading nutrition image:", e)  # Print error if image not found

    def init_activity_tab(self):
        """
        Initializes the Activity Tracking tab by:
        - Creating labels and entry fields for activity name, duration, intensity.
        - Adding a button to log activities.
        - Displaying a text widget to show logged activities.
        """
        # Label and Entry for Activity Name
        tk.Label(self.activity_tab, text="Activity Name:", bg=self.frame_bg, fg=self.fg_color, font=('Arial', 11)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.activity_name = tk.Entry(self.activity_tab, width=25, bg="white", fg="black")  # Entry for activity name
        self.activity_name.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Label and Entry for Duration
        tk.Label(self.activity_tab, text="Duration (min):", bg=self.frame_bg, fg=self.fg_color, font=('Arial', 11)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.activity_duration = tk.Entry(self.activity_tab, width=25, bg="white", fg="black")  # Entry for activity duration
        self.activity_duration.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Label and ComboBox for Intensity
        tk.Label(self.activity_tab, text="Intensity:", bg=self.frame_bg, fg=self.fg_color, font=('Arial', 11)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.intensity = ttk.Combobox(self.activity_tab, values=["Low", "Medium", "High"], width=23)  # Dropdown for intensity levels
        self.intensity.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Button to log the activity
        log_button = tk.Button(self.activity_tab, text="Log Activity", command=self.log_activity, bg=self.highlight_color, fg="black", font=('Arial', 11, 'bold'))
        log_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Text widget to display logged activities
        self.activity_list = tk.Text(self.activity_tab, height=15, width=50, bg="white", fg="black", font=('Arial', 10))
        self.activity_list.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        # Load existing activities from the database
        self.load_activities()

    def log_activity(self):
        """
        Logs the activity input by the user into the database.
        Checks for input validation (non-empty fields and numeric duration).
        On success, displays a message and refreshes the activity list.
        """
        name = self.activity_name.get()    # Get activity name from entry
        duration = self.activity_duration.get()  # Get duration as a string
        intensity = self.intensity.get()   # Get intensity selection

        # Validation: All fields must be filled
        if not name or not duration or not intensity:
            messagebox.showerror("Input Error", "All fields are required!")
            return

        # Validation: Duration must be numeric
        try:
            duration = int(duration)
        except ValueError:
            messagebox.showerror("Input Error", "Duration must be a number!")
            return

        # Insert the activity into the database
        conn = sqlite3.connect('fitness_tracker.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO activities (activity_name, duration, intensity) VALUES (?, ?, ?)",
                       (name, duration, intensity))
        conn.commit()
        conn.close()

        # Confirm success to user
        messagebox.showinfo("Success", "Activity logged successfully!")
        # Reload the activity list to show the new entry
        self.load_activities()

    def load_activities(self):
        """
        Loads all activities from the database and displays them in the activity_list Text widget.
        If no activities are found, displays a default message.
        """
        conn = sqlite3.connect('fitness_tracker.db')
        cursor = conn.cursor()
        cursor.execute("SELECT activity_name, duration, intensity, date FROM activities")
        records = cursor.fetchall()
        conn.close()

        # Clear the text widget before inserting new data
        self.activity_list.delete(1.0, tk.END)

        # Display activities or a 'no records' message
        if records:
            for record in records:
                self.activity_list.insert(tk.END, f"{record[0]} - {record[1]} min - {record[2]} - {record[3]}\n")
        else:
            self.activity_list.insert(tk.END, "No activities logged yet.\n")

    def init_nutrition_tab(self):
        """
        Initializes the Nutrition Logging tab by:
        - Creating labels and entry fields for food item, calories, carbs, protein, and fats.
        - Adding a button to log nutrition.
        - Displaying a text widget to show logged nutrition entries.
        """
        # Food Item label and entry
        tk.Label(self.nutrition_tab, text="Food Item:", bg=self.frame_bg, fg=self.fg_color, font=('Arial', 11)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.food_item = tk.Entry(self.nutrition_tab, width=25, bg="white", fg="black")  # Entry for food item name
        self.food_item.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Calories label and entry
        tk.Label(self.nutrition_tab, text="Calories:", bg=self.frame_bg, fg=self.fg_color, font=('Arial', 11)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.calories = tk.Entry(self.nutrition_tab, width=25, bg="white", fg="black")  # Entry for calorie amount
        self.calories.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Carbs label and entry
        tk.Label(self.nutrition_tab, text="Carbs (g):", bg=self.frame_bg, fg=self.fg_color, font=('Arial', 11)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.carbs = tk.Entry(self.nutrition_tab, width=25, bg="white", fg="black")  # Entry for carbs
        self.carbs.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Protein label and entry
        tk.Label(self.nutrition_tab, text="Protein (g):", bg=self.frame_bg, fg=self.fg_color, font=('Arial', 11)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.protein = tk.Entry(self.nutrition_tab, width=25, bg="white", fg="black")  # Entry for protein
        self.protein.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Fats label and entry
        tk.Label(self.nutrition_tab, text="Fats (g):", bg=self.frame_bg, fg=self.fg_color, font=('Arial', 11)).grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.fats = tk.Entry(self.nutrition_tab, width=25, bg="white", fg="black")  # Entry for fats
        self.fats.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Button to log nutrition
        log_button = tk.Button(self.nutrition_tab, text="Log Nutrition", command=self.log_nutrition, bg=self.highlight_color, fg="black", font=('Arial', 11, 'bold'))
        log_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Text widget to display logged nutrition
        self.nutrition_list = tk.Text(self.nutrition_tab, height=15, width=50, bg="white", fg="black", font=('Arial', 10))
        self.nutrition_list.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        # Load existing nutrition data from the database
        self.load_nutrition()

    def log_nutrition(self):
        """
        Logs nutrition information provided by the user into the database.
        Validates required fields and numeric types.
        On success, shows a message and refreshes the nutrition list.
        """
        food_item = self.food_item.get()   # Get food item name
        calories = self.calories.get()     # Get calories input
        carbs = self.carbs.get()           # Get carbs input
        protein = self.protein.get()       # Get protein input
        fats = self.fats.get()             # Get fats input

        # Validation: Food item and calories must not be empty
        if not food_item or not calories:
            messagebox.showerror("Input Error", "Food Item and Calories are required!")
            return

        # Validation: Calories and macros must be numeric if provided
        try:
            calories = int(calories)
            carbs = int(carbs) if carbs else 0
            protein = int(protein) if protein else 0
            fats = int(fats) if fats else 0
        except ValueError:
            messagebox.showerror("Input Error", "Calories, Carbs, Protein, and Fats must be numbers!")
            return

        # Insert the nutrition entry into the database
        conn = sqlite3.connect('fitness_tracker.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO nutrition (food_item, calories, carbs, protein, fats) 
            VALUES (?, ?, ?, ?, ?)
        """, (food_item, calories, carbs, protein, fats))
        conn.commit()
        conn.close()

        # Inform the user of successful logging
        messagebox.showinfo("Success", "Nutrition logged successfully!")
        # Reload the nutrition list to reflect the new entry
        self.load_nutrition()

    def load_nutrition(self):
        """
        Loads all nutrition records from the database and displays them in the nutrition_list Text widget.
        If no records exist, displays a default message.
        """
        conn = sqlite3.connect('fitness_tracker.db')
        cursor = conn.cursor()
        cursor.execute("SELECT food_item, calories, carbs, protein, fats, date FROM nutrition")
        records = cursor.fetchall()
        conn.close()

        # Clear current text widget content
        self.nutrition_list.delete(1.0, tk.END)

        # Display each record or a 'no records' message
        if records:
            for record in records:
                self.nutrition_list.insert(tk.END, f"{record[0]} - {record[1]} cal - {record[2]}g carbs - {record[3]}g protein - {record[4]}g fats - {record[5]}\n")
        else:
            self.nutrition_list.insert(tk.END, "No nutrition records found.\n")

    def init_goal_tab(self):
        """
        Initializes the Goal Setting tab by:
        - Adding entry fields for weekly exercise goal and daily calorie limit.
        - Providing a button to set goals.
        - A button to view a summary of current goals in a separate window.
        - An exit button to close the application.
        - A label to display the current set goals.
        """
        # Label and Entry for Weekly Exercise Goal
        tk.Label(self.goal_tab, text="Weekly Exercise Goal (hours):", bg=self.frame_bg, fg=self.fg_color, font=('Arial', 11)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.exercise_goal = tk.Entry(self.goal_tab, width=25, bg="white", fg="black")  # Entry for weekly exercise goal
        self.exercise_goal.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Label and Entry for Daily Calorie Limit
        tk.Label(self.goal_tab, text="Daily Calorie Limit:", bg=self.frame_bg, fg=self.fg_color, font=('Arial', 11)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.calorie_limit = tk.Entry(self.goal_tab, width=25, bg="white", fg="black")  # Entry for daily calorie limit
        self.calorie_limit.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Button to Set Goals
        goal_button = tk.Button(self.goal_tab, text="Set Goals", command=self.set_goals, bg=self.highlight_color, fg="black", font=('Arial', 11, 'bold'))
        goal_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Button to View Summary (opens a separate window)
        summary_button = tk.Button(self.goal_tab, text="View Summary", command=self.open_summary_window, bg=self.highlight_color, fg="black", font=('Arial', 11, 'bold'))
        summary_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Exit button to close the application
        exit_button = tk.Button(self.goal_tab, text="Exit Application", command=self.exit_application, bg=self.highlight_color, fg="black", font=('Arial', 11, 'bold'))
        exit_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Label to display current goals
        self.goal_status = tk.Label(self.goal_tab, text="", bg=self.frame_bg, fg=self.fg_color, font=('Arial', 12, 'bold'))
        self.goal_status.grid(row=5, column=0, columnspan=2, pady=10)

    def set_goals(self):
        """
        Sets the user's goals in the database.
        Validates that both fields are filled and numeric.
        On success, updates the goal_status label and displays a success message.
        """
        exercise_goal = self.exercise_goal.get()  # Weekly exercise goal as string
        calorie_limit = self.calorie_limit.get()  # Daily calorie limit as string

        # Validation: Both fields required
        if not exercise_goal or not calorie_limit:
            messagebox.showerror("Input Error", "All fields are required!")
            return

        # Validation: Both values must be integers
        try:
            exercise_goal = int(exercise_goal)
            calorie_limit = int(calorie_limit)
        except ValueError:
            messagebox.showerror("Input Error", "Goals must be numbers!")
            return

        # Insert or update goals in the database
        conn = sqlite3.connect('fitness_tracker.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM goals")  # Clear old goals and store only the latest
        cursor.execute("INSERT INTO goals (weekly_exercise_goal, daily_calorie_limit) VALUES (?, ?)",
                       (exercise_goal, calorie_limit))
        conn.commit()
        conn.close()

        # Update the status label to show the newly set goals
        self.goal_status.config(text=f"Weekly Goal: {exercise_goal} hrs | Daily Limit: {calorie_limit} cal")
        messagebox.showinfo("Success", "Goals set successfully!")

    def open_summary_window(self):
        """
        Opens a new TopLevel window to display the user's current goals.
        Queries the database for the latest goals and displays them.
        If no goals are set, shows a message stating so.
        """
        summary_window = tk.Toplevel(self)  # Create a new window on top of the main window
        summary_window.title("Goal Summary")
        summary_window.geometry("300x200")
        summary_window.configure(bg=self.frame_bg)

        # Label in the summary window
        tk.Label(summary_window, text="Your Current Goals:", bg=self.frame_bg, fg=self.fg_color, font=('Arial', 12, 'bold')).pack(pady=10)

        # Get the latest goals from the database
        conn = sqlite3.connect('fitness_tracker.db')
        cursor = conn.cursor()
        cursor.execute("SELECT weekly_exercise_goal, daily_calorie_limit FROM goals ORDER BY id DESC LIMIT 1")
        goal = cursor.fetchone()
        conn.close()

        # Display goals if present, otherwise show a no-goals message
        if goal:
            weekly_goal, daily_cal = goal
            tk.Label(summary_window, text=f"Weekly Exercise: {weekly_goal} hrs", bg=self.frame_bg, fg=self.fg_color, font=('Arial', 11)).pack(pady=5)
            tk.Label(summary_window, text=f"Daily Calorie Limit: {daily_cal} cal", bg=self.frame_bg, fg=self.fg_color, font=('Arial', 11)).pack(pady=5)
        else:
            tk.Label(summary_window, text="No goals set yet.", bg=self.frame_bg, fg=self.fg_color, font=('Arial', 11)).pack(pady=10)

        # Close button to destroy the summary window
        close_button = tk.Button(summary_window, text="Close", command=summary_window.destroy, bg=self.highlight_color, fg="black", font=('Arial', 11, 'bold'))
        close_button.pack(pady=10)

    def exit_application(self):
        """
        Asks for confirmation before closing the application.
        If confirmed, destroys the main application window and ends the program.
        """
        if messagebox.askyesno("Exit", "Are you sure you want to exit the application?"):
            self.destroy()  # Close the main window and exit


# ---------------------- Main Entry Point ----------------------
if __name__ == "__main__":
    setup_database()  # Ensure the database is set up before starting the GUI
    app = FitnessApp()  # Create an instance of the FitnessApp class
    app.mainloop()       # Start the Tkinter event loop to run the application
