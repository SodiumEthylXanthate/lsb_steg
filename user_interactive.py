# Imports
import lsb_steg as steg

# Constants
ENCODE = ("encode", '1')
DECODE = ("decode", '2')
MODES  = (ENCODE + DECODE)


def main():
    # Loading image from given path, required regardless of the operating mode
    img_path = input("Enter the path of your image:\n>> ").lower()

    # Validating that image path exists
    try:
        img_bytes, img_height, img_width = steg.load_img(img_path)
    except Exception:
        print("The path you have entered does not exist")
        return  # Exit the main loop and thus end the program

    # Ask for input to determine mode of operation
    mode = input("Choose a mode of operation:\n"\
                    "1. Encode - embed a message inside an image\n"\
                    "2. Decode - extract a message from an image\n"\
                    ">> ").lower()

    # Input validation
    while mode not in MODES:
        print(f"{mode} isn't a valid option. please try again or ctrl + c to quit.")
        mode = input(">> ").lower()

    # Switching to chosen mode of operation
    if mode in ENCODE:  # Enter endcoding mode
        # Getting mode-specific input
        msg = input("Enter the message to hide in the image:\n>> ")
        out_path = input("Enter a path to which the generated image will be saved:\n>> ")
        print("Encoding..")
        # The actual encoding
        encoded_img = steg.lsb_encode(img_bytes, msg, img_height, img_width)
        
        if encoded_img:  # Encoding successful
            encoded_img.save(out_path)
            print(f"Your message has been encoded and the image was saved to {out_path}")
        else:  # Function returned False
            print("Your message is too long, the operation was unsuccessful.")
        
    else:  # Enter decoding mode
        print("Decoding..")
        extracted_msg = steg.lsb_decode(img_bytes)

        if extracted_msg:  # Decoding successful
            print(f"Message extracted:\n{extracted_msg}")
        else:  # Function returned False
            print("Couldn't extract a message from your image.")


if __name__ == "__main__":
    main() 




# add a check to make sure input image path exists