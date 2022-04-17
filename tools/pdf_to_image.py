from typing import List
from pdf2image import convert_from_path
from pathlib import Path,PurePath

def convert_pdf_to_image(file_path: List[str], output_directory : str, dpi : int = 300, fmt : str = 'jpeg') -> None:    
    out_dir_parent = Path(output_directory)
    if not out_dir_parent.is_dir():
            out_dir_parent.mkdir()
            
    for single_file_path in file_path:
        file_name = PurePath(single_file_path).parts[-1]
        file_name_no_ext = file_name.split('.')[0]
        in_file = Path(single_file_path)
        
        out_dir_file = out_dir_parent.joinpath(file_name_no_ext) 
        if not out_dir_file.is_dir():
            out_dir_file.mkdir()
            
        images = convert_from_path(pdf_path = in_file, 
                                   thread_count=8,
                                dpi=dpi,
                                fmt=fmt)
        
        for idx_image, image in enumerate(images):
            image.save(out_dir_file.joinpath(f"{file_name_no_ext}_{idx_image}.{fmt}"))

if __name__ == '__main__':
    test_file_path = ['../datasets/documents/the_witcher.pdf']
    test_output_dir = './out_dir'
    convert_pdf_to_image(test_file_path, test_output_dir)

