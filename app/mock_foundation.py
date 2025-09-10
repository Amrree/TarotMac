"""
Mock Foundation module for testing when PyObjC is not available.
"""

import sys
from unittest.mock import Mock

# Create mock Foundation module
foundation_module = type(sys)('Foundation')

# Mock NSObject
class NSObject:
    def __init__(self):
        pass
    
    def init(self):
        return self

# Add NSObject to the module
foundation_module.NSObject = NSObject

# Add to sys.modules
sys.modules['Foundation'] = foundation_module

# Export the module
__all__ = ['foundation_module']