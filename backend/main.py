from fastapi import FastAPI, UploadFile, File
import fitz  # PyMuPDF

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Research Lit Tool backend is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    pdf_bytes = await file.read()

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    num_pages = doc.page_count  # grab this BEFORE closing

    full_text = ""
    for page in doc:
        full_text += page.get_text()

    doc.close()  # now safe to close

    return {
        "filename": file.filename,
        "num_pages": num_pages,
        "text_preview": full_text[:500],
        "full_text_length": len(full_text)
    }