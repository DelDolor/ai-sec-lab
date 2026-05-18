from fastapi import FastAPI

app = FastAPI(
    title="RAG Ingestion",
    description="PDF ingestion pipeline: extract, chunk, embed, and upload to Qdrant.",
)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "rag-ingestion"}


# Placeholder: real implementation will add a POST /ingest endpoint or a CLI entry point
# that reads PDFs from /data/documents/, extracts and chunks text, generates embeddings
# via a local model, and uploads chunks with metadata to Qdrant.
# No file processing is implemented in this placeholder.
