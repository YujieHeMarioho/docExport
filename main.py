from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import io
import json

app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory "database" for demonstration purposes
new_data = {
  "analysis_result": {
    "account_summary": {
      "ending_balance": 75432.10,
      "starting_balance": 78543.21,
      "total_charges_and_debits": 42876.45,
      "total_fees": 0.0,
      "total_interest_earned": None,
      "total_payments_and_credits": 39765.34,
      "transaction_counts": 30
    },
    "period_info": {
      "ending_year": 2024,
      "starting_year": 2024,
      "statement_date": "2024-03-31",
      "statement_end_date": "2024-03-31",
      "statement_start_date": "2024-03-01"
    },
    "statement_info": {
      "account_number": "1234567890",
      "bank_address": "P.O. Box 1234\\nSeattle, WA 98101-1234",
      "bank_name": "FIRST\\nNATIONAL",
      "client_address": "123 MAIN ST\\nSEATTLE WA 98101-1234",
      "client_name": "ACME HEALTHCARE GROUP, INC."
    },
    "transactions": [
      {
        "credit_amount": 425.67,
        "debit_amount": None,
        "description": "BlueCross BlueShield Hcclaimpmt 091000010401234\\nTRN*1*12345678*1411242261*2337A0061~",
        "transaction_date": "2024-03-15",
        "transaction_type": None
      },
      {
        "credit_amount": 2800.0,
        "debit_amount": None,
        "description": "HealthPlan Insurance Hcclaimpmt xxxxx1234\\nTRN*1*25043B1000371103*1362739571*000012345\\\\",
        "transaction_date": "2024-03-15",
        "transaction_type": None
      },
      {
        "credit_amount": 2800.0,
        "debit_amount": None,
        "description": "HealthPlan Insurance Hcclaimpmt xxxxx1234\\nTRN*1*25043B1000943691*1362739571*0000Abcde\\\\",
        "transaction_date": "2024-03-15",
        "transaction_type": None
      },
      {
        "credit_amount": 3456.78,
        "debit_amount": None,
        "description": "State of WA WA Dhs Nfo xxxxx5678\\n344136\\\\SE*14*069873386\\\\GE*1*069873386\\\\lea*1*06987",
        "transaction_date": "2024-03-15",
        "transaction_type": None
      },
      {
        "credit_amount": None,
        "debit_amount": 189.0,
        "description": "QuickBooks * Payroll 240315 1045604 Acme Healthcare Group, IN",
        "transaction_date": "2024-03-15",
        "transaction_type": None
      },
      {
        "credit_amount": 350.0,
        "debit_amount": None,
        "description": "HealthPlan Insurance Hcclaimpmt xxxxx1234\\nTRN*1*25045B1000161194*1362739571*000012345\\\\",
        "transaction_date": "2024-03-18",
        "transaction_type": None
      },
      {
        "credit_amount": 350.0,
        "debit_amount": None,
        "description": "HealthPlan Insurance Hcclaimpmt xxxxx1234\\nTRN*1*S5749019*1411289245*000054321\\\\",
        "transaction_date": "2024-03-18",
        "transaction_type": None
      },
      {
        "credit_amount": 900.0,
        "debit_amount": None,
        "description": "HealthPlan Insurance Hcclaimpmt xxxxx1234\\nTRN*1*25045B1000425960*1362739571*0000Abcde\\\\",
        "transaction_date": "2024-03-18",
        "transaction_type": None
      },
      {
        "credit_amount": 1600.0,
        "debit_amount": None,
        "description": "HealthPlan Insurance Hcclaimpmt xxxxx1234\\nTRN*1*25044B1000208847*1362739571*000012345\\\\",
        "transaction_date": "2024-03-18",
        "transaction_type": None
      },
      {
        "credit_amount": 2100.0,
        "debit_amount": None,
        "description": "HealthPlan Insurance Hcclaimpmt xxxxx1234\\nTRN*1*25044B1000512150*1362739571*0000Abcde\\\\",
        "transaction_date": "2024-03-18",
        "transaction_type": None
      },
      {
        "credit_amount": 2543.21,
        "debit_amount": None,
        "description": "WA Claims Hcclaimpmt 240319\\nTRN*1*0901377725*1464829006\\\\",
        "transaction_date": "2024-03-19",
        "transaction_type": None
      },
      {
        "credit_amount": 234.56,
        "debit_amount": None,
        "description": "Community Health Hcclaimpmt xxxxx1234\\nTRN*1*25050B1000846162*1470676824*0000Abcde\\\\",
        "transaction_date": "2024-03-21",
        "transaction_type": None
      },
      {
        "credit_amount": 350.0,
        "debit_amount": None,
        "description": "HealthPlan Insurance Hcclaimpmt xxxxx1234\\nTRN*1*25050B1000319828*1362739571*000012345\\\\",
        "transaction_date": "2024-03-21",
        "transaction_type": None
      },
      {
        "credit_amount": 450.0,
        "debit_amount": None,
        "description": "HealthPlan Insurance Hcclaimpmt xxxxx1234\\nTRN*1*S5979915*1411289245*000054321\\\\",
        "transaction_date": "2024-03-21",
        "transaction_type": None
      },
      {
        "credit_amount": 3021.45,
        "debit_amount": None,
        "description": "State of WA WA Dhs Nfo xxxxx9876\\n344136\\\\SE*14*069942128\\\\GE*1*069942128\\\\lea*1*06994",
        "transaction_date": "2024-03-21",
        "transaction_type": None
      },
      {
        "credit_amount": None,
        "debit_amount": 225.67,
        "description": "Business to Business ACH Debit - 12345 Acme HC Billing\\n240321 12345 Acme Healthcare Group, IN",
        "transaction_date": "2024-03-21",
        "transaction_type": None
      },
      {
        "credit_amount": None,
        "debit_amount": 6542.18,
        "description": "Business to Business ACH Debit - Paylocity Corpor Tax Col First\\nNational Bank, N.A",
        "transaction_date": "2024-03-21",
        "transaction_type": None
      },
      {
        "credit_amount": None,
        "debit_amount": 19876.54,
        "description": "Business to Business ACH Debit - 12345 Acme HC Dir Dep\\n240321 12345 Acme Healthcare Group, IN",
        "transaction_date": "2024-03-21",
        "transaction_type": None
      },
      {
        "credit_amount": 267.89,
        "debit_amount": None,
        "description": "Community Health Hcclaimpmt xxxxx1234\\nTRN*1*25051B1000424105*1470676824*0000Abcde\\\\",
        "transaction_date": "2024-03-24",
        "transaction_type": None
      },
      {
        "credit_amount": 1623.45,
        "debit_amount": None,
        "description": "ATM Check Deposit on 03/24 18030 R Plz Seattle WA 0005889\\nATM ID 9959R Card 1234",
        "transaction_date": "2024-03-24",
        "transaction_type": None
      },
      {
        "credit_amount": 450.0,
        "debit_amount": None,
        "description": "HealthPlan Insurance Hcclaimpmt xxxxx1234\\nTRN*1*S6167869*1411289245*000054321\\\\",
        "transaction_date": "2024-03-25",
        "transaction_type": None
      },
      {
        "credit_amount": 4205.67,
        "debit_amount": None,
        "description": "ATM Check Deposit on 03/25 18030 R Plz Seattle WA 0006030\\nATM ID 9959R Card 1234",
        "transaction_date": "2024-03-25",
        "transaction_type": None
      },
      {
        "credit_amount": None,
        "debit_amount": 18.0,
        "description": None,
        "transaction_date": "2024-03-25",
        "transaction_type": None
      },
      {
        "credit_amount": 525.0,
        "debit_amount": None,
        "description": "WA Claims Hcclaimpmt 240327\\nTRN*1*0901381543*1464829006\\\\",
        "transaction_date": "2024-03-27",
        "transaction_type": None
      },
      {
        "credit_amount": 350.0,
        "debit_amount": None,
        "description": "HealthPlan Insurance Hcclaimpmt xxxxx1234\\nTRN*1*S6330348*1411289245*000054321\\\\",
        "transaction_date": "2024-03-28",
        "transaction_type": None
      },
      {
        "credit_amount": 511.23,
        "debit_amount": None,
        "description": "WA Claims Hcclaimpmt 240328\\nTRN*1*0901384013*1464829006\\\\",
        "transaction_date": "2024-03-28",
        "transaction_type": None
      },
      {
        "credit_amount": 1150.0,
        "debit_amount": None,
        "description": "HealthPlan Insurance Hcclaimpmt xxxxx1234\\nTRN*1*S6406776*1411289245*000054321\\\\",
        "transaction_date": "2024-03-28",
        "transaction_type": None
      },
      {
        "credit_amount": 1400.0,
        "debit_amount": None,
        "description": "HealthPlan Insurance Hcclaimpmt xxxxx1234\\nTRN*1*25057B1000343328*1362739571*000012345\\\\",
        "transaction_date": "2024-03-28",
        "transaction_type": None
      },
      {
        "credit_amount": 2632.87,
        "debit_amount": None,
        "description": "State of WA WA Dhs Nfo xxxxx4567\\n344136\\\\SE*14*070012591\\\\GE*1*070012591\\\\lea*1*07001",
        "transaction_date": "2024-03-28",
        "transaction_type": None
      },
      {
        "credit_amount": 3611.28,
        "debit_amount": None,
        "description": "HealthPlan Insurance Hcclaimpmt xxxxx1234\\nTRN*1*25057B1000886445*1362739571*0000Abcde\\\\",
        "transaction_date": "2024-03-28",
        "transaction_type": None
      }
    ]
  }
}

bank_statement_fields = []
analysis_result = new_data["analysis_result"]

for section, data in analysis_result.items():
    if section != "transactions":
        for key, value in data.items():
            bank_statement_fields.append({
                "field_name": f"{section.replace('_', ' ').title()} - {key.replace('_', ' ').title()}",
                "value": str(value),
                "confidence": 1.0
            })

fake_documents_db = {
    "bank_statement_2024_03": {
        "id": "bank_statement_2024_03",
        "fields": bank_statement_fields,
        "transactions": analysis_result["transactions"]
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
            <a href="/review/bank_statement_2024_03" class="document-link">🏦 Bank Statement (March 2024)</a>
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

    # Create a Pandas Excel writer using openpyxl as the engine
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Export main fields
        main_fields_df = pd.DataFrame(document["fields"])
        main_fields_df.to_excel(writer, index=False, sheet_name='Summary')
        
        # Export transactions
        transactions_df = pd.DataFrame(document["transactions"])
        transactions_df.to_excel(writer, index=False, sheet_name='Transactions')

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
                <p>Found {len(document['fields'])} summary fields and {len(document['transactions'])} transactions.</p>
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
            <h2>Transactions</h2>
            <div class="transactions-table" style="overflow-x:auto;">
                <table style="width:100%; border-collapse: collapse;">
                    <tr style="background-color: #f5f5f7;">
                        <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Date</th>
                        <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Description</th>
                        <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Debit</th>
                        <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Credit</th>
                    </tr>
    """
    for tx in document['transactions']:
        debit = tx['debit_amount'] if tx['debit_amount'] is not None else ""
        credit = tx['credit_amount'] if tx['credit_amount'] is not None else ""
        html_content += f"""
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ddd;">{tx['transaction_date']}</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">{tx['description']}</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">{debit}</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">{credit}</td>
                    </tr>
        """
    html_content += """
                </table>
            </div>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)
