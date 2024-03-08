from PIL import Image, ImageDraw, ImageFont

# Define text content
text = "Your Text Here"

# Define desired thumbnail size
thumbnail_size = (200, 200)

# Load and resize image
image = Image.open("lofi_maker/images/lofi_cover.jpg").copy()
image.thumbnail(thumbnail_size, Image.LANCZOS)

# Create a new image with transparent background for the text overlay
text_image = Image.new("RGBA", thumbnail_size, (255, 255, 255, 0))

# Load the custom font
font_path = "path/to/your/custom/font.ttf"  # Replace with the correct path
# try:
font = ImageFont.truetype("Ariel.ttf", size=30)
# except OSError:
#    print(f"Error loading font: {font_path}")
#    print("Try using an absolute path or check if the file exists.") 

# Draw the text onto the text_image
draw = ImageDraw.Draw(text_image)
text_width, text_height = draw.textsize(text, font=font)
x_offset = (thumbnail_size[0] - text_width) // 2
y_offset = (thumbnail_size[1] - text_height) // 2
draw.text((x_offset, y_offset), text, font=font, fill=(0, 0, 0, 255))

# Combine the image and text_image using alpha compositing
final_image = Image.alpha_composite(image, text_image)

# Save the final thumbnail image
final_image.save("path/to/your/thumbnail.jpg", "JPEG")

print("Thumbnail created successfully!")
