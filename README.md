# Musiko: Music Sheet Transposer

Project Overview
Musiko is a specialized executable system program designed for musicians and composers. Its primary goal is to transpose music sheets from their original keys to desired target keys with speed and accuracy, making it an ideal tool for:
* Musicians experimenting with different key changes.
* Composers needing quick transpositions.
* Beginners learning music theory and key changes.

# Key Features
* Music Transposition: Transpose musical notes quickly and accurately between keys.
* Real-Time Video Background: Dynamic video backgrounds enhance the graphical interface.
* Database Integration: User information, music pieces, and transpositions are stored in an SQL database.
* Error Handling: Ensures robustness against invalid inputs and database issues.
* User-Friendly GUI: Simple and intuitive interface supported by Tkinter.

# Benefits
* Reduces time spent manually transposing music by at least 50%.
* Provides an accessible tool for learning and practicing music.
* Facilitates music education and performance by simplifying transposition.

# Limitations
* Does not support transposing music sheets with chords for instruments like piano and guitar.
* Currently optimized for single-note transpositions.

# Python Concepts and Libraries Used
Tkinter
* Used for creating the graphical user interface.
* Widgets like Label, Entry, Text, Button, and OptionMenu handle user inputs and outputs.
* Displays user prompts and transposition interfaces.

MySQL
* Open-source database management system used to store user data, music pieces, and transposition records.
* Managed via the mysql.connector package for Python.

OpenCV
* Handles video processing for the dynamic background.
* Reads, displays, and manipulates video frames.
* Integrated with Tkinter using the VideoCapture() and cv2.cvtColor() functions.

Pillow (PIL)
* Processes and resizes images.
* Converts OpenCV video frames for display in Tkinter.

Threading
* Ensures smooth video playback without freezing the GUI.
* Background video updates run in a separate thread.

# Sustainable Development Goals Supported
Quality Education
* Simplifies music education by making transposition accessible to learners of all levels.

Economic Growth and Decent Work
* Increases productivity for music educators and performers by automating time-consuming tasks.

Reduced Inequality
* Provides an affordable tool for music education accessible to users regardless of economic or geographic barriers.

Industry, Innovation, and Infrastructure
* Represents a digital innovation that supports the music education and technology industries.

Responsible Consumption and Production
* Encourages sustainable practices by reducing reliance on printed music sheets.

# Program/System Instructions

Database Operations
* Stores and retrieves user information, compositions, and transpositions in a MySQL database.

Music Transposition
* Converts musical notes to semitones, calculates intervals, and applies them to transpose notes into the target key.

User Interface (GUI)
* Prompts users to enter details (name, composition, composer) and transposes notes based on selected keys.

Video Background
* Displays a dynamic video background using OpenCV and Pillow within the Tkinter interface.

# Key Program Components

Database Functions
* connect_to_db: Establishes a connection to the MySQL database.
* save_user_to_db, save_music_piece_to_db, save_transposition_to_db: Save user data, music pieces, and transposition records to the database.

Music Transposition Functions
* transpose_note: Converts a note into its semitone form and applies the calculated interval.
* transpose_sheet: Transposes an entire music sheet.

Tkinter GUI
* User Prompt Interface: Collects user details.
* Transposition Interface: Allows key selection, displays transposed notes, and saves results.

Background Video
* update_background: Reads and updates video frames in real-time without interfering with GUI responsiveness.

# Considerations for Future Improvements
Enhanced Error Handling
* Add more robust validations for user inputs and database operations.

Optimized Video Playback
* Improve background video loop to ensure smooth performance.

User-Friendly Input Formats
* Introduce options for entering musical notation more interactively (e.g., clickable notes).

# Flow of Functionality

* Users log in by entering their name, composition, and composer details.
* User details are stored in the database.
* Transposition screen allows users to:
* Select original and target keys.
* Enter musical notes for transposition.
* Transposed notes are displayed and stored in the database.
* Dynamic video background enhances user experience throughout.

