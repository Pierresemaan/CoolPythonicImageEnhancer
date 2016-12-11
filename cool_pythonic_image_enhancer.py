import os
import math
from PIL import Image, ImageFilter, ImageEnhance, ImageFont, ImageDraw
import textwrap


def main():
    assets_folder = os.path.join(os.path.dirname(__file__), 'assets')
    print_header()
    raw_im = get_image(assets_folder)
    text = get_text_from_user()
    if raw_im and text:
        im = update_image(raw_im, assets_folder, text)
        im.show()
        im.save('cool_pythonic_image.jpg', 'JPEG')
    elif text:
        print("Ups, image cannot be found")


def print_header():
    print('-------------------------------------')
    print('    Cool Pythonic Image Enhancer')
    print('--------------------------------------')


def get_image(assets_folder):
    filename = input('Enter Image (Full)Name ')

    if os.path.exists(os.path.join(assets_folder, filename)):
        image = Image.open(os.path.join(assets_folder, filename))
    elif os.path.exists(filename):
        image = Image.open(filename)
    else:
        image = None
    return image


def get_text_from_user():
    text = input('Enter Text (60 Char max): ')
    if not text.strip() or len(text) > 60:
        print("Invalid Text")
        text = None
    return text


def update_image(raw_im, assets_folder, text):
    margin = 10
    logo_size = 100
    # Image Filters
    im = raw_im.filter(ImageFilter.SHARPEN)
    enhancer = ImageEnhance.Color(im)
    im = enhancer.enhance(1.3)
    # Background
    background = Image.new('RGB', (im.width, im.height + logo_size + 2*margin), (0, 0, 0))
    background.paste(im, (0, 0))
    # DD Logo
    dd_logo = Image.open(os.path.join(assets_folder, 'dimensionDataLogo.png'))
    dd_logo.thumbnail((logo_size, logo_size))
    background.paste(dd_logo, (background.width - dd_logo.width, background.height - dd_logo.height - margin))
    # Python Logo
    python_logo = Image.open(os.path.join(assets_folder, 'python-logo.png'))
    python_logo.thumbnail((logo_size, logo_size))
    background.paste(python_logo, (margin, background.height - python_logo.height - margin))

    # Text Area
    font_size = (background.width - 2*(logo_size+margin)) / margin
    font = ImageFont.truetype("arial.ttf", int(font_size))
    draw = ImageDraw.Draw(background)
    w, h = draw.textsize(text, font)

    lines = textwrap.wrap(text, width=20)
    y_text = im.height
    for line in lines:
        width, height = font.getsize(line)
        y_text += height
        draw.text((140, y_text), line, font=font)
    return background


if __name__ == '__main__':
    main()
