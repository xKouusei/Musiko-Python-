import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox
import threading
import cv2
from PIL import Image, ImageTk

# Dictionary
notes_to_semitones = {
    "C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4,
    "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9,
    "A#": 10, "B": 11
}

semitones_to_notes = {v: k for k, v in notes_to_semitones.items()}

# MySQL connection function
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",   # MySQL server address (localhost or your server)
            user="root",        # Your MySQL username
            password="",        # Your MySQL password
            database="Musiko"   # Database name
        )
        if conn.is_connected():
            print("Database connection successful!")
            return conn
    except Error as e:
        print(f"Error: {e}")
        return None

# Save
def save_user_to_db(user_name, music_piece, composer):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (user_name, music_piece, composer)
                VALUES (%s, %s, %s)
            """, (user_name, music_piece, composer))
            conn.commit()
            print(f"User {user_name} saved to database!")
            messagebox.showinfo("Success", f"User {user_name} saved successfully!")
        except Error as e:
            print(f"Failed to insert user: {e}")
            messagebox.showerror("Error", "Failed to save user to database.")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

# Save music
def save_music_piece_to_db(music_piece_name, composer):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO musicpieces (music_piece_name, composer)
                VALUES (%s, %s)
            """, (music_piece_name, composer))
            conn.commit()
            print(f"Music piece {music_piece_name} saved to database!")
            messagebox.showinfo("Success", f"Music piece {music_piece_name} saved successfully!")
        except Error as e:
            print(f"Failed to insert music piece: {e}")
            messagebox.showerror("Error", "Failed to save music piece to database.")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

# Save transposition
def save_transposition_to_db(original_key, target_key, original_notes, transposed_notes):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transpositions (original_key, target_key, original_notes, transposed_notes)
                VALUES (%s, %s, %s, %s)
            """, (original_key, target_key, original_notes, transposed_notes))
            conn.commit()
            print("Transposition saved to database!")
        except Error as e:
            print(f"Failed to insert transposition: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to the database.")

# Transpose single note
def transpose_note(note, interval):
    if note not in notes_to_semitones:
        raise ValueError(f"Invalid note: {note}")
    original_semitone = notes_to_semitones[note]
    new_semitone = (original_semitone + interval) % 12
    return semitones_to_notes[new_semitone]

# Transpose a sheet
def transpose_sheet(music_sheet, from_key, to_key):
    if from_key not in notes_to_semitones or to_key not in notes_to_semitones:
        raise ValueError("Invalid key provided.")
    
    from_semitone = notes_to_semitones[from_key]
    to_semitone = notes_to_semitones[to_key]
    interval = to_semitone - from_semitone
    
    transposed_sheet = [transpose_note(note, interval) for note in music_sheet]
    return transposed_sheet

# GUI
def show_transposition_gui(music_piece, composer):
    transposition_root = tk.Tk()
    transposition_root.title("Music Sheet Transposer with Video Background")
    transposition_root.geometry("800x600")  

    cap = cv2.VideoCapture("45.mp4")  

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    def update_background():
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()

        if ret:
            frame = cv2.resize(frame, (transposition_root.winfo_width(), transposition_root.winfo_height()))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_image = ImageTk.PhotoImage(Image.fromarray(frame))
            background_label.config(image=frame_image)
            background_label.image = frame_image
        transposition_root.after(10, update_background)

    background_label = tk.Label(transposition_root)
    background_label.grid(row=0, column=0, columnspan=2, rowspan=8, sticky="nsew")

    background_thread = threading.Thread(target=update_background, daemon=True)
    background_thread.start()

    label_title = tk.Label(transposition_root, text="Music Sheet Transposer", font=("Times New Roman Bold Italic", 30, "bold"), fg="black", bg="#f0f0f0")
    label_title.grid(row=0, column=0, columnspan=2, pady=20)

    music_info_label = tk.Label(transposition_root, text=f"Piece: {music_piece} by {composer}", font=("Arial", 16, "italic"), fg="black", bg="#f0f0f0")
    music_info_label.grid(row=1, column=0, columnspan=2, pady=10)

    label_instructions = tk.Label(transposition_root, text="Enter the notes of the music sheet (such as D F# A B G):", font=("Arial Italic", 12), fg="black", bg="#f0f0f0")
    label_instructions.grid(row=2, column=0, columnspan=2, pady=10)

    music_entry = tk.Text(transposition_root, height=4, width=40, font=("Arial", 14), wrap="word", fg="black", bd=0, highlightthickness=0, bg="#f0f0f0")
    music_entry.grid(row=3, column=0, columnspan=2, pady=10)

    label_from_key = tk.Label(transposition_root, text="Select the original key:", font=("Times New Roman Bold", 12), fg="black", bg="#f0f0f0")
    label_from_key.grid(row=4, column=0, padx=10, pady=5, sticky="e")
    from_key_var = tk.StringVar(value="C")
    from_key_dropdown = tk.OptionMenu(transposition_root, from_key_var, *notes_to_semitones.keys())
    from_key_dropdown.config(font=("Times New Roman Bold", 12), bd=0, highlightthickness=0)
    from_key_dropdown.grid(row=4, column=1, pady=5, sticky="w")

    label_to_key = tk.Label(transposition_root, text="Select the target key:", font=("Times New Roman Bold", 12), fg="black", bg="#f0f0f0")
    label_to_key.grid(row=5, column=0, padx=10, pady=5, sticky="e")
    to_key_var = tk.StringVar(value="C")
    to_key_dropdown = tk.OptionMenu(transposition_root, to_key_var, *notes_to_semitones.keys())
    to_key_dropdown.config(font=("Times New Roman Bold", 12), bd=0, highlightthickness=0)
    to_key_dropdown.grid(row=5, column=1, pady=5, sticky="w")

    def transpose_button_click():
        music_input = music_entry.get("1.0", "end-1c").strip()
        music_sheet = music_input.split()

        from_key = from_key_var.get()
        to_key = to_key_var.get()

        try:
            # Save original notes and transposed notes
            original_notes = " ".join(music_sheet)
            transposed_sheet = transpose_sheet(music_sheet, from_key, to_key)
            result_label.config(text="Transposed Sheet: " + " ".join(transposed_sheet))
            
            # Save to database
            save_transposition_to_db(from_key, to_key, original_notes, " ".join(transposed_sheet))
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    transpose_button = tk.Button(transposition_root, text="Transpose", font=("Arial Bold Italic", 14, "bold"), fg="black", command=transpose_button_click, bg="#f0f0f0")
    transpose_button.grid(row=6, column=0, columnspan=2, pady=20)

    result_label = tk.Label(transposition_root, text="Transposed Sheet: ", font=("Helvetica", 14, "italic"), fg="black", bg="#f0f0f0")
    result_label.grid(row=7, column=0, columnspan=2, pady=20)

    transposition_root.mainloop()
    cap.release()

# User Prompt
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def show_user_prompt():
    try:
        # Create the main window
        prompt_root = tk.Tk()
        prompt_root.title("User Login")
        prompt_root.geometry("1500x1000")

        print("Window created successfully.")  # Debugging message

        # Bg
        bg_image = Image.open("12.jpg")  # Replace 'background.jpg' with your image file
        print("Background image loaded successfully.")  # Debugging message
        bg_image = bg_image.resize((1500, 1000), Image.Resampling.LANCZOS)  # Use LANCZOS for high-quality resizing
        bg_image_tk = ImageTk.PhotoImage(bg_image)

        # Label
        background_label = tk.Label(prompt_root, image=bg_image_tk)
        background_label.place(relwidth=1, relheight=1)  # Fill the entire window with the background image

        # Widgets
        frame = tk.Frame(prompt_root)
        frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

        # Enter name
        label = tk.Label(frame, text="Enter your name:", font=("Arial", 20), fg="black", bg="white")
        label.grid(row=0, pady=(30, 10), padx=30)  # Added more space above and below

        # User name
        user_name_entry = tk.Entry(frame, font=("Arial", 18), fg="black", bg="white", width=30)
        user_name_entry.grid(row=1, pady=(0, 30), padx=30)  # Added more space below

        # Music piece
        label_music_piece = tk.Label(frame, text="Enter music piece name:", font=("Arial", 20), fg="black", bg="white")
        label_music_piece.grid(row=2, pady=(30, 10), padx=30)  # Added more space above and below

        # Entry for music piece
        music_piece_entry = tk.Entry(frame, font=("Arial", 18), fg="black", bg="white", width=30)
        music_piece_entry.grid(row=3, pady=(0, 30), padx=30)  # Added more space below

        # Composer
        label_composer = tk.Label(frame, text="Enter composer's name:", font=("Arial", 20), fg="black", bg="white")
        label_composer.grid(row=4, pady=(30, 10), padx=30)  # Added more space above and below

        # Composer's name
        composer_entry = tk.Entry(frame, font=("Arial", 18), fg="black", bg="white", width=30)
        composer_entry.grid(row=5, pady=(0, 30), padx=30)  # Added more space below

        def on_enter_pressed(event):
            user_name = user_name_entry.get().strip()
            music_piece = music_piece_entry.get().strip()
            composer = composer_entry.get().strip()

            if not user_name or not music_piece or not composer:
                messagebox.showerror("Error", "Please fill in all fields")
                return

            print("Saving user to DB...")  # Debugging message
            save_user_to_db(user_name, music_piece, composer)  # Save user to DB
            save_music_piece_to_db(music_piece, composer)  # Save music piece to DB

            prompt_root.destroy()
            show_transposition_gui(music_piece, composer)

        # Enter 
        user_name_entry.bind("<Return>", on_enter_pressed)
        music_piece_entry.bind("<Return>", on_enter_pressed)
        composer_entry.bind("<Return>", on_enter_pressed)

        # Start Tkinter loop
        print("Starting Tkinter event loop...")  # Debugging message
        prompt_root.mainloop()

    except Exception as e:
        print(f"Error occurred: {e}")

# Prompt
show_user_prompt()
