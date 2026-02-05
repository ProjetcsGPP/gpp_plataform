"""
Comando Django: generate_structure_docs

Gera documentacao completa da estrutura de todas as aplicacoes Django.
Útil para evitar conflitos de nomes e documentar a arquitetura.

Uso:
    python manage.py generate_structure_docs
    python manage.py generate_structure_docs --output /caminho/docs
    python manage.py generate_structure_docs --format json
"""

import os
import json
from pathlib import Path
from datetime import datetime
import ast
import re
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps


class Command(BaseCommand):
    help = 'Gera documentacao da estrutura interna de todas as aplicacoes Django'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='docs/app_structure',
            help='Diretorio de saida para a documentacao (padrao: docs/app_structure)'
        )
        parser.add_argument(
            '--format',
            type=str,
            choices=['markdown', 'json', 'both'],
            default='both',
            help='Formato de saida (markdown, json ou both)'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Modo verbose com detalhes adicionais'
        )

    def handle(self, *args, **options):
        output_dir = Path(options['output'])
        output_format = options['format']
        verbose = options['verbose']

        # Criar diretorio de saida
        output_dir.mkdir(parents=True, exist_ok=True)

        self.stdout.write(self.style.SUCCESS(f'\n📚 Gerando Documentacao de Estrutura de Apps\n'))
        self.stdout.write(f'Output: {output_dir.absolute()}')
        self.stdout.write(f'Format: {output_format}\n')

        # Gerar documentacao
        structure_data = self.get_apps_structure(verbose)

        # Salvar em markdown
        if output_format in ['markdown', 'both']:
            self.write_markdown_docs(output_dir, structure_data)

        # Salvar em JSON
        if output_format in ['json', 'both']:
            self.write_json_docs(output_dir, structure_data)

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Documentacao gerada com sucesso em {output_dir.absolute()}\n'
        ))

    def get_apps_structure(self, verbose=False):
        """Retorna estrutura completa de todos os apps instalados."""
        structure = {
            'timestamp': datetime.now().isoformat(),
            'apps': {}
        }

        for app_config in apps.get_app_configs():
            # Pular apps do Django core
            if app_config.name.startswith('django.'):
                continue

            app_path = Path(app_config.module.__file__).parent
            app_structure = self.analyze_app(app_config, app_path, verbose)
            structure['apps'][app_config.name] = app_structure

        return structure

    def analyze_app(self, app_config, app_path, verbose=False):
        """Analisa estrutura de um app individual."""
        app_data = {
            'name': app_config.name,
            'verbose_name': app_config.verbose_name,
            'path': str(app_path),
            'files': {},
            'models': [],
            'views': [],
            'serializers': [],
            'urls': [],
            'permissions': [],
            'signals': []
        }

        # Analisar models.py
        models_file = app_path / 'models.py'
        if models_file.exists():
            app_data['models'] = self.extract_models(models_file)
            app_data['files']['models.py'] = True

        # Analisar models/ (pacote)
        models_dir = app_path / 'models'
        if models_dir.exists() and models_dir.is_dir():
            app_data['files']['models/'] = True
            for f in models_dir.glob('*.py'):
                if f.name != '__init__.py':
                    app_data['models'].extend(self.extract_models(f))

        # Analisar views.py
        views_file = app_path / 'views.py'
        if views_file.exists():
            app_data['views'] = self.extract_views(views_file)
            app_data['files']['views.py'] = True

        # Analisar views/ (pacote)
        views_dir = app_path / 'views'
        if views_dir.exists() and views_dir.is_dir():
            app_data['files']['views/'] = True
            for f in views_dir.glob('*.py'):
                if f.name != '__init__.py':
                    app_data['views'].extend(self.extract_views(f))

        # Analisar serializers
        serializers_file = app_path / 'serializers.py'
        if serializers_file.exists():
            app_data['serializers'] = self.extract_classes(serializers_file, 'Serializer')
            app_data['files']['serializers.py'] = True

        # Analisar URLs
        urls_file = app_path / 'urls.py'
        if urls_file.exists():
            app_data['urls'] = self.extract_urls(urls_file)
            app_data['files']['urls.py'] = True

        urls_init = app_path / 'urls' / '__init__.py'
        if urls_init.exists():
            app_data['urls'].extend(self.extract_urls(urls_init))
            app_data['files']['urls/'] = True

        # Analisar permissions
        permissions_file = app_path / 'permissions.py'
        if permissions_file.exists():
            app_data['permissions'] = self.extract_classes(permissions_file, 'Permission')
            app_data['files']['permissions.py'] = True

        # Analisar signals
        signals_file = app_path / 'signals.py'
        if signals_file.exists():
            app_data['signals'] = self.extract_functions(signals_file)
            app_data['files']['signals.py'] = True

        # Estrutura de diretorio
        app_data['structure'] = self.get_directory_structure(app_path, max_depth=3)

        return app_data

    def extract_models(self, file_path):
        """Extrai nomes de models de um arquivo."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())

            models = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Verificar se herda de Model
                    for base in node.bases:
                        if isinstance(base, ast.Name) and 'Model' in base.id:
                            models.append({
                                'name': node.name,
                                'lineno': node.lineno,
                                'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                            })
                        elif isinstance(base, ast.Attribute):
                            if 'Model' in base.attr:
                                models.append({
                                    'name': node.name,
                                    'lineno': node.lineno,
                                    'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                                })
            return models
        except Exception as e:
            return []

    def extract_views(self, file_path):
        """Extrai nomes de views de um arquivo."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content)

            views = []

            # Extrair funcoes
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Verificar se tem decorator @
                    decorators = [d.id if isinstance(d, ast.Name) else 
                                (d.func.id if isinstance(d, ast.Call) and isinstance(d.func, ast.Name) else '')
                                for d in node.decorator_list]
                    views.append({
                        'name': node.name,
                        'type': 'function',
                        'lineno': node.lineno,
                        'decorators': decorators
                    })

                elif isinstance(node, ast.ClassDef):
                    # Verificar se herda de View
                    is_view = any('View' in (base.id if isinstance(base, ast.Name) else 
                                           base.attr if isinstance(base, ast.Attribute) else '')
                                 for base in node.bases)
                    if is_view:
                        methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                        views.append({
                            'name': node.name,
                            'type': 'class',
                            'lineno': node.lineno,
                            'methods': methods
                        })

            return views
        except Exception as e:
            return []

    def extract_classes(self, file_path, filter_name=None):
        """Extrai nomes de classes de um arquivo."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())

            classes = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    if not filter_name or filter_name in str(node.bases):
                        classes.append({
                            'name': node.name,
                            'lineno': node.lineno,
                            'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                        })
            return classes
        except Exception:
            return []

    def extract_functions(self, file_path):
        """Extrai nomes de funcoes de um arquivo."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())

            functions = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
                    decorators = [d.id if isinstance(d, ast.Name) else '' for d in node.decorator_list]
                    functions.append({
                        'name': node.name,
                        'lineno': node.lineno,
                        'decorators': decorators
                    })
            return functions
        except Exception:
            return []

    def extract_urls(self, file_path):
        """Extrai informacoes de URLs."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            urls = []
            # Usar regex para encontrar path() e include()
            path_pattern = r'path\([\'\"]([^\'\"]*)[\'\"]'
            matches = re.findall(path_pattern, content)
            urls = [{'pattern': m} for m in matches]

            return urls
        except Exception:
            return []

    def get_directory_structure(self, path, prefix="", max_depth=3, current_depth=0):
        """Retorna estrutura de diretorios em formato de arvore."""
        if current_depth >= max_depth:
            return ""

        items = []
        try:
            for item in sorted(path.iterdir()):
                if item.name.startswith('.'):
                    continue
                if item.name.startswith('__pycache__'):
                    continue

                if item.is_file():
                    items.append(f"{prefix}├── {item.name}")
                elif item.is_dir():
                    items.append(f"{prefix}├── {item.name}/")
                    sub_items = self.get_directory_structure(
                        item,
                        prefix + "│   ",
                        max_depth,
                        current_depth + 1
                    )
                    if sub_items:
                        items.append(sub_items)
        except PermissionError:
            pass

        return "\n".join(items)

    def write_markdown_docs(self, output_dir, structure_data):
        """Escreve documentacao em Markdown."""
        md_file = output_dir / 'STRUCTURE.md'

        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(f"# 📦 Estrutura de Aplicacoes Django\n\n")
            f.write(f"**Gerado em:** {structure_data['timestamp']}\n\n")
            f.write(f"## Indice\n\n")

            # Indice
            for app_name in structure_data['apps'].keys():
                f.write(f"- [{app_name}](#{app_name})\n")

            f.write("\n---\n\n")

            # Detalhes de cada app
            for app_name, app_data in structure_data['apps'].items():
                f.write(f"## {app_name}\n\n")
                f.write(f"**Path:** `{app_data['path']}`\n\n")

                # Models
                if app_data['models']:
                    f.write(f"### 📊 Models\n\n")
                    for model in app_data['models']:
                        f.write(f"- **{model['name']}** (linha {model['lineno']})\n")
                        if model.get('methods'):
                            f.write(f"  - Metodos: {', '.join(model['methods'])}\n")
                    f.write("\n")

                # Views
                if app_data['views']:
                    f.write(f"### 👁️ Views\n\n")
                    for view in app_data['views']:
                        if view['type'] == 'function':
                            f.write(f"- **{view['name']}()** (função)\n")
                        else:
                            f.write(f"- **{view['name']}** (classe)\n")
                            if view.get('methods'):
                                f.write(f"  - Metodos: {', '.join(view['methods'])}\n")
                    f.write("\n")

                # Serializers
                if app_data['serializers']:
                    f.write(f"### 📝 Serializers\n\n")
                    for ser in app_data['serializers']:
                        f.write(f"- **{ser['name']}**\n")
                    f.write("\n")

                # URLs
                if app_data['urls']:
                    f.write(f"### 🌐 URLs\n\n")
                    f.write(f"```\n")
                    for url in app_data['urls'][:10]:  # Limitar a 10
                        f.write(f"- {url['pattern']}\n")
                    if len(app_data['urls']) > 10:
                        f.write(f"... e mais {len(app_data['urls']) - 10}\n")
                    f.write(f"```\n\n")

                # Estrutura
                if app_data.get('structure'):
                    f.write(f"### 📁 Estrutura de Diretorios\n\n")
                    f.write(f"```\n")
                    f.write(app_data['structure'])
                    f.write(f"\n```\n\n")

                f.write("---\n\n")

        self.stdout.write(self.style.SUCCESS(f'✅ Markdown: {md_file}'))

    def write_json_docs(self, output_dir, structure_data):
        """Escreve documentacao em JSON."""
        json_file = output_dir / 'structure.json'

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(structure_data, f, indent=2, ensure_ascii=False)

        self.stdout.write(self.style.SUCCESS(f'✅ JSON: {json_file}'))
