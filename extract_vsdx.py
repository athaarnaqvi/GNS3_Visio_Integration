import zipfile
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Function to allow the user to select a file using a file dialog
def select_vsdx_file():
    # Hide the root Tkinter window
    Tk().withdraw()

    # Open the file dialog and allow the user to select a .vsdx file
    vsdx_file = askopenfilename(
        title="Select a VSDX file",
        filetypes=[("VSDX files", "*.vsdx")],  # Only show .vsdx files
    )

    return vsdx_file

def save_vsdx_path(vsdx_file):
    # Define a specific path for 'vsdx_path' file
    path = os.path.expanduser("~/Documents/VSCodeProjects/vsdx_path.txt")
    with open(path, "w") as file:
        file.write(vsdx_file)


def main():
    # Prompt the user to select the .vsdx file
    vsdx_file = select_vsdx_file()

    if not vsdx_file:
        print("No file selected.")
        return

    # Save the selected file path
    save_vsdx_path(vsdx_file)

    # Directory to extract the contents
    extract_dir = os.path.expanduser("~/Documents/VSCodeProjects/extracted_vsdx")

    # Ensure the extraction directory exists
    os.makedirs(extract_dir, exist_ok=True)

    # Open and extract the .vsdx (ZIP) file
    with zipfile.ZipFile(vsdx_file, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    print(f'XML files extracted to: {extract_dir}')

if __name__ == "__main__":
    main()
