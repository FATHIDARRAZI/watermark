from PIL import Image, ImageDraw, ImageFont, ImageEnhance

def add_text_watermark(input_image_path, output_image_path, text, opacity=0.5, scale_factor=0.9, watermark_type='single'):
    try:
        original = Image.open(input_image_path).convert("RGBA")
        original_width, original_height = original.size

        # Create a transparent image for the text watermark
        text_overlay = Image.new("RGBA", original.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(text_overlay)

        # Load a font
        font_size = int(original_width * scale_factor)
        font = ImageFont.truetype("arial.ttf", font_size)

        # Calculate text size and position
        text_width, text_height = draw.textsize(text, font=font)
        position = ((original_width - text_width) // 2, (original_height - text_height) // 2)

        # Draw the text on the transparent image
        draw.text(position, text, font=font, fill=(255, 255, 255, int(255 * opacity)))

        if watermark_type == 'loop':
            spacing = int(text_width * 1.5)
            for y in range(0, original_height, spacing):
                for x in range(0, original_width, spacing):
                    draw.text((x, y), text, font=font, fill=(255, 255, 255, int(255 * opacity)))

        # Combine the original image with the text overlay
        watermarked = Image.alpha_composite(original, text_overlay)
        watermarked.convert("RGB").save(output_image_path, "JPEG")
    except Exception as e:
        raise Exception(f"Failed to add text watermark: {e}")
