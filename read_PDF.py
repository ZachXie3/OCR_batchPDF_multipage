# Requires Python 3.6 or higher due to f-strings

# Import libraries
import platform
from tempfile import TemporaryDirectory
from pathlib import Path

import pytesseract
from pdf2image import convert_from_path
from PIL import Image

if platform.system() == "Windows":
	# Windows needs a PyTesseract Download
	# https://github.com/UB-Mannheim/tesseract/wiki/Downloading-Tesseract-OCR-Engine

	pytesseract.pytesseract.tesseract_cmd = (
		r"C:\Program Files\Tesseract-OCR\tesseract.exe"
	)

	# Windows also needs poppler_exe
	path_to_poppler_exe = Path(r"C:\Program Files\poppler-0.68.0\bin")
	
	out_directory = Path(r"~\Desktop").expanduser()
else:
	out_directory = Path("~").expanduser()	

# Path of the Input pdf
PDF_file = r"\\ntsupport\TicShare\toshiba02\Users\EngTest\Report\0514.pdf"

# Store all the pages of the PDF in a variable
image_file_list = []

text_file = out_directory / Path("out_text.txt")

def main():
	''' Main execution point of the program'''
	with TemporaryDirectory() as tempdir:
		# Create a temporary directory to hold our temporary images.

		"""
		Part #1 : Converting PDF to images
		"""

		if platform.system() == "Windows":
			pdf_pages = convert_from_path(
				PDF_file, 500, poppler_path=path_to_poppler_exe, grayscale= True
			)
		else:
			pdf_pages = convert_from_path(PDF_file, 500, grayscale=True)
		# Read in the PDF file at 500 DPI

		# Iterate through all the pages stored above
		for page_enumeration, page in enumerate(pdf_pages[1:3], start=1):
			# enumerate() "counts" the pages for us.

			# Create a file name to store the image
			filename = f"{tempdir}\page_{page_enumeration:03}.jpg"

			# Declaring filename for each page of PDF as JPG
			# For each page, filename will be:
			# PDF page 1 -> page_001.jpg
			# PDF page 2 -> page_002.jpg
			# PDF page 3 -> page_003.jpg
			# ....
			# PDF page n -> page_00n.jpg

			# Save the image of the page in system
			page.save(filename, "JPEG")
			image_file_list.append(filename)

		"""
		Part #2 - Recognizing text from the images using OCR
		"""

		with open(text_file, "a") as output_file:
			# Open the file in append mode so that
			# All contents of all images are added to the same file

			# Iterate from 1 to total number of pages
			for image_file in image_file_list:

				# Set filename to recognize text from
				# Again, these files will be:
				# page_1.jpg
				# page_2.jpg
				# ....
				# page_n.jpg

				text = str(((pytesseract.image_to_string(Image.open(image_file)))))
				text = text.replace("-\n", "")

				output_file.write(text)

			# At the end of the with .. output_file block the file is closed
		# At the end of the with .. tempdir block, the TemporaryDirectory() gets removed

	
if __name__ == "__main__":
	main()
