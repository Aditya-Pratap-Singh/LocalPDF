# LocalPDF

LocalPDF is a secure, offline desktop application for managing PDF files. It replicates the functionality of popular online PDF tools but runs entirely on your machine, ensuring your sensitive documents never leave your computer.

## Privacy Guarantee
**100% Offline.** This application does not have any internet connectivity features for processing files. All operations (merge, split, convert, compress) are performed locally on your device using Python libraries.

## Features
-   **Merge PDFs**: Combine multiple PDF files into one.
-   **Split PDF**: Extract pages or split by range.
-   **Images to PDF**: Convert JPG/PNG images to a single PDF.
-   **PDF to Images**: Convert PDF pages to images.
-   **Compress PDF**: Reduce PDF file size.

## Download
You can download the latest version of LocalPDF from the [Releases](https://github.com/Aditya-Pratap-Singh/LocalPDF/releases) page.

## Running from Source

### Prerequisites
-   Python 3.10+
-   pip

### Installation
1.  Clone the repository:
    ```bash
    git clone https://github.com/Aditya-Pratap-Singh/LocalPDF.git
    cd LocalPDF
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Usage
Run the application:
```bash
python src/main.py
```

## Building the Executable
To build the .exe file manually:
```bash
pyinstaller --onefile --noconsole --name "LocalPDF" src/main.py
```
The executable will be located in the `dist/` folder.
