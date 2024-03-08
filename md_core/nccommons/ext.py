"""
python3 core8/pwb.py md_core/nccommons/ext
"""
from pathlib import Path
import mimetypes

import re

def get_new_ext(error_info, file_name):
    """
    استخراج الامتداد الصحيح من رسالة الخطأ باستخدام وحدة pathlib
    """
    
    # استخراج نوع MIME من رسالة mimetypes
    mime_type = re.findall(r'MIME type of the file \((.*?)\)', error_info)
    if len(mime_type) > 0:
        mime_type = mime_type[0]
    
    if not mime_type:
        print("MIME type could not be extracted from the error message.")
        return file_name

    print(f"{mime_type=}")

    # استخراج الامتداد الصحيح من نوع MIME
    correct_ext = mimetypes.guess_extension(mime_type)
    if not correct_ext and mime_type == 'image/x-bmp':
        correct_ext = '.bmp'
    
    if not correct_ext:
        print("Could not determine the correct file extension for the MIME type.")
        return file_name

    # استبدال الامتداد في اسم الملف
    new_file_name = Path(file_name).with_suffix(correct_ext)
    new_file_name = str(new_file_name)
    
    print(f"{new_file_name=}")
    
    return new_file_name

if __name__ == '__main__':
    error = {
    "code": "verification-error",
    # "info": "File extension \".jpg\" does not match the detected MIME type of the file (image/png).",
    "info": "File extension \".jpg\" does not match the detected MIME type of the file (image/x-bmp).",
    "details": [
    "filetype-mime-mismatch",
    "jpg",
    "image/png"
    ],
    "*": "See ..."
    }
    file_name = "VACTERL (Radiopaedia 22547-22573 None 1).jpg"

    new_file_name = get_new_ext(error["info"], file_name)

    print(new_file_name)
