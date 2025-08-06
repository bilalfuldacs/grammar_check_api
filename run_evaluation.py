#!/usr/bin/env python3

import asyncio
import sys
import os

sys.path.append(os.path.dirname(__file__))

from evaluation_framework import generate_evaluation_report

async def main():
    print("🚀 Grammar Check API Evaluation")
    print("=" * 50)
    print("This will evaluate your grammar checking system on:")
    print("✅ Accuracy - How well it detects grammar errors")
    print("✅ Performance - Response times and reliability")
    print("✅ Reliability - Error handling and edge cases")
    print("✅ API Endpoints - Functionality and documentation")
    print("\nMake sure your API is running: python -m uvicorn app.main:app --reload")
    print("=" * 50)
    
    try:
        await generate_evaluation_report()
    except Exception as e:
        print(f"\n❌ Evaluation failed: {e}")
        print("Make sure your API is running and accessible at http://localhost:8000")

if __name__ == "__main__":
    asyncio.run(main()) 