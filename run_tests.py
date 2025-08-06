#!/usr/bin/env python3
"""
Simple test runner for Grammar Check API
"""

import asyncio
import sys
import os

# Add app directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Import and run the test
from tests.test import main

if __name__ == "__main__":
    print("🧪 Running Grammar Check API Tests")
    print("=" * 50)
    asyncio.run(main()) 