from PIL import Image

ASCII_CHARS = ['.',',',':',';','+','*','?','%','S','#','@']  # Символы необходимые для формирования изображения
ASCII_CHARS = ASCII_CHARS[::-1]

def resize(image, new_width=100):  # Изменяет размер изображения
    (old_width, old_height) = image.size
    aspect_ratio = float(old_height)/float(old_width)
    new_height = int(aspect_ratio * new_width)
    new_dim = (new_width, new_height)
    new_image = image.resize(new_dim)
    return new_image

def grayscalify(image):  # Делает изображение чёрно-белым
    return image.convert('L')

def modify(image, buckets=25):  # Заменяет пиксели на символы схожей интенсивности
    initial_pixels = list(image.getdata())
    new_pixels = [ASCII_CHARS[pixel_value//buckets] for pixel_value in initial_pixels]
    return ''.join(new_pixels)

def do(image, new_width=100):  # Вызывает ранее описанные функции
    image = resize(image)
    image = grayscalify(image)

    pixels = modify(image)
    len_pixels = len(pixels)

    # Construct the image from the character list
    new_image = [pixels[index:index+new_width] for index in range(0, len_pixels, new_width)]

    return '\n'.join(new_image)

def runner(path):  # Управляет процессом выполнения программы и обрабатывает исключения
    image = None
    try:
        image = Image.open(path)
    except Exception:
        print("Unable to find image in",path)
        #print(e)
        return
    image = do(image)

    # To print on console
    print(image)

    # Else, to write into a file
    # Note: This text file will be created by default under
    #       the same directory as this python file,
    #       NOT in the directory from where the image is pulled.
    f = open('img.txt','w')
    f.write(image)
    f.close()

if __name__ == '__main__':  # Вход в программу, здесь происходит определение идёт работа с локальным файлом или интернет ресурсом
    import sys
    import urllib.request
    if sys.argv[1].startswith('http://') or sys.argv[1].startswith('https://'):  # Если параметр содержит ссылку программа скачивает обрабатываемый файл
        urllib.request.urlretrieve(sys.argv[1], "asciify.jpg")
        path = "asciify.jpg"
    else:
        path = sys.argv[1]
    runner(path)
