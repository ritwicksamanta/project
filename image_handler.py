import numpy as np
from PIL import Image


# os.chdir('static/')


# os.mkdir('encoded/')
# print(os.listdir())

def convert_message_to_binary(message):
    if type(message) == str:
        return ''.join(
            [format(ord(i), '08b') for i in message])  # it will convert each character to 8 digit binary code
    elif type(message) == bytes or type(message) == np.ndarray:
        return [format(i, '08b') for i in message]
    elif type(message) == int:
        return format(message, '08b')
    else:
        raise TypeError('Invalid Data Type')


def encode(src, message, dest):
    src = 'static/images/' + src
    img = Image.open(src, 'r').convert('RGB')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size // n

    message += '&I$igm@'
    binary_message = convert_message_to_binary(message)

    pixels_required = len(binary_message)

    if pixels_required > total_pixels:
        raise ValueError('Need a Large Image')
    else:
        index = 0
        for pixel in range(total_pixels):
            for channel in range(0, 3):
                if index < pixels_required:
                    array[pixel][channel] = int((bin(array[pixel][channel])[2:]) + binary_message[index], 2)
                    index += 1
        array = array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        dest = 'static/encoded/' + dest
        enc_img.save(dest)
        return "Image encoded Successfully"


def decode(src):
    src = './static/decoded/' + src
    img = Image.open(src, 'r')
    array = np.array(img.getdata())

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    total_pixels = array.size // n
    hidden_bits = ''

    for pixel in range(total_pixels):
        for channel in range(0, 3):
            hidden_bits += bin(array[pixel][channel])[2:][-1]  # it will take the last bit only

    hidden_bits = [hidden_bits[i:i + 8] for i in range(0, len(hidden_bits), 8)]
    message = ""
    for i in range(len(hidden_bits)):
        if message[-7:] == '&I$igm@':
            break
        else:
            message += chr(int(hidden_bits[i], 2))


    if '&I$igm@' in message:
        return message[:-7]

    else:
        return 'No hidden message'

# encode('static/images/img.png', 'Hi ALL', 'img.png')
#print(decode('static/encoded/encoded.png'))
