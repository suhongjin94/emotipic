from PIL import Image

original = Image.open('test.jpg')
print original.size
if hasattr(original, '_getexif'):
    orientation = 0x0112
    exif = original._getexif()
    if exif is not None:
        orientation = exif[orientation]
        rotations = {
            3: Image.ROTATE_180,
            6: Image.ROTATE_270,
            8: Image.ROTATE_90
        }
        original = original.transpose(rotations[orientation])

original.save('compressed.jpg', quality=10)
