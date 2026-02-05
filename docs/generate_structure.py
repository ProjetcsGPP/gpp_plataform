#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script standalone para gerar documentacao da estrutura de aplicacoes.

Uso:
    python docs/generate_structure.py
    python docs/generate_structure.py --output /caminho/docs
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import ast
import re
import argparse


class AppStructureAnalyzer:
    """Analisa estrutura de aplicacoes Django."""

    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.apps = []

    def find_apps(self):
        """Encontra todas as aplicacoes Django no projeto."""
        for item in self.project_root.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                # Verificar se tem apps.py
                apps_file = item / 'apps.py'
                if apps_file.exists():
                    self.apps.append(item)
        return self.apps

    def analyze_app(self, app_path):
        """Analisa estrutura de um app."""
        app_name = app_path.name
        app_data = {
            'name': app_name,
            'path': str(app_path),
            'files': {},
            'models': [],
            'views': [],
            'viewsets': [],
            'serializers': [],
            'urls': [],
            'forms': [],
            'admin': [],
            'signals': []
        }

        # Models
        models_file = app_path / 'models.py'
        if models_file.exists():
            app_data['models'] = self._extract_models(models_file)
            app_data['files']['models.py'] = True

        models_dir = app_path / 'models'
        if models_dir.exists():
            app_data['files']['models/'] = True
            for f in models_dir.glob('*.py'):
                if f.name != '__init__.py':
                    app_data['models'].extend(self._extract_models(f))

        # Views
        views_file = app_path / 'views.py'
        if views_file.exists():
            views_data = self._extract_views(views_file)
            app_data['views'].extend(views_data['views'])
            app_data['viewsets'].extend(views_data['viewsets'])
            app_data['files']['views.py'] = True

        views_dir = app_path / 'views'
        if views_dir.exists():
            app_data['files']['views/'] = True
            for f in views_dir.glob('*.py'):
                if f.name != '__init__.py':
                    views_data = self._extract_views(f)
                    app_data['views'].extend(views_data['views'])
                    app_data['viewsets'].extend(views_data['viewsets'])

        # Serializers
        serializers_file = app_path / 'serializers.py'
        if serializers_file.exists():
            app_data['serializers'] = self._extract_classes(serializers_file)
            app_data['files']['serializers.py'] = True

        # URLs
        urls_file = app_path / 'urls.py'
        if urls_file.exists():
            app_data['urls'] = self._extract_urls(urls_file)
            app_data['files']['urls.py'] = True

        urls_init = app_path / 'urls' / '__init__.py'
        if urls_init.exists():
            app_data['urls'].extend(self._extract_urls(urls_init))
            app_data['files']['urls/'] = True

        # Forms
        forms_file = app_path / 'forms.py'
        if forms_file.exists():
            app_data['forms'] = self._extract_classes(forms_file)
            app_data['files']['forms.py'] = True

        # Admin
        admin_file = app_path / 'admin.py'
        if admin_file.exists():
            app_data['admin'] = self._extract_classes(admin_file)
            app_data['files']['admin.py'] = True

        # Signals
        signals_file = app_path / 'signals.py'
        if signals_file.exists():
            app_data['signals'] = self._extract_functions(signals_file)
            app_data['files']['signals.py'] = True

        # Estrutura
        app_data['structure_tree'] = self._build_tree(app_path)

        return app_data

    def _extract_models(self, file_path):
        """Extrai models de um arquivo."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())

            models = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    for base in node.bases:
                        base_name = self._get_name(base)
                        if 'Model' in base_name or 'AbstractModel' in base_name:
                            models.append({
                                'name': node.name,
                                'line': node.lineno,
                                'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef) and not n.name.startswith('_')]
                            })
            return models
        except Exception as e:
            print(f"Erro ao analisar {file_path}: {e}", file=sys.stderr)
            return []

    def _extract_views(self, file_path):
        """Extrai views e viewsets de um arquivo."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())

            views = []
            viewsets = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    views.append({
                        'name': node.name,
                        'type': 'function',
                        'line': node.lineno
                    })
                elif isinstance(node, ast.ClassDef):
                    for base in node.bases:
                        base_name = self._get_name(base)
                        if 'View' in base_name or 'APIView' in base_name:
                            views.append({
                                'name': node.name,
                                'type': 'class',
                                'line': node.lineno,
                                'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef) and not n.name.startswith('_')]
                            })
                        elif 'ViewSet' in base_name or 'ModelViewSet' in base_name:
                            viewsets.append({
                                'name': node.name,
                                'line': node.lineno,
                                'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef) and not n.name.startswith('_')]
                            })
            return {'views': views, 'viewsets': viewsets}
        except Exception as e:
            print(f"Erro ao analisar {file_path}: {e}", file=sys.stderr)
            return {'views': [], 'viewsets': []}

    def _extract_classes(self, file_path):
        """Extrai classes de um arquivo."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())

            classes = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.append({
                        'name': node.name,
                        'line': node.lineno,
                        'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef) and not n.name.startswith('_')]
                    })
            return classes
        except Exception:
            return []

    def _extract_functions(self, file_path):
        """Extrai funcoes de um arquivo."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())

            functions = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
                    functions.append({
                        'name': node.name,
                        'line': node.lineno
                    })
            return functions
        except Exception:
            return []

    def _extract_urls(self, file_path):
        """Extrai patterns de URL."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            urls = []
            path_pattern = r"path\(['\"]([^'\"]*)['\"][,)]"
            for match in re.finditer(path_pattern, content):
                urls.append(match.group(1))

            re_path_pattern = r"re_path\(r?['\"]([^'\"]*)['\"][,)]"
            for match in re.finditer(re_path_pattern, content):
                urls.append(match.group(1))

            return urls
        except Exception:
            return []

    def _get_name(self, node):
        """Extrai nome de um node AST."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return node.attr
        return ''

    def _build_tree(self, path, prefix="", max_depth=2, current_depth=0):
        """Constroi arvore de diretorios."""
        if current_depth >= max_depth:
            return ""

        lines = []
        try:
            items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
            for i, item in enumerate(items):
                if item.name.startswith('.') or item.name.startswith('__pycache__'):
                    continue

                is_last = i == len(items) - 1
                current = "└─" if is_last else "├─"
                next_prefix = prefix + ("  " if is_last else "│ ")

                if item.is_dir():
                    lines.append(f"{prefix}{current}{item.name}/")
                    if current_depth + 1 < max_depth:
                        subtree = self._build_tree(item, next_prefix, max_depth, current_depth + 1)
                        if subtree:
                            lines.append(subtree)
                else:
                    lines.append(f"{prefix}{current}{item.name}")
        except PermissionError:
            pass

        return "\n".join(lines)

    def generate_markdown(self, output_file):
        """Gera documentacao em Markdown."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# 📦 Estrutura de Aplicacoes\n\n")
            f.write(f"**Gerado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # Indice
            f.write("## 📚 Indice\n\n")
            for app in self.apps:
                app_name = app.name
                f.write(f"- [{app_name}](#{app_name})\n")
            f.write("\n")

            # Detalhes
            for app in self.apps:
                app_data = self.analyze_app(app)
                self._write_app_section(f, app_data)

    def _write_app_section(self, f, app_data):
        """Escreve secao de uma app no markdown."""
        f.write(f"## {app_data['name']}\n\n")
        f.write(f"**Path:** `{app_data['path']}`\n\n")

        # Models
        if app_data['models']:
            f.write(f"### 📊 Models ({len(app_data['models'])})\n\n")
            for model in app_data['models']:
                f.write(f"- `{model['name']}` (linha {model['line']})\n")
                if model['methods']:
                    f.write(f"  - Métodos: {', '.join(model['methods'])}\n")
            f.write("\n")

        # Views
        if app_data['views']:
            f.write(f"### 👁️ Views ({len(app_data['views'])})\n\n")
            for view in app_data['views']:
                f.write(f"- `{view['name']}` ({view['type']})\n")
                if view.get('methods'):
                    f.write(f"  - Métodos: {', '.join(view['methods'])}\n")
            f.write("\n")

        # ViewSets
        if app_data['viewsets']:
            f.write(f"### 🌠 ViewSets ({len(app_data['viewsets'])})\n\n")
            for vs in app_data['viewsets']:
                f.write(f"- `{vs['name']}`\n")
                if vs['methods']:
                    f.write(f"  - Ações: {', '.join(vs['methods'])}\n")
            f.write("\n")

        # Serializers
        if app_data['serializers']:
            f.write(f"### 📝 Serializers ({len(app_data['serializers'])})\n\n")
            for ser in app_data['serializers']:
                f.write(f"- `{ser['name']}`\n")
            f.write("\n")

        # URLs
        if app_data['urls']:
            f.write(f"### 🌐 URLs ({len(app_data['urls'])})\n\n")
            for url in app_data['urls'][:15]:
                f.write(f"- `{url}`\n")
            if len(app_data['urls']) > 15:
                f.write(f"- ... e mais {len(app_data['urls']) - 15}\n")
            f.write("\n")

        # Estrutura
        if app_data['structure_tree']:
            f.write(f"### 📁 Estrutura\n\n```\n{app_data['structure_tree']}\n```\n\n")

        f.write("---\n\n")

    def generate_json(self, output_file):
        """Gera documentacao em JSON."""
        data = {
            'timestamp': datetime.now().isoformat(),
            'apps': []
        }

        for app in self.apps:
            data['apps'].append(self.analyze_app(app))

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description='Gera documentacao da estrutura de apps')
    parser.add_argument('--output', default='docs/app_structure', help='Diretorio de saida')
    parser.add_argument('--format', choices=['markdown', 'json', 'both'], default='both', help='Formato de saida')
    parser.add_argument('--root', default='.', help='Raiz do projeto')

    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    analyzer = AppStructureAnalyzer(args.root)
    analyzer.find_apps()

    print(f"\n📚 Analisando {len(analyzer.apps)} aplicacoes...\n")

    if args.format in ['markdown', 'both']:
        md_file = output_dir / 'STRUCTURE.md'
        analyzer.generate_markdown(md_file)
        print(f"✅ Markdown: {md_file}")

    if args.format in ['json', 'both']:
        json_file = output_dir / 'structure.json'
        analyzer.generate_json(json_file)
        print(f"✅ JSON: {json_file}")

    print(f"\n✅ Documentacao gerada em {output_dir.absolute()}\n")


if __name__ == '__main__':
    main()
