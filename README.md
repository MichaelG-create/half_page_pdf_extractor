# Half Page PDF Extractor

## Description
This Python project extracts the upper half of each page from a PDF and generates a new PDF with the cropped pages. It also preserves hyperlinks by extracting their coordinates and inserting them correctly in the new cropped pages.

## Features
- **Extracts the upper half of each page** from the original PDF.
- **Preserves hyperlinks** by extracting and inserting them into the new PDF, maintaining their positions.
- **Uses PyMuPDF (fitz)** for PDF manipulation, ensuring high-quality extraction and link preservation.

## Requirements
- Python 3.x
- Install the required dependencies with `pip`:

```bash
pip install -r requirements.txt
