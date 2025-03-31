import sys
from PIL import Image

def encode_image(image_path, message):


    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy ảnh tại '{image_path}'")
        sys.exit(1)

    width, height = img.size
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '1111111111111110'  # Dấu hiệu kết thúc thông điệp

    data_index = 0
    for row in range(height):
        for col in range(width):
            pixel = list(img.getpixel((col, row)))
            for color_channel in range(3):  # R, G, B
                if data_index < len(binary_message):
                    pixel[color_channel] = int(format(pixel[color_channel], '08b')[:-1] + binary_message[data_index], 2)
                    data_index += 1
                else:
                    break  # Đã mã hóa hết thông điệp
            img.putpixel((col, row), tuple(pixel))
        if data_index >= len(binary_message):
            break  # Đã mã hóa hết thông điệp

    encoded_image_path = 'encoded_image.png'
    img.save(encoded_image_path)
    print(f"Steganography complete. Encoded image saved as {encoded_image_path}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python encrypt.py <image_path> <message>")
        return

    image_path = sys.argv[1]
    message = sys.argv[2]
    encode_image(image_path, message)

if __name__ == "__main__":
    main()