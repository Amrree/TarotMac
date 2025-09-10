"""
Py2app build script for creating macOS .app bundle.
"""

import sys
import os
from setuptools import setup

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

APP = ['app/main.py']
DATA_FILES = [
    ('db', ['db/canonical_deck.json']),
    ('docs', ['docs/README.md', 'docs/architecture.md', 'docs/ollama_setup.md']),
    ('tests', ['tests/unit/test_influence_engine.py']),
]

OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'app/assets/icon.icns',  # Will be created
    'plist': {
        'CFBundleName': 'Tarot',
        'CFBundleDisplayName': 'Tarot',
        'CFBundleIdentifier': 'com.tarotapp.tarot',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
        'NSRequiresAquaSystemAppearance': False,  # Support dark mode
        'LSMinimumSystemVersion': '12.0',  # macOS Monterey
        'NSHumanReadableCopyright': 'Copyright 2024 Tarot App. All rights reserved.',
        'NSAppleScriptEnabled': False,
        'NSSupportsAutomaticGraphicsSwitching': True,
    },
    'packages': [
        'PyObjC',
        'sqlalchemy',
        'ollama',
        'pydantic',
        'jsonschema',
        'cryptography',
        'keyring'
    ],
    'includes': [
        'app',
        'core',
        'ai',
        'db'
    ],
    'excludes': [
        'tkinter',
        'unittest',
        'test',
        'tests'
    ],
    'optimize': 2,
    'compressed': True,
    'strip': True,
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    name='Tarot',
    version='1.0.0',
    description='macOS Tarot Application with Local AI',
    author='Tarot App Team',
    author_email='team@tarotapp.com',
    url='https://github.com/tarotapp/tarot',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.10',
        'Topic :: Games/Entertainment',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)