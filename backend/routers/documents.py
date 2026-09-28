"""
Document upload and management router.
Covers CN Exp 5 (checksum validation) and CN Exp 9 (file transfer).
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Document
from services.checksum_service import ChecksumService
from services.document_processor import DocumentProcessor

router = APIRouter()
checksum_svc = ChecksumService()
doc_processor = DocumentProcessor()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload academic document (PDF/TXT), compute checksums, chunk text."""
    content = await file.read()

    # CN Exp 5: Compute multiple checksums for integrity verification
    file_hash = checksum_svc.sha256(content)
    crc = checksum_svc.crc32(content)
    icksum = checksum_svc.internet_checksum(content)

    # Check for duplicates via hash
    existing = db.query(Document).filter(Document.file_hash == file_hash).first()
    if existing:
        raise HTTPException(
            status_code=409,
            detail="Document already exists (duplicate SHA-256 hash)"
        )

    # Process and chunk the document
    chunks = doc_processor.process(content, file.filename)

    # Store metadata in DB
    doc = Document(
        filename=file.filename,
        file_hash=file_hash,
        chunk_count=len(chunks),
        file_size=len(content),
        status="pending_embedding"
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return {
        "id": doc.id,
        "filename": file.filename,
        "chunks": len(chunks),
        "sha256": file_hash,
        "crc32": hex(crc),
        "internet_checksum": hex(icksum),
        "status": doc.status,
    }


@router.get("/list")
async def list_documents(db: Session = Depends(get_db)):
    """List all uploaded documents."""
    docs = db.query(Document).all()
    return [
        {
            "id": d.id,
            "filename": d.filename,
            "chunks": d.chunk_count,
            "size": d.file_size,
            "status": d.status,
            "uploaded": str(d.uploaded_at),
        }
        for d in docs
    ]


@router.delete("/{doc_id}")
async def delete_document(doc_id: int, db: Session = Depends(get_db)):
    """Delete a document by ID."""
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(doc)
    db.commit()
    return {"message": f"Deleted document {doc_id}"}
