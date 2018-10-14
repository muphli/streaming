from imgpy import Img
from PIL import Image, ImageSequence, ImageOps
import sys

#pass one argument: name of source file
if (len(sys.argv[1:]) == 1):
    source = sys.argv[1]
else:
    print("Too many arguments. Please do only provide the name of the source-file.")
    sys.exit(1)

image = Image.open(source)

#read sequence of frames within GIF-image
frames = ImageSequence.Iterator(image)

def crop(frames):
    for frame in frames:
        croppedImage = frame.copy()
        croppedImage = ImageOps.fit(croppedImage, (360, 216))
        yield croppedImage

frames = crop(frames)

outputImage = next(frames)
outputImage.info = image.info
outputImage.save("resized.gif", save_all=True, append_images=list(frames))

# define two-dimensional list with boundaries
b = [[0,0,72,72],[72,0,144,72],[144,0,216,72],[216,0,288,72],[288,0,360,72]
    ,[0,72,72,144],[72,72,144,144],[144,72,216,144],[216,72,288,144],[288,72,360,144]
    ,[0,144,72,216],[72,144,144,216],[144,144,216,216],[216,144,288,216],[288,144,360,216]]

# iterate through lists within b
for index, box in enumerate(b):
    # set values of list-item for box
    left = box[0]
    upper = box[1]
    right = box[2]
    lower = box[3]

    # crop and save image
    with Img(fp="resized.gif") as im:
        im.crop(box=(left, upper, right, lower))
        incrFP = 'cropped_' + str(index + 1) + '.gif'
        im.save(fp=incrFP)