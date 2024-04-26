from PIL import Image, ImageFilter
import pytesseract
import os

img_folder = 'images'
img_names = os.listdir(img_folder)
# for img_name in img_names:
#     img_path = os.path.join(img_folder, img_name)
#     img = Image.open(img_path)
#     img = img.convert('L')
#     img = img.filter(ImageFilter.SHARPEN)
#     text = pytesseract.image_to_string(img, lang='chi_tra')
#     print(text)
img_name = 'images/1000003031.jpg'
img = Image.open(img_name)
img = img.convert('L')
# img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

text = pytesseract.image_to_string(img, lang='chi_tra')
print(text)
result_folder = 'results'
result_file = os.path.join(result_folder, os.path.basename(img_name) + '.txt')
with open(result_file, 'w') as f:
    f.write(text)
