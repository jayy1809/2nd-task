from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
from fastapi import HTTPException

def generate_pdf(product_data: dict):
    try:

        env = Environment(loader=FileSystemLoader('app/templates'))

        template = env.get_template('product_template.html')
        
        html_content = template.render(product=product_data)
        
        pdf = HTML(string=html_content).write_pdf()
        
        return pdf
    except Exception as e:
        print(f"Error generating PDF: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error while generating PDF"
        )