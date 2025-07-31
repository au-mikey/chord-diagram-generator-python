Chord Diagram Generator - Python Version

A Python script to generate customizable guitar chord diagrams as image files. This tool automatically detects barre chords and allows for extensive visual customization through a theme parameter.
Features

    Customizable Chord Names: Easily set the title for your chord diagram.

    Flexible Fingering Input: Supports muted ('X'), open ('O'), and fretted notes (fret, finger number).

    Automatic Barre Chord Detection: Intelligently identifies and draws barre chords as a background rectangle when the same finger is used on the same fret across multiple strings.

    Individual Finger Number Display: Shows finger numbers on each fretted note, including those under a barre.

    Customizable Themes: Control colors (background, lines, text, dots, barres) and font styles/sizes for the heading and other text elements.

    Output as PNG: Generates high-quality PNG image files of the chord diagrams.

Installation

To use this script, you need Python installed on your system.

    Clone the repository:

    git clone https://github.com/au-mikey/chord-diagram-generator-python.git
    cd chord-diagram-generator-python

    (Remember to replace au-mikey with your actual GitHub username)

    Install dependencies:
    This project requires the Pillow library for image manipulation. You can install it using pip:

    pip install -r requirements.txt

Usage

The core functionality is provided by the draw_chord_diagram function.
Function Signature

draw_chord_diagram(chord_name, fingering, output_filename, start_fret=1, theme=None)

    chord_name (str): The name of the chord (e.g., "C Major", "G7").

    fingering (list): A list of 6 items, one for each string (low E to high E).

        ('X',): Muted string.

        ('O',): Open string.

        (fret_number, finger_number): Fretted note. fret_number is an integer (0 for open, 1-based for frets), finger_number is an integer (1-4 for fingers, or 0 if no specific finger/open).

    output_filename (str): The name of the output image file (e.g., "c_major.png").

    start_fret (int, optional): The fret number where the diagram starts. Defaults to 1. If greater than 1, the fret number will be displayed on the side.

    theme (dict, optional): A dictionary to customize colors and fonts. See "Customization" section below.

Example

To generate a C Major chord diagram with default settings:

from guitar_tab_generator import draw_chord_diagram

# C Major (EADGBe): X 3 2 0 1 0
draw_chord_diagram("C Major", [('X',), (3, 3), (2, 2), ('O',), (1, 1), ('O',)], "c_major_default.png")

To run all the examples provided in the script, simply execute the guitar_tab_generator.py file:

python guitar_tab_generator.py

Customization (Theme Parameter)

The theme parameter allows you to control the visual appearance of the diagram. It's a dictionary that can contain colors and fonts sub-dictionaries. You only need to specify the values you want to change; the rest will use defaults.

Default Theme Structure:

default_theme = {
    'colors': {
        'background': 'white',
        'fretboard_lines': 'black',
        'fret_label': 'black',
        'heading_text': 'black',
        'open_mute_text': 'black',
        'fingering_dots': 'black',
        'finger_number_text': 'white',
        'barre_rectangle': 'darkgrey',
    },
    'fonts': {
        'heading_font_name': 'arial.ttf',
        'heading_font_size': 40,
        'small_font_name': 'arial.ttf',
        'small_font_size': 20,
    }
}

Example of Custom Theme Usage:

from guitar_tab_generator import draw_chord_diagram

# Custom dark mode theme for an F Barre chord
dark_theme = {
    'colors': {
        'background': '#222222', 
        'fretboard_lines': '#CCCCCC',
        'heading_text': '#CCCCCC',
        'fingering_dots': '#CCCCCC',
        'finger_number_text': '#222222',
        'barre_rectangle': '#444444'
    },
    'fonts': {
        'heading_font_name': 'times.ttf', # Ensure this font file is available
        'heading_font_size': 45,
    }
}
draw_chord_diagram(
    "F (Barre)",
    [(1, 1), (3, 3), (3, 4), (2, 2), (1, 1), (1, 1)],
    "f_major_barre_dark.png",
    theme=dark_theme
)

Note on Fonts: If you specify a custom font name (e.g., 'times.ttf', 'dejavusansmono.ttf'), ensure that the .ttf font file is present in the same directory as your Python script, or provide a full path to the font file. If the font is not found, the script will fall back to a default font.
License

This project is licensed under the MIT License. See the LICENSE file for details.
Contributing

Contributions are welcome! If you have ideas for improvements, new features, or bug fixes, feel free to open an issue or submit a pull request.
