from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def grayscale_luminosity(image_path, output_path):
        img = Image.open(image_path)
        img_array = np.array(img)
        gray_array = (0.21 * img_array[:, :, 0] + 0.72 * img_array[:, :, 1] + 0.07 * img_array[:, :, 2]).astype(np.uint8)
        gray_img = Image.fromarray(gray_array)
        gray_img.save(output_path)
        plt.imshow(gray_img, cmap='gray')
        plt.show()

    grayscale_luminosity('input.jpg', 'output.jpg')