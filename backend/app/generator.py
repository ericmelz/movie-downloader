"""
Prints movie titles to PDF.  Based on
https://chatgpt.com/share/679e7f00-3788-8001-84fb-5ae508c22c4f
"""

import os
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, portrait
from reportlab.lib.units import inch


NUM_COLUMNS = 3
FONT_NAME = "Helvetica"
FONT_SIZE = 8

# Margins (in inches)
LEFT_MARGIN = 0.5
RIGHT_MARGIN = 0.5
TOP_MARGIN = 0.5
BOTTOM_MARGIN = 0.5

# Regex to remove IMDB in braces (e.g., " {imdb-tt2024544}")
IMDB_REGEX = re.compile(r"\s*\{imdb-[^}]+}")


def clean_title(filename):
    """
    Remove filename extension and IMDB id pattern from the movie title
    """
    # Remove file extension if present
    title, _ = os.path.splitext(filename)
    # Remove the IMDb part if present.
    clean = IMDB_REGEX.sub("", title)
    return clean.strip()


async def get_movie_titles(directory):
    """
    Return a sort list of cleaned movie titles from the given directory
    """
    print("Getting movie titles...")
    all_dirs = os.listdir(directory)
    titles = [
        clean_title(f) for f in all_dirs if os.path.isdir(os.path.join(directory, f))
    ]
    return sorted(titles, key=lambda s: s.lower())


def generate_pdf(titles, output_pdf):
    """
    Generate a PDF with the movie titles in multiple columns.
    """
    print("Generating...")
    # Use landscape letter page size for more horizontal space
    # page_width, page_height = landscape(letter)
    page_width, page_height = portrait(letter)

    # Convert margins to points
    left_margin = LEFT_MARGIN * inch
    right_margin = RIGHT_MARGIN * inch
    top_margin = TOP_MARGIN * inch
    bottom_margin = BOTTOM_MARGIN * inch

    # Calculate available width and column width
    available_width = page_width - left_margin - right_margin
    column_width = available_width / NUM_COLUMNS

    # Set line height (a bit more than the font size for spacing)
    line_height = FONT_SIZE * 1.2

    # Create the PDF canvas
    c = canvas.Canvas(output_pdf, pagesize=(page_width, page_height))
    c.setFont(FONT_NAME, FONT_SIZE)

    # Initial positions: start at the top left of the content area
    current_col = 0
    x_positions = [left_margin + i * column_width for i in range(NUM_COLUMNS)]
    y = page_height - top_margin

    for title in titles:
        # If we run out of vertical space in the current column, move to the next column
        if y - line_height < bottom_margin:
            current_col += 1
            if current_col >= NUM_COLUMNS:
                # Start a new page if all columns are used.
                c.showPage()
                c.setFont(FONT_NAME, FONT_SIZE)
                current_col = 0
            y = page_height - top_margin

        x = x_positions[current_col]
        c.drawString(x, y, title)
        y -= line_height

    c.save()
    print(f"PDF saved as: {output_pdf}")


async def generate_report_pdf(movies_directory, output_pdf):
    titles = await get_movie_titles(movies_directory)
    if not titles:
        raise Exception(f"No movie directories found in {movies_directory}")
    generate_pdf(titles, output_pdf)
