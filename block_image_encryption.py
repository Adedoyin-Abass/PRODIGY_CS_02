from PIL import Image
import random
import math
import json
import os # To handle file extensions for key file

def block_scramble(image_path, output_path, block_size=32):
    """
    Scrambles an image by dividing it into blocks, shuffling their order,
    and saves the permutation to a key file for unscrambling.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the scrambled image.
        block_size (int): Size of the square blocks (in pixels).
    """
    try:
        # Open the image and ensure it's in RGB mode for consistent processing
        img = Image.open(image_path).convert('RGB')
        width, height = img.size

        # Calculate the number of blocks in each direction, rounding up
        cols = math.ceil(width / block_size)
        rows = math.ceil(height / block_size)

        original_blocks = []
        for i in range(rows):
            for j in range(cols):
                # Define the coordinates for cropping the current block
                left = j * block_size
                top = i * block_size
                right = min((j + 1) * block_size, width)  # Ensure block doesn't go out of bounds
                bottom = min((i + 1) * block_size, height) # Ensure block doesn't go out of bounds

                # Extract the block and add it to our list of original blocks
                block = img.crop((left, top, right, bottom))
                original_blocks.append(block)

        # Create a list of indices representing the original order of blocks
        # This list will be shuffled to determine the new positions of blocks
        permutation = list(range(len(original_blocks)))
        random.shuffle(permutation) # Shuffle the indices to create the permutation

        # Create a new blank image to paste the scrambled blocks onto
        scrambled_img = Image.new('RGB', (width, height))

        # Iterate through the grid positions of the new scrambled image
        # For each position, we determine which original block should go there
        for i in range(rows):
            for j in range(cols):
                current_grid_index = i * cols + j # The linear index of the current grid position
                
                # Check if we have enough blocks to fill this position based on the permutation length
                if current_grid_index < len(permutation):
                    # The value in permutation[current_grid_index] tells us which original block's content
                    # should be placed at this current_grid_index position in the scrambled image.
                    original_block_source_index = permutation[current_grid_index]
                    block_to_paste = original_blocks[original_block_source_index]

                    # Calculate the top-left coordinates for pasting the block
                    left = j * block_size
                    top = i * block_size
                    scrambled_img.paste(block_to_paste, (left, top))

        # Save the newly created scrambled image
        scrambled_img.save(output_path)
        print(f"Scrambled image saved to: {output_path}")

        # Save the permutation (the "key") to a JSON file
        # This key is crucial for correctly unscrambling the image later
        key_output_path = f"{output_path}.key.json"
        with open(key_output_path, 'w') as f:
            json.dump(permutation, f)
        print(f"Scrambling key saved to: {key_output_path}")

    except FileNotFoundError:
        print(f"Error: Input image file not found at {image_path}. Please check the path and try again.")
    except Exception as e:
        print(f"An unexpected error occurred during scrambling: {e}")

def block_unscramble(scrambled_path, output_path, block_size=32, key_path=None):
    """
    Unscrambles a block-scrambled image using a previously saved permutation key.

    Args:
        scrambled_path (str): Path to the scrambled image.
        output_path (str): Path to save the unscrambled image.
        block_size (int): Size of the square blocks used during scrambling.
        key_path (str): Path to the JSON key file containing the permutation.
    """
    try:
        # If no key path is provided, try to infer it from the scrambled image path
        if not key_path:
            key_path = f"{scrambled_path}.key.json"
            print(f"No key path provided. Attempting to load key from default location: {key_path}")

        # Check if the key file exists before attempting to load it
        if not os.path.exists(key_path):
            print(f"Error: Key file not found at {key_path}. Cannot unscramble without the correct key.")
            return

        # Load the permutation from the JSON key file
        with open(key_path, 'r') as f:
            permutation = json.load(f)

        # Open the scrambled image
        scrambled_img = Image.open(scrambled_path).convert('RGB')
        width, height = scrambled_img.size

        # Calculate the number of blocks in each direction based on the image size and block_size
        cols = math.ceil(width / block_size)
        rows = math.ceil(height / block_size)

        scrambled_blocks = []
        for i in range(rows):
            for j in range(cols):
                # Extract blocks from the scrambled image in their current (scrambled) visual order
                left = j * block_size
                top = i * block_size
                right = min((j + 1) * block_size, width)
                bottom = min((i + 1) * block_size, height)
                block = scrambled_img.crop((left, top, right, bottom))
                scrambled_blocks.append(block)

        # Basic validation: check if the number of blocks extracted matches the key's length
        if len(permutation) != len(scrambled_blocks):
            print("Error: The loaded key's permutation size does not match the number of blocks in the scrambled image.")
            print("This usually means the wrong key was provided or the image/block size changed.")
            return

        # Create a list to hold the blocks in their *original* (unscrambled) order
        unscrambled_blocks_ordered = [None] * len(scrambled_blocks)

        # Reconstruct the original order using the permutation
        # The permutation tells us that the block at `scrambled_blocks[k]` (its current visual position `k`)
        # was originally at `permutation[k]` (its original position).
        for k in range(len(permutation)):
            original_idx = permutation[k]
            unscrambled_blocks_ordered[original_idx] = scrambled_blocks[k]

        # Create a new blank image to paste the unscrambled blocks onto
        unscrambled_img = Image.new('RGB', (width, height))
        
        # Paste blocks back into the image in their original grid positions
        # We iterate through the target grid positions and place the blocks from
        # our `unscrambled_blocks_ordered` list sequentially.
        block_idx_counter = 0
        for i in range(rows):
            for j in range(cols):
                if block_idx_counter < len(unscrambled_blocks_ordered):
                    left = j * block_size
                    top = i * block_size
                    block_to_paste = unscrambled_blocks_ordered[block_idx_counter]
                    unscrambled_img.paste(block_to_paste, (left, top))
                    block_idx_counter += 1

        # Save the reconstructed (unscrambled) image
        unscrambled_img.save(output_path)
        print(f"Unscrambled image saved to: {output_path}")

    except FileNotFoundError:
        print(f"Error: Scrambled image file not found at {scrambled_path} or key file at {key_path}.")
        print("Please ensure both files exist and paths are correct.")
    except json.JSONDecodeError:
        print(f"Error: Could not read the key file {key_path}. It might be corrupted or not a valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred during unscrambling: {e}")

def main():
    print("--- Block-Based Image Scrambler/Unscrambler ---")

    while True:
        choice = ''
        # Loop until a valid choice (E, D, Q) is entered
        while choice not in ['E', 'D', 'Q']:
            choice = input("\nDo you want to (E)ncrypt, (D)ecrypt, or (Q)uit? (E/D/Q): ").strip().upper()
            if choice not in ['E', 'D', 'Q']:
                print("Invalid choice. Please enter 'E' for Encrypt, 'D' for Decrypt, or 'Q' to Quit.")

        if choice == 'Q':
            print("Exiting Image Scrambler/Unscrambler. Goodbye!")
            break # Exit the main program loop

        input_file = input("Enter the path to the input image file: ").strip()
        output_file = input("Enter the desired output file name: ").strip()

        block_size = 32 # Set a default block size
        # Loop to get a valid block size from the user
        while True:
            block_size_input = input(f"Enter the block size (e.g., 32, default is {block_size}): ").strip()
            if not block_size_input:
                break # If input is empty, use the default block size
            try:
                temp_block_size = int(block_size_input)
                if temp_block_size <= 0:
                    print("Block size must be a positive integer.")
                else:
                    block_size = temp_block_size
                    break # Valid block size, exit loop
            except ValueError:
                print("Invalid block size entered. Please enter a number.")

        if choice == 'E':
            block_scramble(input_file, output_file, block_size)
        elif choice == 'D':
            # Prompt for key file, giving an example of its expected name
            key_file = input(f"Enter the path to the scrambling key file (e.g., your_scrambled_image.png.key.json): ").strip()
            # If the user doesn't provide a key file path, infer it based on the input image path
            if not key_file:
                key_file = f"{input_file}.key.json"
                print(f"Using inferred key file path: {key_file}")
            block_unscramble(input_file, output_file, block_size, key_file)

if __name__ == "__main__":
    main()
