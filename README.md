# 🔒 Block-Based Image Scrambler & Unscrambler
A simple yet effective Python script that scrambles images by rearranging their constituent blocks and provides a reversible mechanism to unscramble them using a generated key file. Ideal for demonstrating basic image manipulation, data hiding concepts, or just having some fun with your pictures!

## ✨ Features
* Block-Based Scrambling: Divides an image into square blocks and shuffles their positions randomly.
* Reversible Unscrambling: Generates a `.key.json` file during scrambling, which can be used to perfectly restore the original image.
* Customizable Block Size: Allows users to specify the size of the blocks for varying levels of scrambling.
* User-Friendly Command-Line Interface: Easy to interact with via a simple menu.
* Error Handling: Includes basic checks for file existence and valid inputs.

⚙️ ## How It Works
1. Scrambling (`block_scramble`):
  * The input image is loaded and converted to RGB format.
  * It's conceptually divided into a grid of blocks based on the specified `block_size`.
  * Each block is extracted and stored, maintaining its original index.
  * A permutation key (a list of shuffled indices) is generated. This key dictates where each original block's content will be placed in the scrambled image.
  * The scrambled image is created by pasting the original blocks according to this permutation.
  * The scrambled image is saved, and the generated permutation key is saved as a `.key.json` file (e.g.,` my_scrambled_image.png.key.json`).
2. Unscrambling (`block_unscramble`):
  * The scrambled image and its corresponding `.key.json` file are loaded.
  * Blocks are extracted from the scrambled image in their current visual order.
  * The permutation key is used to map these visually ordered scrambled blocks back to their original grid positions.

A new image is constructed by pasting the blocks into their correct original order.

⚠️ ## Important Note on Unscrambling
The `.key.json` file is essential for unscrambling. Without this file, the original image cannot be reliably restored, as the shuffling order is unknown. Treat this key file as you would a password for decryption!

🚀 ## Getting Started
* Prerequisites
* Python 3.x

Pillow library (PIL Fork)

## Installation
1. Clone the repository (or download the script):

`git clone https://github.com/Ubuntu-Dekiru/block_based_image_scrambler`
`cd image-scrambler`

Install the Pillow library:

`pip install Pillow`

## Usage
Run the script from your terminal:

`python image_scrambler.py`

The script will present a menu:

`Block-Based Image Scrambler/Unscrambler
Do you want to (E)ncrypt, (D)ecrypt, or (Q)uit? (E/D/Q):`

🖼️ Scrambling an Image (Encrypt)
1. Choose `E` (Encrypt).
2. Enter the path to your input image (e.g., `my_photo.png` or `C:\Users\USER\Documents\py\my_photo.png`).
3. Enter the desired output file name for the scrambled image (e.g., `scrambled_photo.png`).
4. Enter a block size (e.g., `32`, `64`, or press Enter for default `32`).

🔓 Unscrambling an Image (Decrypt)
1. Choose `D` (Decrypt).
2. Enter the path to your scrambled image file (e.g., `scrambled_image.png`).
3. Enter the desired output file name for the unscrambled image (e.g., `restored_image.png`).
4. Enter the same block size that was used during scrambling.
5. Enter the path to the `.key.json` file. If left blank, the script will attempt to infer it (e.g., `scrambled_image.png.key.json`).

## Contributing
Feel free to fork this repository, make improvements, and submit pull requests. Any contributions are welcome!

📄 ## License
This project is open source and available under the MIT License.

## Author
Adedoyin Abass / https://github.com/Ubuntu-Dekiru
