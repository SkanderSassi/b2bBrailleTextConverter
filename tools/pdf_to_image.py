from pdf2image import convert_from_path
from pathlib import Path,PurePath
def convert_pdf_to_image(file_path: str, output_directory : str, dpi : int = 300, fmt : str = 'jpeg') -> None:
    file_name = PurePath(file_path).parts
    out_dir = Path(output_directory)
    in_file = Path(file_path)
    if not Path(output_directory).is_dir():
        out_dir.mkdir()
    images = convert_from_path(pdf_path = in_file, output_folder=output_directory, dpi=dpi,fmt=fmt)
    for idx, image in enumerate(images):
        image.save(f"out_{idx}")
    print(file_name)

if __name__ == '__main__':
    test_file_path = '../datasets/documents/visa_document.pdf'
    test_output_dir = './out_dir'
    convert_pdf_to_image(test_file_path, test_output_dir)

