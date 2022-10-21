#!/usr/bin/env python3
from gen_invoice import InvoiceGenerator, Utility

# Our output file paths
OUTFILE_HTML = "/path/to/output.html"
OUTFILE_PDF = "/path/to/output.pdf"

# Load our template and stylesheet data from file
template = Utility.read_file("template.html")
stylesheet = Utility.read_file("stylesheet.css")

# Generate our invoice
generator = InvoiceGenerator()
generator.generate(
  
  # Our output HTML file
  outfile = OUTFILE_HTML,
  
  # Our invoice number
  number = "INV001",
  
  # Our line items
  items = [
    {
      "Section": "Materials",
      "Item": "Widget A",
      "Quantity": "20",
      "Units": "pcs",
      "Price": "12.99"
    }
  ],
  
  # Our payee details
  payee = {
    "name": "XYZ Widget Company",
    "identifier": "123456789",
    "email": "domestic@example.com",
    "address": [
      "1 Widget Road",
      "Widgetville",
      "WID 9999"
    ],
    "bank": {
      "holder": "XYZ Widget Company",
      "bank": "Acme Banking Co",
      "code": "123-456",
      "account": "192837465"
    }
  },
  
  # Our payer details
  payer = {
    "name": "XYZ Widget Company",
    "address": [
      "1 Widget Road",
      "Widgetville",
      "WID 9999"
    ],
    "due": "Within 30 days of receipt"
  },
  
  # Our template and stylesheet
  template = template,
  stylesheet = stylesheet,
  
  # No tax
  tax = 0.0,
  
  # Generate a domestic invoice rather than an international one
  is_international = False,
  
  # Generate an invoice rather than a quote
  is_quote = False
)

# Render the invoice HTML to a PDF file using electron-pdf
generator.render(OUTFILE_HTML, OUTFILE_PDF)