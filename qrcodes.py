import io
import qrcode
from PIL import Image


def generate_qr_code_file(data, logo_file, output_file="qr_code.png", fill_color='black', back_color='white', size=12, border=0):
    """Embeds an image in the center of a QR code."""
    qr_image_bytes = generate_qr_code_bytes(data, logo_file, fill_color, back_color, size, border)
    saved_path = save_image_to_file(qr_image_bytes, output_file)  # Call the save function

    if saved_path:
        # Use saved_path in your application
        print(f"Image saved at: {saved_path}")
    else:
        print("Image save failed")

    return saved_path


def generate_qr_code_bytes(data, logo_file, fill_color='black', back_color='white', size=12, border=0):
    """Embeds an image in the center of a QR code."""

    try:
        # Create the QR code (adjust version and error correction as needed)
        qr = qrcode.QRCode(
            version=7,  # Start with a lower version; increase if needed
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction is recommended
            box_size=size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGBA")  # Ensure RGB for image pasting

        if logo_file:
            # Load and resize the image
            try:
                logo = Image.open(logo_file).convert("RGBA") # Ensure RGB for image pasting
            except FileNotFoundError:
                print(f"Error: Logo image not found at {logo_file}")
                return

            # Logo size relative to QR width
            qr_width, qr_height = qr_image.size
            max_logo_size = int(qr_width * 0.3)
            logo_w, logo_h = logo.size
            if logo_w > logo_h:
                logo_new_w = max_logo_size
                logo_new_h = round(logo_h * max_logo_size / logo_w)
            else:
                logo_new_h = max_logo_size
                logo_new_w = round(logo_w * max_logo_size / logo_h)

            logo = logo.resize((logo_new_w, logo_new_h), Image.LANCZOS)
            logo_width, logo_height = logo.size
            position = ((qr_width - logo_width) // 2, (qr_width - logo_height) // 2)

            # Create a background image with the QR code's background color
            background = Image.new("RGBA", logo.size, qr_image.getpixel((0, 0)))  # Get top-left pixel color

            # Paste the logo onto the background
            background.paste(logo, (0, 0), logo)

            # Paste the combined logo+background onto the QR code
            qr_image.paste(background, position)


        # Save the combined image
        img_bytes = io.BytesIO()
        qr_image.save(img_bytes, format='PNG')
        img_bytes.seek(0)  # Reset stream position
        return img_bytes.getvalue()

    except Exception as e:
        print(f"An error occurred: {e}")


def save_image_to_file(image_bytes, filename):
    """Saves image bytes to a file."""
    try:
        image = Image.open(io.BytesIO(image_bytes))  # Open the image from bytes
        image.save(filename)  # Save to the specified filename
        print(f"Image saved to {filename}")
        return filename  # Return the filename on success
    except Exception as e:
        print(f"Error saving image: {e}")
        return None  # Or raise the exception if you prefer
