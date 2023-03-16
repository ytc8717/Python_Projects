# pip install Pillow

from PIL import Image

def resize_image(width, height, imgPath):
    image = Image.open(imgPath)

    print(f"Original size: {image.size}")

    resized_image = image.resize((width, height))

    resized_image.save(f"test-{size1}.png")

size1 = int(input("Enter width: "))
size2 = int(input("Enter height: "))
imgPath = input("Enter image path: ")
resize_image(size1, size2, imgPath)