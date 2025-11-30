import unittest
import os
import shutil
from PIL import Image
from src.pdf_tools import merge_pdfs, split_pdf, images_to_pdf, pdf_to_images, compress_pdf

class TestPDFTools(unittest.TestCase):
    def setUp(self):
        self.test_dir = "tests/test_data"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)
        
        # Create dummy images
        self.img1_path = os.path.join(self.test_dir, "img1.png")
        self.img2_path = os.path.join(self.test_dir, "img2.png")
        Image.new('RGB', (100, 100), color='red').save(self.img1_path)
        Image.new('RGB', (100, 100), color='blue').save(self.img2_path)
        
        # Create dummy PDF (from images)
        self.pdf1_path = os.path.join(self.test_dir, "test1.pdf")
        self.pdf2_path = os.path.join(self.test_dir, "test2.pdf")
        images_to_pdf([self.img1_path], self.pdf1_path)
        images_to_pdf([self.img2_path], self.pdf2_path)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_merge_pdfs(self):
        output_path = os.path.join(self.test_dir, "merged.pdf")
        merge_pdfs([self.pdf1_path, self.pdf2_path], output_path)
        self.assertTrue(os.path.exists(output_path))

    def test_split_pdf(self):
        # Create a 2-page PDF first
        merged_path = os.path.join(self.test_dir, "merged_for_split.pdf")
        merge_pdfs([self.pdf1_path, self.pdf2_path], merged_path)
        
        output_dir = os.path.join(self.test_dir, "split_output")
        os.makedirs(output_dir)
        
        split_pdf(merged_path, output_dir)
        self.assertEqual(len(os.listdir(output_dir)), 2)

    def test_images_to_pdf(self):
        output_path = os.path.join(self.test_dir, "from_images.pdf")
        images_to_pdf([self.img1_path, self.img2_path], output_path)
        self.assertTrue(os.path.exists(output_path))

    def test_pdf_to_images(self):
        output_dir = os.path.join(self.test_dir, "images_output")
        os.makedirs(output_dir)
        pdf_to_images(self.pdf1_path, output_dir)
        self.assertTrue(len(os.listdir(output_dir)) > 0)
        
    def test_compress_pdf(self):
        output_path = os.path.join(self.test_dir, "compressed.pdf")
        compress_pdf(self.pdf1_path, output_path)
        self.assertTrue(os.path.exists(output_path))

if __name__ == '__main__':
    unittest.main()
