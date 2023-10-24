import re
import sys
import shutil
from pathlib import Path


JPEG_iMAGES = []
PNG_iMAGES = []
JPG_iMAGES = []
SVG_iMAGES = []
AVI_VIDEO = []
MP4_VIDEO = [] 
MOV_VIDEO = []
MKV_VIDEO = []
DOC_DOCUMENTS = []
DOCX_DOCUMENTS = [] 
TXT_DOCUMENTS = []
PDF_DOCUMENTS = []
XLSX_DOCUMENTS = []
PPTX_DOCUMENTS = []
MP3_AUDIO = [] 
OGG_AUDIO = [] 
WAV_AUDIO = [] 
AMR_AUDIO = []
ZIP_ARCHIVES = []
GZ_ARCHIVES = []
TAR_ARCHIVES = []
MY_OTHER = []

REGISTER_EXTENSION = {
   'JPEG': JPEG_iMAGES ,
   'PNG': PNG_iMAGES , 
   'JPG': JPG_iMAGES , 
   'SVG': SVG_iMAGES ,
   'AVI': AVI_VIDEO ,
   'MOV': MOV_VIDEO ,
   'DOC': DOC_DOCUMENTS ,
   'DOCX': DOCX_DOCUMENTS,
   'TXT': TXT_DOCUMENTS, 
   'PDF' : PDF_DOCUMENTS, 
   'XLSX': XLSX_DOCUMENTS ,
   'PPTX': PPTX_DOCUMENTS ,
   'MP3': MP3_AUDIO , 
   'OGG': OGG_AUDIO ,
   'WAV': WAV_AUDIO ,  
   'AMR': AMR_AUDIO ,
   'ZIP': ZIP_ARCHIVES ,
   'GZ': GZ_ARCHIVES ,
   'TAR': TAR_ARCHIVES ,
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN= set()

def get_extension(name: str):
    return Path(name).suffix[1:].upper()

def scan(folder: Path):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                FOLDERS.append(item)
                scan(item)
            continue
        extension = get_extension(item.name)
        full_name = folder / item.name
        if not extension:
            MY_OTHER.append(full_name)
        else:
            try:
                ext_reg = REGISTER_EXTENSION[extension]
                ext_reg.append(full_name)
                EXTENSIONS.add(extension)
            except KeyError:
                UNKNOWN.add(extension)
                MY_OTHER.append(full_name)

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = dict()

for cyrillic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyrillic)] = latin
    TRANS[ord(cyrillic.upper())] = latin.upper()

def normalize(name: str):
    translate_name = re.sub(r'[^A-Za-z0-9.]', '_', name.translate(TRANS))
    return translate_name

def handle_media(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    file_name.replace(target_folder / normalize(file_name.name))

def handle_documents(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    file_name.replace(target_folder / normalize(file_name.name))

def handle_archive(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(file_name.name.replace(file_name.suffix, ""))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return
    file_name.unlink


def main(folder: Path):
    scan(folder)
    for file in JPEG_iMAGES:
        handle_media(file, folder / 'images' / 'JPEG')
    for file in JPG_iMAGES:
        handle_media(file, folder / 'images' / 'JPG')    
    for file in PNG_iMAGES:
        handle_media(file, folder / 'images' / 'PNG')    
    for file in SVG_iMAGES:
        handle_media(file, folder / 'images' / 'SVG')
    for file in AVI_VIDEO:
        handle_media(file, folder / 'video' / 'AVI')   
    for file in MP4_VIDEO:
        handle_media(file, folder / 'video' / 'MP4')   
    for file in MOV_VIDEO:
        handle_media(file, folder / 'video' / 'MOV')
    for file in MKV_VIDEO:
        handle_media(file, folder / 'video' / 'MKV')
    for file in MP3_AUDIO:
        handle_media(file, folder / 'audio' / 'MP3')
    for file in OGG_AUDIO:
        handle_media(file, folder / 'audio' / 'OGG') 
    for file in WAV_AUDIO:
        handle_media(file, folder / 'audio' / 'WAV')   
    for file in AMR_AUDIO:
        handle_media(file, folder / 'audio' / 'AMR')   
    for file in DOC_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'DOC')  
    for file in DOCX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'DOCX') 
    for file in TXT_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'TXT')  
    for file in PDF_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'PDF')       
    for file in XLSX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'XLSX')
    for file in PPTX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'PPTX')
    for file in DOC_DOCUMENTS:
        handle_media(file, folder / 'MY_OTHER' )
    for file in ZIP_ARCHIVES:
        handle_media(file, folder / 'archives' / 'ZIP')
    for file in GZ_ARCHIVES:
        handle_media(file, folder / 'archives' / 'GZ')
    for file in TAR_ARCHIVES:
        handle_media(file, folder / 'archives' / 'TAR')
    for file in MY_OTHER:
        handle_media(file, folder / 'unknown')

    for folder in FOLDERS[::-1]:
        try :
            folder.rmdir()
        except OSError:
            print(f'Error during remove folder {folder}')

def start():
    if len(sys.argv) > 1: 
        folder_process = Path(sys.argv[1])
        main(folder_process)
    else:
        print("Потрібно надати шлях до папки як аргумент командного рядка")

if __name__ == "__main__":
    start()
