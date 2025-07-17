from io import BytesIO
from PIL import Image
from fpdf import FPDF

def save_bracket_to_pdf(image: Image.Image) -> bytes:
    """Converts a PIL image of the bracket to a downloadable PDF in memory."""
    buffer = BytesIO()
    image_rgb = image.convert("RGB")
    image_rgb.save(buffer, format="PNG")
    buffer.seek(0)

    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()

    # Save the image temporarily to load into PDF
    temp_img_path = "temp_bracket.png"
    with open(temp_img_path, "wb") as f:
        f.write(buffer.getvalue())

    pdf.image(temp_img_path, x=10, y=10, w=270)

    pdf_output = BytesIO()
    pdf.output(pdf_output)
    return pdf_output.getvalue()
