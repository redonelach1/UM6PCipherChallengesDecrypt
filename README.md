# Context
- We had a cipher challenge, topics were mainly maths that is related to cryptography : Polynomials, Prime Number, Some Probability, Group Theory, Arithmetics...
- We were given solutions after the challenge in an encrypted format (steganography) where we had to decrypt some images and extract images that had links to challenges solutions.

- here is my implementation.

# steganography
- Install Python, Pillow and Click.
- To hide `solution1.png` in `challenge1.png` and store it in `hidden1.png` (all images in `img/` directory), run:
```bash
python steganography.py merge --image1=img/challenge1.png --image2=img/solutions1.png --output=img/hidden1.png
```
- To recover the hidden image and store it in `img/`, run:
```bash
    python steganography.py unmerge --image=img/hidden1.png --output=recovered1.png
```
**N.B.!** You will need to write the functions `_unmerge_rgb` and `unmerge` in `steganography.py` to extract the hidden image.

### Example
- Merge:
![screenshot](img/merge_example.png)

- Unmerge:
![screenshot](img/unmerge_example.png)

# PIL
PIL (Python Imaging Library) is a library that adds image processing capabilities to your Python interpreter. This library supports many file formats, and provides powerful image processing and graphics capabilities.

An image is an array of pixels, where each pixel is an array of three values (red, green, blue). Each value is an integer between 0 and 255. The image is stored as a two-dimensional array of pixels.

```python
from PIL import Image
# Open the image file stored in the img/ directory
image = Image.open('img/challenge1.png')
# Get the array of pixels forming the image
map = image.load()
# Get the the image dimensions
height, width = image.size[0], image.size[1]
```
![screenshot](img/rgb.png)
