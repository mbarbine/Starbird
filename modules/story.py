import os
from modules.text_effects import render_star_wars_text
import markdown
from modules.settings import *
def read_story_text(filename, line_number):
    """
    Reads a specific line from the story text file.

    Args:
        filename (str): The path to the story text file.
        line_number (int): The line number to read.

    Returns:
        str: The content of the specified line.
    """
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if line_number < len(lines):
                return lines[line_number].strip()
            else:
                return "Line not found."
    except FileNotFoundError:
        return f"File {filename} not found."
    except Exception as e:
        return f"Error reading file: {e}"

def star_wars_intro(screen):
    """
    Renders the Star Wars-style intro text on the screen.
    
    Args:
        screen (pygame.Surface): The Pygame screen surface to render on.
    """
    # Assuming main.py and README.md are in the same directory
    readme_path = os.path.join(os.path.dirname(__file__), '../README.md')
    intro_text = read_markdown_section(readme_path, 'Overview')
    if intro_text:
        render_star_wars_text(intro_text, screen)
    else:
        print("Overview section not found in README.md")

def read_markdown_section(filename, section_title):
    """
    Reads a specific section from a markdown file and returns its content.
    
    Args:
        filename (str): The path to the markdown file.
        section_title (str): The title of the section to extract.

    Returns:
        str: The content of the section, or a message if not found.
    """
    try:
        with open(filename, 'r') as file:
            content = file.read()
            md = markdown.Markdown(extensions=['meta'])
            html_content = md.convert(content)
            sections = html_content.split('<h1>')
            for section in sections:
                if section_title in section:
                    return section
        return "Section not found."
    except FileNotFoundError:
        return f"File {filename} not found."
    except Exception as e:
        return f"Error reading markdown file: {e}"
