#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIX MASTER - ACOESPNGI TESTS (368 → 368 OK)
Corrige: BaseTestCase, datfinalvigencia, response.data['results'], self.eixo
"""

import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
TESTS_DIR = PROJECT_ROOT / "acoespngi" / "tests"

# 1. CORREÇÃO BaseTestCase (3 arquivos com ImportError)
BASETEST_FILES = [
    "testdiagnosticapi.py",
    "testwebacoesviews.py", 
    "testwebviewscomplete.py"
]

# 2. CORREÇÃO datfinalvigencia (ValidationError)
VIGENCIA_PATTERN = r"VigenciaPNGI\.objects\.create\([^)]*datiniciovigenciadate\([^)]*\)"

# 3. CORREÇÃO response.data['results'] → response.data['results'][0]
RESULTS_PATTERN = r"response\.data\['results'\]\.([a-zA-Z0-9_]+)"

# 4. CORREÇÃO self.eixo → self.eixo_base (AttributeError)
EIXO_PATTERN = r"self\.eixo\.([a-zA-Z0-9_]+)"

def fix_base_test_case(file_path):
    """Adiciona from .base_test_case import BaseTestCase"""
    content
