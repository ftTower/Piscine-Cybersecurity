from PIL import Image, ExifTags
import sys

unable_log = False

if (len(sys.argv) < 2):
    print("\033[91mUsage: ./scorpion.py <image_path> [additional_image_paths...]\033[0m")
    sys.exit()


for i in range(1, len(sys.argv)):
    try:
        img = Image.open(sys.argv[i])
        img_exif = img.getexif()
    except Exception as e:
        if unable_log == True:
            print(f'\033[91m[ERROR] Unable to open image: {sys.argv[i]}\033[0m')
            print(f'\033[91m[DETAILS] {e}\033[0m')
        continue

    if not img_exif:
        if unable_log == True:
            print(f'\033[91m[INFO] No EXIF data found for image: {sys.argv[i]}\033[0m')
    else:
        print(f'\033[92m[METADATA] Extracting metadata for: {sys.argv[i]}\033[0m')
        print('\033[93m[EXIF DATA]\033[0m')
        for key, val in img_exif.items():
            if key in ExifTags.TAGS:
                tag_name = ExifTags.TAGS[key]
                print(f'  \033[96m{tag_name}:\033[0m {val}')
            else:
                print(f'  \033[96mUnknown Tag {key}:\033[0m {val}')

        # Additional metadata
        print('\033[94m[ADDITIONAL METADATA]\033[0m')
        print(f'  \033[96mFormat:\033[0m {img.format}')
        print(f'  \033[96mMode:\033[0m {img.mode}')
        print(f'  \033[96mSize:\033[0m {img.size}\n')
