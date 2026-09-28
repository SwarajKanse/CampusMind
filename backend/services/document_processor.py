"""Document parsing and text chunking service."""
import io
from config import settings


class DocumentProcessor:
    def process(self, content: bytes, filename: str) -> list[str]:
        """Parse document and split into chunks."""
        if filename.lower().endswith(".pdf"):
            text = self._extract_pdf(content)
        else:
            text = content.decode("utf-8", errors="ignore")
        return self._chunk_text(text)

    def _extract_pdf(self, content: bytes) -> str:
        """Extract text from PDF using PyMuPDF (fitz) or pypdf fallback."""
        try:
            try:
                import pymupdf as fitz
            except ImportError:
                import fitz
            doc = fitz.open(stream=content, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        except ImportError:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(content))
            return "\n".join(page.extract_text() or "" for page in reader.pages)

    def _chunk_text(self, text: str) -> list[str]:
        """Split text into overlapping chunks of words."""
        words = text.split()
        chunks = []
        chunk_size = settings.CHUNK_SIZE
        overlap = settings.CHUNK_OVERLAP
        i = 0
        while i < len(words):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
            i += chunk_size - overlap
        return chunks
