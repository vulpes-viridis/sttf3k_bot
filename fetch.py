from urllib.request import urlretrieve
import pypdfium2 as pdfium
import re


def fetch_timetable(vn):
    url = f"https://lpi.sfu-kras.ru/files/page_files/1_ius-mie_{vn}n.pdf"
    urlretrieve(url, "pdf.pdf")

    # делает из первой страницы нормальный пацанский битмап
    pdf = pdfium.PdfDocument("pdf.pdf")
    img = pdf[0].render(scale=4).to_pil()

    # уууу волшебные числа
    width, height = img.size
    left = 510
    top = height / 14
    right = width / 2
    bottom = height * 0.955

    cropped = img.crop((left, top, right, bottom))
    cropped.save("./jpeg.jpeg")

    return "jpeg.jpeg"


def find_date(pdf="pdf.pdf"):
    # не слишком конкретно, но здесь прокатывает
    date_pattern = r"\d+\.\d+\.\d+"

    pdf = pdfium.PdfDocument(pdf)
    head = pdf.get_page(0).get_textpage().get_text_range(count=200)

    match = re.search(date_pattern, head)
    if match:
        return match.group()
    else:
        return "??.??.????"
