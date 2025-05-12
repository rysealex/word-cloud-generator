# Word Cloud Generator

This Python script generates a word cloud image based on a user-provided theme word and several customizable options. It fetches related words using the Datamuse API and arranges them in a visually appealing spiral layout. Each word's definition can be viewed by hovering over it in the generated image.

## Features

* **Theme Word Input:** Allows the user to enter a central theme word for the word cloud.
* **Related Word Generation:** Fetches related words from the Datamuse API based on the theme.
* **Customizable Word Count:** Users can specify the number of related words to include (up to 75).
* **Background Color Options:** Offers a choice of white, black, or gray for the word cloud background.
* **Color Palette Selection:** Users can select a main theme color and three additional colors for the words.
* **Font Style Customization:** Provides options for font weight (light, normal, bold) and font type (serif, sans-serif, monospace, cursive, fantasy).
* **Spiral Layout:** Arranges words in an aesthetically pleasing spiral pattern.
* **Collision Detection:** Implements collision detection using R-tree spatial indexing.
* **Interactive Definitions:** Hovering the mouse over a word in the generated image displays its definition (fetched from the Dictionary API) in the Matplotlib toolbar.
* **Progress Indicator:** Shows a spinner animation during the word cloud generation process.
* **Elapsed Time:** Displays the total time taken to generate the word cloud.
* **Debug Mode (Optional):** When enabled, visualizes the padded bounding boxes around each placed word and spiral coordinate points in white, which can be helpful for understanding the collision detection.
* **Statistics Mode (Optional):** When enabled, prints the number of failed coordinate points during each word placement attempt to the terminal, providing insights into the algorithm's efficiency.

## Prerequisites

* Python 3.x
* The following Python libraries:
    * `rtree`
    * `numpy`
    * `matplotlib`
    * `requests`

You can install these libraries using pip:

```bash
pip install rtree numpy matplotlib requests
```

## Installation
1. Clone the repository to your local machine:
```bash
git clone repository_url
```
2. Navigate to the project directory:
```bash
cd project_directory
```
3. (Optional) Enable Debug or Statistics Mode: Open the func.py file and change the values of the DEBUG_MODE and STATISTICS_MODE variables at the beginning of the file to True if you wish to enable these modes. By default, they are set to False.
```python
DEBUG_MODE = False
STATISTICS_MODE = False
```

## Usage
1. Run the main script:
```bash
python generator.py
```
2. Follow the prompts in the terminal to enter a theme word, the number of related words, background color, word colors, font weight, and font type.

3. After generation is finished, a Matplotlib window will appear displaying the word cloud.

4. Hover your mouse over any word in the cloud to see its definition in the toolbar at the bottom of the window.

5. Press the Esc key to close the word cloud window.

6. (If Debug Mode is enabled) You will see white boxes around each word and a series of white spiral coordinate points in the generated image.

7. (If Statistics Mode is enabled) The terminal will display the number of failed placement attempts during the word cloud generation.

## Code Structure
The project consists of two main Python files:
* **generator.py:** This script handles user input, initiates the word cloud generation process, and displays the final image. It utilizes the functions defined in func.py.
* **func.py:** This file contains the core logic for fetching related words, generating the spiral coordinates, placing words while avoiding collisions, and providing interactive definitions.

## Libraries Used
* **func:** Contains the word cloud generation functions.
* **time:** Used for tracking the elapsed time and implementing the spinner.
* **sys:** Used for the spinner animation.
* **threading:** Used to run the spinner in a separate thread.
* **os:** Used to clear the terminal screen (os.system('cls')).
* **rtree:** Used for efficient spatial indexing to detect word collisions.
* **numpy:** Used for numerical operations, particularly in generating the spiral coordinates.
* **matplotlib.pyplot:** Used for plotting the word cloud.
* **random:** Used for randomly selecting colors and rotations for words.
* **requests:** Used to fetch data from the Datamuse and Dictionary APIs.

## Notes
* The accuracy of related words depends on the Datamuse API. Some theme words might not yield any related terms.
* The placement algorithm attempts to fit as many words as possible within the defined space, but some words might be excluded if they cannot be placed without overlapping. Additionally, the placement of words is not perfect and may leave extra space or gaps between words.
* Internet connectivity is required to fetch related words and definitions from the APIs.

## Author
Alex Ryse/rysealex
