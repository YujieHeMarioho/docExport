from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import io

app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory "database" for demonstration purposes
fake_documents_db = {
    "doc123": {
        "id": "doc123",
        "fields": [
            {"field_name": "Invoice Number", "value": "INV-001", "confidence": 0.95},
            {"field_name": "Vendor Name", "value": "ACME Corp", "confidence": 0.89},
            {"field_name": "Amount Due", "value": "100.00", "confidence": 0.99},
        ]
    },
    "doc456": {
        "id": "doc456",
        "fields": [
            {"field_name": "Patient Name", "value": "John Doe", "confidence": 0.98},
            {"field_name": "Date of Birth", "value": "1990-01-15", "confidence": 0.99},
            {"field_name": "Insurance ID", "value": "XYZ12345", "confidence": 0.85},
        ]
    }
}

@app.get("/", response_class=HTMLResponse)
async def index_page():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document Review App</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f7;
                color: #1d1d1f;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                padding: 30px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #1d1d1f;
                margin-bottom: 30px;
                font-weight: 600;
                text-align: center;
            }
            .document-link {
                background: linear-gradient(135deg, #007AFF 0%, #5856D6 100%);
                color: white;
                border: none;
                padding: 15px 20px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s ease;
                box-shadow: 0 2px 4px rgba(0, 122, 255, 0.3);
                margin: 10px 0;
                display: block;
                text-decoration: none;
                text-align: center;
            }
            .document-link:hover {
                transform: translateY(-1px);
                box-shadow: 0 4px 8px rgba(0, 122, 255, 0.4);
            }
            .document-link:active {
                transform: translateY(0);
            }
            .description {
                text-align: center;
                color: #86868b;
                margin-bottom: 30px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📄 Document Review App</h1>
            <p class="description">Select a document to review and export to Excel</p>
            <a href="/review/doc123" class="document-link">📋 Invoice Document (doc123)</a>
            <a href="/review/doc456" class="document-link">🏥 Medical Document (doc456)</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/api")
def read_root():
    return {"Hello": "World"}

@app.get("/api/v1/export/documents/{document_id}/{format}")
async def export_document(document_id: str, format: str):
    if format.lower() != "excel":
        return {"error": "Only Excel format is supported"}

    document = fake_documents_db.get(document_id)
    if not document:
        return {"error": "Document not found"}

    df = pd.DataFrame(document["fields"])

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Extraction Results')
    
    output.seek(0)
    
    headers = {
        'Content-Disposition': f'attachment; filename="{document_id}.xlsx"'
    }

    return StreamingResponse(output, headers=headers, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.get("/api/v1/review/documents/{document_id}")
async def get_document(document_id: str):
    document = fake_documents_db.get(document_id)
    if not document:
        return {"error": "Document not found"}
    return document

@app.get("/review/{document_id}", response_class=HTMLResponse)
async def review_page(document_id: str):
    document = fake_documents_db.get(document_id)
    if not document:
        return HTMLResponse(content="<h1>Document not found</h1>", status_code=404)
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document Review - {document_id}</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f7;
                color: #1d1d1f;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                padding: 30px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #1d1d1f;
                margin-bottom: 30px;
                font-weight: 600;
            }}
            .field {{
                background: #f5f5f7;
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
                border-left: 4px solid #007AFF;
            }}
            .field-name {{
                font-weight: 600;
                color: #1d1d1f;
                margin-bottom: 5px;
            }}
            .field-value {{
                color: #86868b;
                font-size: 14px;
            }}
            .confidence {{
                color: #007AFF;
                font-size: 12px;
                margin-top: 5px;
            }}
            .export-button {{
                background: linear-gradient(135deg, #34C759 0%, #30D158 100%);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s ease;
                box-shadow: 0 2px 4px rgba(52, 199, 89, 0.3);
                margin-top: 20px;
                display: inline-block;
                text-decoration: none;
            }}
            .export-button:hover {{
                transform: translateY(-1px);
                box-shadow: 0 4px 8px rgba(52, 199, 89, 0.4);
            }}
            .export-button:active {{
                transform: translateY(0);
            }}
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Document Review</h1>
                <a href="/api/v1/export/documents/{document_id}/excel" class="export-button">
                    📊 Export to Excel
                </a>
            </div>
            <div class="document-info">
                <h2>Document ID: {document_id}</h2>
                <p>Found {len(document['fields'])} extracted fields</p>
            </div>
            <div class="fields">
    """
    
    for field in document['fields']:
        confidence_percentage = int(field['confidence'] * 100)
        html_content += f"""
                <div class="field">
                    <div class="field-name">{field['field_name']}</div>
                    <div class="field-value">{field['value']}</div>
                    <div class="confidence">Confidence: {confidence_percentage}%</div>
                </div>
        """
    
    html_content += """
            </div>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)
