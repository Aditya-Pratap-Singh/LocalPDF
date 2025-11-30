import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import threading
from .pdf_tools import merge_pdfs, split_pdf, images_to_pdf, pdf_to_images, compress_pdf

class LocalPDFApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LocalPDF - Secure Offline PDF Tools")
        self.geometry("900x600")
        
        # Set theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Configure grid layout (1x2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="LocalPDF",
                                                             compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.merge_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Merge PDFs",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.merge_button_event)
        self.merge_button.grid(row=2, column=0, sticky="ew")

        self.split_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Split PDF",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.split_button_event)
        self.split_button.grid(row=3, column=0, sticky="ew")

        self.img2pdf_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Images to PDF",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.img2pdf_button_event)
        self.img2pdf_button.grid(row=4, column=0, sticky="ew")

        self.pdf2img_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="PDF to Images",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.pdf2img_button_event)
        self.pdf2img_button.grid(row=5, column=0, sticky="ew")
        
        self.compress_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Compress PDF",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.compress_button_event)
        self.compress_button.grid(row=6, column=0, sticky="n ew")

        # Create home frame
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_label = ctk.CTkLabel(self.home_frame, text="Welcome to LocalPDF\n\nSelect a tool from the sidebar to get started.\n\n100% Offline & Secure.",
                                                 font=ctk.CTkFont(size=20, weight="bold"))
        self.home_label.grid(row=0, column=0, padx=20, pady=100)

        # Create tool frames
        self.merge_frame = MergeFrame(self)
        self.split_frame = SplitFrame(self)
        self.img2pdf_frame = Img2PdfFrame(self)
        self.pdf2img_frame = Pdf2ImgFrame(self)
        self.compress_frame = CompressFrame(self)

        # Select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.merge_button.configure(fg_color=("gray75", "gray25") if name == "merge" else "transparent")
        self.split_button.configure(fg_color=("gray75", "gray25") if name == "split" else "transparent")
        self.img2pdf_button.configure(fg_color=("gray75", "gray25") if name == "img2pdf" else "transparent")
        self.pdf2img_button.configure(fg_color=("gray75", "gray25") if name == "pdf2img" else "transparent")
        self.compress_button.configure(fg_color=("gray75", "gray25") if name == "compress" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        
        if name == "merge":
            self.merge_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.merge_frame.grid_forget()

        if name == "split":
            self.split_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.split_frame.grid_forget()

        if name == "img2pdf":
            self.img2pdf_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.img2pdf_frame.grid_forget()
            
        if name == "pdf2img":
            self.pdf2img_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.pdf2img_frame.grid_forget()
            
        if name == "compress":
            self.compress_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.compress_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def merge_button_event(self):
        self.select_frame_by_name("merge")

    def split_button_event(self):
        self.select_frame_by_name("split")

    def img2pdf_button_event(self):
        self.select_frame_by_name("img2pdf")
        
    def pdf2img_button_event(self):
        self.select_frame_by_name("pdf2img")
        
    def compress_button_event(self):
        self.select_frame_by_name("compress")

class BaseToolFrame(ctk.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20)
        
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)

    def select_files(self, filetypes):
        return filedialog.askopenfilenames(filetypes=filetypes)
    
    def select_file(self, filetypes):
        return filedialog.askopenfilename(filetypes=filetypes)

    def select_folder(self):
        return filedialog.askdirectory()
    
    def save_file(self, defaultextension, filetypes):
        return filedialog.asksaveasfilename(defaultextension=defaultextension, filetypes=filetypes)

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def show_success(self, message):
        messagebox.showinfo("Success", message)

class MergeFrame(BaseToolFrame):
    def __init__(self, master):
        super().__init__(master, "Merge PDFs")
        
        self.files = []
        
        self.select_btn = ctk.CTkButton(self.content_frame, text="Select PDFs", command=self.select_pdfs)
        self.select_btn.grid(row=0, column=0, padx=20, pady=20)
        
        self.file_list_label = ctk.CTkLabel(self.content_frame, text="No files selected")
        self.file_list_label.grid(row=1, column=0, padx=20, pady=10)
        
        self.merge_btn = ctk.CTkButton(self.content_frame, text="Merge & Save", command=self.run_merge, state="disabled")
        self.merge_btn.grid(row=2, column=0, padx=20, pady=20)

    def select_pdfs(self):
        files = self.select_files([("PDF Files", "*.pdf")])
        if files:
            self.files = files
            self.file_list_label.configure(text=f"{len(files)} files selected")
            self.merge_btn.configure(state="normal")

    def run_merge(self):
        output_path = self.save_file(".pdf", [("PDF Files", "*.pdf")])
        if output_path:
            try:
                merge_pdfs(self.files, output_path)
                self.show_success(f"Merged {len(self.files)} files successfully!")
                self.files = []
                self.file_list_label.configure(text="No files selected")
                self.merge_btn.configure(state="disabled")
            except Exception as e:
                self.show_error(str(e))

class SplitFrame(BaseToolFrame):
    def __init__(self, master):
        super().__init__(master, "Split PDF")
        self.file_path = None
        
        self.select_btn = ctk.CTkButton(self.content_frame, text="Select PDF", command=self.select_pdf)
        self.select_btn.grid(row=0, column=0, padx=20, pady=20)
        
        self.file_label = ctk.CTkLabel(self.content_frame, text="No file selected")
        self.file_label.grid(row=1, column=0, padx=20, pady=10)
        
        self.range_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Page Ranges (e.g. 1-3,5) or leave empty for all")
        self.range_entry.grid(row=2, column=0, padx=20, pady=10)
        
        self.split_btn = ctk.CTkButton(self.content_frame, text="Split & Save", command=self.run_split, state="disabled")
        self.split_btn.grid(row=3, column=0, padx=20, pady=20)

    def select_pdf(self):
        file = self.select_file([("PDF Files", "*.pdf")])
        if file:
            self.file_path = file
            self.file_label.configure(text=os.path.basename(file))
            self.split_btn.configure(state="normal")

    def run_split(self):
        output_dir = self.select_folder()
        if output_dir:
            range_str = self.range_entry.get().strip()
            try:
                split_pdf(self.file_path, output_dir, range_str if range_str else None)
                self.show_success("PDF split successfully!")
            except Exception as e:
                self.show_error(str(e))

class Img2PdfFrame(BaseToolFrame):
    def __init__(self, master):
        super().__init__(master, "Images to PDF")
        self.images = []
        
        self.select_btn = ctk.CTkButton(self.content_frame, text="Select Images", command=self.select_images)
        self.select_btn.grid(row=0, column=0, padx=20, pady=20)
        
        self.file_list_label = ctk.CTkLabel(self.content_frame, text="No images selected")
        self.file_list_label.grid(row=1, column=0, padx=20, pady=10)
        
        self.convert_btn = ctk.CTkButton(self.content_frame, text="Convert & Save", command=self.run_convert, state="disabled")
        self.convert_btn.grid(row=2, column=0, padx=20, pady=20)

    def select_images(self):
        files = self.select_files([("Images", "*.jpg *.jpeg *.png")])
        if files:
            self.images = files
            self.file_list_label.configure(text=f"{len(files)} images selected")
            self.convert_btn.configure(state="normal")

    def run_convert(self):
        output_path = self.save_file(".pdf", [("PDF Files", "*.pdf")])
        if output_path:
            try:
                images_to_pdf(self.images, output_path)
                self.show_success("Converted images to PDF successfully!")
                self.images = []
                self.file_list_label.configure(text="No images selected")
                self.convert_btn.configure(state="disabled")
            except Exception as e:
                self.show_error(str(e))

class Pdf2ImgFrame(BaseToolFrame):
    def __init__(self, master):
        super().__init__(master, "PDF to Images")
        self.file_path = None
        
        self.select_btn = ctk.CTkButton(self.content_frame, text="Select PDF", command=self.select_pdf)
        self.select_btn.grid(row=0, column=0, padx=20, pady=20)
        
        self.file_label = ctk.CTkLabel(self.content_frame, text="No file selected")
        self.file_label.grid(row=1, column=0, padx=20, pady=10)
        
        self.convert_btn = ctk.CTkButton(self.content_frame, text="Convert & Save", command=self.run_convert, state="disabled")
        self.convert_btn.grid(row=2, column=0, padx=20, pady=20)

    def select_pdf(self):
        file = self.select_file([("PDF Files", "*.pdf")])
        if file:
            self.file_path = file
            self.file_label.configure(text=os.path.basename(file))
            self.convert_btn.configure(state="normal")

    def run_convert(self):
        output_dir = self.select_folder()
        if output_dir:
            try:
                pdf_to_images(self.file_path, output_dir)
                self.show_success("PDF converted to images successfully!")
            except Exception as e:
                self.show_error(str(e))

class CompressFrame(BaseToolFrame):
    def __init__(self, master):
        super().__init__(master, "Compress PDF")
        self.file_path = None
        
        self.select_btn = ctk.CTkButton(self.content_frame, text="Select PDF", command=self.select_pdf)
        self.select_btn.grid(row=0, column=0, padx=20, pady=20)
        
        self.file_label = ctk.CTkLabel(self.content_frame, text="No file selected")
        self.file_label.grid(row=1, column=0, padx=20, pady=10)
        
        self.compress_btn = ctk.CTkButton(self.content_frame, text="Compress & Save", command=self.run_compress, state="disabled")
        self.compress_btn.grid(row=2, column=0, padx=20, pady=20)

    def select_pdf(self):
        file = self.select_file([("PDF Files", "*.pdf")])
        if file:
            self.file_path = file
            self.file_label.configure(text=os.path.basename(file))
            self.compress_btn.configure(state="normal")

    def run_compress(self):
        output_path = self.save_file(".pdf", [("PDF Files", "*.pdf")])
        if output_path:
            try:
                compress_pdf(self.file_path, output_path)
                self.show_success("PDF compressed successfully!")
            except Exception as e:
                self.show_error(str(e))
