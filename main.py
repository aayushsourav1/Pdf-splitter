import streamlit as st
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_filename, start_page, end_page):

  with open(input_filename, 'rb') as input_file:
    pdf_reader = PdfReader(input_file)
    num_pages = len(pdf_reader.pages)

    if start_page < 0 or end_page >= num_pages or start_page > end_page:
      return "Invalid page range. Please provide valid start and end page numbers."

    pdf_writer = PdfWriter()
    for page_num in range(start_page, end_page + 1):
      pdf_writer.add_page(pdf_reader.pages[page_num])

    # Create an in-memory stream for the PDF output
    output_stream = BytesIO()
    pdf_writer.write(output_stream)
    return output_stream.getvalue()  # Return the PDF content as bytes

def main():
  """
  Streamlit app for splitting PDFs with download functionality.
  """

  st.title("PDF Splitter App")

  uploaded_file = st.file_uploader("Choose a PDF file to split")
  if uploaded_file is not None:
    saved_filename = uploaded_file.name
    with open(saved_filename, "wb") as buffer:
      buffer.write(uploaded_file.getbuffer())

    start_page = st.number_input("Enter starting page number (0-based)", min_value=0)
    end_page = st.number_input("Enter ending page number (0-based)", min_value=0)

    if st.button("Split PDF"):
      pdf_content = split_pdf(saved_filename, start_page, end_page)
      if isinstance(pdf_content, str):  # Handle error message
        st.error(pdf_content)
      else:
        st.success("Successfully split PDF!")
        st.download_button(label="Download Split PDF", data=pdf_content, file_name="split.pdf")

if __name__ == "__main__":
  main()
