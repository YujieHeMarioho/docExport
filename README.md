# 📄 Document Review App

A simple FastAPI application for reviewing and exporting document data to Excel format.

## 🚀 Features

- View extracted document data with confidence scores
- Export data to Excel format with one click
- Beautiful Apple-style web interface
- RESTful API endpoints
- Real-time server reloading

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## 🛠️ Installation

1. **Clone or download** this project to your computer

2. **Navigate** to the project directory:

   ```bash
   cd document_review_app
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   If `pip` doesn't work, try:

   ```bash
   pip3 install -r requirements.txt
   ```

## 🏃‍♂️ Running the Application

### Option 1: Simple Startup Script (Recommended)

```bash
python3 run.py
```

or

```bash
python run.py
```

### Option 2: Direct Uvicorn Command

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Then Open Your Browser

Go to: `http://localhost:8000`

## 🌐 Available Endpoints

### Web Interface

- **Homepage**: `http://localhost:8000/`
- **Document Review**: `http://localhost:8000/review/{document_id}`

### API Endpoints

- **Get Document Data**: `GET /api/v1/review/documents/{document_id}`
- **Export to Excel**: `GET /api/v1/export/documents/{document_id}/excel`

## 📁 Sample Documents

The app comes with 2 sample documents:

- **doc123**: Invoice document (Invoice Number, Vendor Name, Amount Due)
- **doc456**: Medical document (Patient Name, Date of Birth, Insurance ID)

## 🎨 Features

- **Responsive Design**: Works on desktop and mobile
- **Apple-style UI**: Clean, modern interface
- **Real-time Updates**: Server automatically reloads when you make changes
- **Excel Export**: One-click download of document data

## 🔧 Customization

To add your own documents, edit the `fake_documents_db` dictionary in `main.py`:

```python
fake_documents_db = {
    "your_doc_id": {
        "id": "your_doc_id",
        "fields": [
            {"field_name": "Your Field", "value": "Your Value", "confidence": 0.95},
        ]
    }
}
```

## 🐛 Troubleshooting

### Port Already in Use

If you get an error about port 8000 being in use, try a different port:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### Package Installation Issues

If you have trouble installing packages:

```bash
python -m pip install -r requirements.txt
```

## 📝 Project Structure

```
document_review_app/
├── main.py              # Main application code
├── run.py               # Simple startup script
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── static/             # Static files directory (created automatically)
```

## 🤝 Contributing

Feel free to modify and improve this project!

## 📄 License

This project is open source and available under the MIT License.
