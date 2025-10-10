from utils import pdf_to_markdown

pdf_path = "/Users/ritvik/Downloads/pdf2markdown/Deep Learning - Motion Detection Project.pdf"     

md_content = pdf_to_markdown(pdf_path)
md_path = pdf_path.replace('.pdf', '.md')
with open(md_path, 'w', encoding='utf-8') as md_file:
    md_file.write(md_content)

print(f"Conversion complete! Markdown saved to: {md_path}")
