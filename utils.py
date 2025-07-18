from io import BytesIO
from PIL import Image
from fpdf import FPDF

def save_bracket_to_pdf(image: Image.Image) -> bytes:
    """Converts a PIL image of the bracket to a downloadable PDF in memory."""
    buffer = BytesIO()
    image_rgb = image.convert("RGB")
    image_rgb.save(buffer, format="PNG")
    buffer.seek(0)

    # Save to temporary PNG file
    temp_img_path = "temp_bracket.png"
    with open(temp_img_path, "wb") as f:
        f.write(buffer.getvalue())

    # Create PDF
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.image(temp_img_path, x=10, y=10, w=270)

    # Save to temp PDF and return its bytes
    temp_path = "bracket_output.pdf"
    pdf.output(temp_path)
    with open(temp_path, "rb") as f:
        return f.read()
# force rebuild
