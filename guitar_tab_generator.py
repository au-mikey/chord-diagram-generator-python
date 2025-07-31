from PIL import Image, ImageDraw, ImageFont
from collections import defaultdict

def draw_chord_diagram(chord_name, fingering, output_filename, start_fret=1, theme=None):
    # Image dimensions
    width = 200
    height = 250
    padding = 20
    string_count = 6
    fret_count = 6
    fret_spacing = 30
    string_spacing = 30
    dot_radius = 10
    
    # Define default theme (colors and fonts)
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

    # Merge user-provided theme with defaults
    if theme:
        # Recursively update the dictionary to handle nested keys
        for key, value in theme.items():
            if isinstance(value, dict):
                default_theme[key].update(value)
            else:
                default_theme[key] = value

    # Create a blank image with a custom background
    image = Image.new("RGB", (width, height), default_theme['colors']['background'])
    draw = ImageDraw.Draw(image)

    # Load fonts
    try:
        heading_font = ImageFont.truetype(default_theme['fonts']['heading_font_name'], default_theme['fonts']['heading_font_size'])
        small_font = ImageFont.truetype(default_theme['fonts']['small_font_name'], default_theme['fonts']['small_font_size'])
    except IOError:
        heading_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Define the height of the top area for the chord name and open/muted strings.
    title_area_height = padding * 2 + heading_font.getmask(chord_name).getbbox()[3]

    # Calculate the center point for the chord name text.
    text_center_x = width / 2
    text_center_y = title_area_height / 2

    # Draw the chord name using the "ms" (middle-center) anchor.
    draw.text((text_center_x, text_center_y), chord_name, fill=default_theme['colors']['heading_text'], font=heading_font, anchor="ms")

    # Now, calculate where the fretboard diagram should start.
    diagram_start_y = title_area_height

    # Draw the fretboard
    for i in range(string_count):
        x = padding + i * string_spacing
        draw.line((x, diagram_start_y, x, diagram_start_y + fret_spacing * (fret_count - 1)), fill=default_theme['colors']['fretboard_lines'], width=2)
    
    for i in range(fret_count):
        y = diagram_start_y + i * fret_spacing
        draw.line((padding, y, padding + (string_count - 1) * string_spacing, y), fill=default_theme['colors']['fretboard_lines'], width=2)
    
    if start_fret == 1:
        draw.line((padding, diagram_start_y, padding + (string_count - 1) * string_spacing, diagram_start_y), fill=default_theme['colors']['fretboard_lines'], width=6)
    else:
        fret_label_y = diagram_start_y + fret_spacing / 2 - small_font.getmask(str(start_fret)).getbbox()[3] / 2
        draw.text((padding + (string_count - 1) * string_spacing + 10, fret_label_y), str(start_fret), fill=default_theme['colors']['fret_label'], font=small_font)

    string_x_positions = [padding + i * string_spacing for i in range(string_count)]

    # --- Barre Detection Logic ---
    barres = defaultdict(list)
    for string_idx, fret_info in enumerate(fingering):
        if isinstance(fret_info, tuple) and fret_info[0] not in ('X', 'O'):
            fret, finger = fret_info
            if finger > 0: # Only consider fretted notes with a finger number
                barres[(fret, finger)].append(string_idx)

    detected_barres = {key: value for key, value in barres.items() if len(value) > 1}

    # --- Draw Barres First (as a background element) ---
    for (barre_fret, barre_finger), string_indices in detected_barres.items():
        start_string_idx = min(string_indices)
        end_string_idx = max(string_indices)
        
        display_fret = barre_fret - (start_fret - 1)
        
        if display_fret >= 1 and display_fret <= (fret_count - 1):
            barre_y = diagram_start_y + (display_fret - 0.5) * fret_spacing
            x1 = string_x_positions[start_string_idx]
            x2 = string_x_positions[end_string_idx]
            
            barre_box = (x1 - dot_radius, barre_y - dot_radius, x2 + dot_radius, barre_y + dot_radius)
            draw.rounded_rectangle(barre_box, radius=dot_radius, fill=default_theme['colors']['barre_rectangle'])

    # --- Draw Individual Notes and X/O's ---
    for string_idx, fret_info in enumerate(fingering):
        x = string_x_positions[string_idx]
        
        if isinstance(fret_info, tuple):
            fret_value = fret_info[0]

            if fret_value == 'X':
                draw.text((x - 7, diagram_start_y - padding * 1.2), "X", fill=default_theme['colors']['open_mute_text'], font=small_font)
            elif fret_value in ('O', 0):
                draw.text((x - 7, diagram_start_y - padding * 1.2), "O", fill=default_theme['colors']['open_mute_text'], font=small_font)
            else: # It's a fingered note
                fret, finger = fret_info
                
                display_fret = fret - (start_fret - 1)
                
                if display_fret >= 1 and display_fret <= (fret_count - 1):
                    y = diagram_start_y + (display_fret - 0.5) * fret_spacing
                    draw.ellipse((x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius), fill=default_theme['colors']['fingering_dots'])

                    finger_text = str(finger)
                    descent = small_font.getmetrics()[1]
                    ascent = small_font.getmetrics()[0]
                    y_offset = (ascent - descent) / 1.8
                    
                    draw.text((x, y + y_offset), finger_text, fill=default_theme['colors']['finger_number_text'], font=small_font, anchor="ms")
        else: # Handle old format for frets (single integer)
            fret = fret_info
            display_fret = fret - (start_fret - 1)
            if display_fret >= 1 and display_fret <= (fret_count - 1):
                y = diagram_start_y + (display_fret - 0.5) * fret_spacing
                draw.ellipse((x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius), fill=default_theme['colors']['fingering_dots'])
                 
    # Save the image
    image.save(output_filename)
    print(f"Chord diagram for {chord_name} saved as {output_filename}")


# --- Example Usage with Custom Themes ---

# Example 1: Default theme
draw_chord_diagram("C", [('X',), (3, 3), (2, 2), ('O',), (1, 1), ('O',)], "c_major_default.png")

# Example 2: Custom dark mode theme
dark_mode_theme = {
    'colors': {
        'background': '#222222', 
        'fretboard_lines': '#CCCCCC',
        'fret_label': '#CCCCCC',
        'heading_text': '#CCCCCC',
        'open_mute_text': '#CCCCCC',
        'fingering_dots': '#CCCCCC',
        'finger_number_text': '#222222',
        'barre_rectangle': '#444444'
    },
    'fonts': {
        'heading_font_name': 'times.ttf',
        'heading_font_size': 45,
    }
}


draw_chord_diagram("F (Barre)", [(1, 1), (3, 3), (3, 4), (2, 2), (1, 1), (1, 1)], "f_major_barre_dark.png", theme=dark_mode_theme)

draw_chord_diagram("C", [('X',), (3, 3), (2, 2), ('O',), (1, 1), ('O',)], "c_major_dark.png", theme=dark_mode_theme)
