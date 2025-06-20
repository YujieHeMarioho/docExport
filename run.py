#!/usr/bin/env python3
"""
Simple startup script for the Document Review App
Run this with: python3 run.py
"""

import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Document Review App...")
    print("📱 Open your browser and go to: http://localhost:8000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 