from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import pytesseract
import os
import cv2

img_folder = 'images'
img_names = os.listdir(img_folder)
# for img_name in img_names:
#     img_path = os.path.join(img_folder, img_name)
#     img = Image.open(img_path)
#     img = img.convert('L')
#     img = img.filter(ImageFilter.SHARPEN)
#     text = pytesseract.image_to_string(img, lang='chi_tra')
#     print(text)

def main():
    img_name = 'images/IMG_20240425_125133.jpg'
    # img = Image.open(img_name)
    # Deskew the image
    processed_image = process_image_with_opencv(img_name)
    text = pytesseract.image_to_string(processed_image, lang='chi_tra+eng')
    print(text)
    result_folder = 'results'
    result_file = os.path.join(result_folder, os.path.basename(img_name) + '.txt')
    with open(result_file, 'w') as f:
        f.write(text)

def resize_by_percentage(image, percentage):
    width, height = image.size
    resized_dimensions = (int(width * percentage), int(height * percentage))
    resized_im = image.resize(resized_dimensions)
    return resized_im

def process_image_with_pillow(img_name):
    img = Image.open(img_name)
    enhanced_contrast_image = ImageOps.autocontrast(img, cutoff=0)
    grayscale_image = ImageOps.grayscale(enhanced_contrast_image)
    # resize image
    resize_image = resize_by_percentage(grayscale_image, 0.5)
    # enhanced_contrast_image = ImageEnhance.Contrast(resize_image).enhance(1.5)
    unsharpmask_image = resize_image.filter(ImageFilter.UnsharpMask(radius=3, percent=220, threshold=4))
    # threshold_value = 140  # Adjust threshold value as needed
    # binarized_image = unsharpmask_image.point(lambda p: p > threshold_value and 255)
    return unsharpmask_image

def process_image_with_opencv(img_name):
    image = cv2.imread(img_name)
    # Define the scaling factor (e.g., 50% = 0.5, 25% = 0.25)
    scale_factor = 0.5  # Resize to 50% of original size

    # Resize the image using OpenCV's resize function
    resized_img = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)
    gray_image = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
    # threshold_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    erode_image = cv2.erode(gray_image, (3,3), iterations=1)
    # cv2.imshow("erode_image", erode_image)
    dilate_image = cv2.dilate(erode_image, (3,3), iterations=1)
    # cv2.imshow("dilate_image", dilate_image)
    # cv2.waitKey()
    # threshold_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return dilate_image

if __name__ == "__main__":
    main()

