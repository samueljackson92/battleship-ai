try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os.path

config = {
    'description': 'Co-ranking matricies for Python',
    'author': 'Samuel Jackson',
    'url': 'http://github.com/samueljackson92/battleship-ai',
    'download_url': 'http://github.com/samueljackson92/battleship-ai',
    'author_email': 'samueljackson@outlook.com',
    'version': '0.1.0',
    'install_requires': [
	    'Click',
        'numpy',
	    'selenium==2.48',
	    'beautifulsoup4'
    ],
    'entry_points':'''
        [console_scripts]
        battleship=battleshipai.command:cli
    ''',
    'packages': ['battleshipai'],
    'name': 'battleship-ai'
}

setup(**config)
