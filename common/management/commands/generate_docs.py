"""
Comando Django para gerar documentação completa da estrutura de todas as apps.

Uso:
    python manage.py generate_docs [--format json|markdown|both] [--output docs/]

Gera:
    - app_structure.json (estrutura completa)
    - app_structure.md (markdown legível)
"""

import json
import os
from pathlib import Path
from django.core.management.base import BaseCommand
from django.apps import apps
import inspect
import importlib


class Command(BaseCommand):
    help = 'Gera documentação da estrutura de todas as apps'

    def add_arguments(self, parser):
        parser.add_argument(
            '--format',
            type=str,
            default='both',
            choices=['json', 'markdown', 'both'],
            help='Formato de saída (json, markdown, ou both)'
        )
        parser.add_argument(
            '--output',
            type=str,
            default='docs/',
            help='Diretório de saída (padrão: docs/)'
        )

    def handle(self, *args, **options):
        output_dir = Path(options['output'])
        output_dir.mkdir(exist_ok=True)

        # Coletar informações de todas as apps
        apps_data = {}
        for app in apps.get_app_configs():
            if not app.name.startswith('django.'):
                self.stdout.write(f"📦 Processando: {app.name}")
                apps_data[app.name] = self.get_app_structure(app)

        # Gerar JSON
        if options['format'] in ['json', 'both']:
            json_file = output_dir / 'app_structure.json'
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(apps_data, f, indent=2, default=str, ensure_ascii=False)
            self.stdout.write(self.style.SUCCESS(f'✅ JSON gerado: {json_file}'))

        # Gerar Markdown
        if options['format'] in ['markdown', 'both']:
            md_file = output_dir / 'app_structure.md'
            with open(md_file, 'w', encoding='utf-8') as f:
                self._write_markdown(f, apps_data)
            self.stdout.write(self.style.SUCCESS(f'✅ Markdown gerado: {md_file}'))

    def get_app_structure(self, app):
        """Extrai estrutura completa de uma app"""
        app_path = Path(app.module.__file__).parent
        
        return {
            'name': app.name,
            'verbose_name': app.verbose_name,
            'path': str(app_path),
            'files': self._get_file_structure(app_path),
            'models': self._get_models(app),
            'views': self._get_views(app),
            'urls': self._get_urls(app),
            'admin_registered': self._get_admin_registered(app),
        }

    def _get_file_structure(self, app_path):
        """Mapeia estrutura de pastas e arquivos"""
        structure = {}
        for root, dirs, files in os.walk(app_path):
            # Ignorar __pycache__ e .pyc
            dirs[:] = [d for d in dirs if d != '__pycache__']
            
            rel_path = Path(root).relative_to(app_path)
            rel_path_str = str(rel_path) if str(rel_path) != '.' else ''
            
            structure[rel_path_str or '.'] = [
                f for f in files 
                if f.endswith(('.py', '.html', '.txt', '.md', '.json'))
            ]
        
        return structure

    def _get_models(self, app):
        """Lista todos os models da app"""
        models_info = {}
        try:
            models_module = importlib.import_module(f'{app.name}.models')
            for name, obj in inspect.getmembers(models_module):
                if inspect.isclass(obj) and hasattr(obj, '_meta'):
                    try:
                        # Verificar se é um model do Django
                        if hasattr(obj._meta, 'app_label') and obj._meta.app_label == app.label:
                            fields = [f.name for f in obj._meta.get_fields()]
                            models_info[name] = {
                                'fields': fields,
                                'module': obj.__module__,
                            }
                    except:
                        pass
        except ImportError:
            pass
        
        return models_info

    def _get_views(self, app):
        """Lista funções de view da app"""
        views_info = {}
        
        # Verificar web_views
        try:
            web_views_module = importlib.import_module(f'{app.name}.views.web_views')
            if hasattr(web_views_module, '__all__'):
                for name in web_views_module.__all__:
                    views_info[name] = {'type': 'web_view', 'module': 'web_views'}
        except (ImportError, AttributeError):
            pass
        
        # Verificar api_views
        try:
            api_views_module = importlib.import_module(f'{app.name}.views.api_views')
            if hasattr(api_views_module, '__all__'):
                for name in api_views_module.__all__:
                    views_info[name] = {'type': 'api_view', 'module': 'api_views'}
        except (ImportError, AttributeError):
            pass
        
        # Views diretas em views.py
        try:
            views_module = importlib.import_module(f'{app.name}.views')
            for name, obj in inspect.getmembers(views_module):
                if callable(obj) and (inspect.isfunction(obj) or inspect.isclass(obj)):
                    if not name.startswith('_'):
                        views_info[name] = {'type': 'function' if inspect.isfunction(obj) else 'class', 'module': 'views'}
        except ImportError:
            pass
        
        return views_info

    def _get_urls(self, app):
        """Lista padrões de URLs e namespaces"""
        urls_info = {'patterns': [], 'namespace': None}
        
        try:
            urls_module = importlib.import_module(f'{app.name}.urls')
            
            # Namespace
            if hasattr(urls_module, 'app_name'):
                urls_info['namespace'] = urls_module.app_name
            
            # Padrões
            if hasattr(urls_module, 'urlpatterns'):
                for pattern in urls_module.urlpatterns:
                    try:
                        urls_info['patterns'].append({
                            'pattern': str(pattern.pattern),
                            'name': getattr(pattern, 'name', None),
                        })
                    except:
                        pass
        except ImportError:
            pass
        
        return urls_info

    def _get_admin_registered(self, app):
        """Lista models registrados no admin"""
        admin_registered = []
        try:
            admin_module = importlib.import_module(f'{app.name}.admin')
            # Verificar o registro no site do admin
            from django.contrib import admin as django_admin
            for model, admin_class in django_admin.site._registry.items():
                if model._meta.app_label == app.label:
                    admin_registered.append({
                        'model': model.__name__,
                        'admin_class': admin_class.__class__.__name__,
                    })
        except (ImportError, AttributeError):
            pass
        
        return admin_registered

    def _write_markdown(self, f, apps_data):
        """Escreve documentação em Markdown"""
        f.write("# 📋 Documentação da Estrutura do GPP Platform\n\n")
        f.write(f"*Gerada automaticamente pelo comando `generate_docs`*\n\n")
        
        # Índice
        f.write("## 📑 Índice\n\n")
        for app_name in sorted(apps_data.keys()):
            if not app_name.startswith('django.'):
                f.write(f"- [{apps_data[app_name]['verbose_name']}](#{app_name})\n")
        
        f.write("\n---\n\n")
        
        # Detalhes de cada app
        for app_name, app_data in sorted(apps_data.items()):
            if app_name.startswith('django.'):
                continue
            
            f.write(f"## {app_data['verbose_name']} {app_name}\n\n")
            f.write(f"**Path:** `{app_data['path']}`\n\n")
            
            # Estrutura de arquivos
            if app_data['files']:
                f.write("### 📁 Estrutura de Arquivos\n\n")
                f.write("```\n")
                for folder, files in sorted(app_data['files'].items()):
                    f.write(f"{folder}/\n")
                    for file in sorted(files):
                        f.write(f"  ├─ {file}\n")
                f.write("```\n\n")
            
            # Models
            if app_data['models']:
                f.write("### 🗂️ Models\n\n")
                for model_name, model_info in sorted(app_data['models'].items()):
                    f.write(f"#### `{model_name}`\n\n")
                    f.write(f"**Fields:** `{', '.join(model_info['fields'])}`\n\n")
            
            # Views
            if app_data['views']:
                f.write("### 👀 Views\n\n")
                f.write("| Nome | Tipo | Módulo |\n")
                f.write("|------|------|--------|\n")
                for view_name, view_info in sorted(app_data['views'].items()):
                    f.write(f"| `{view_name}` | {view_info['type']} | {view_info['module']} |\n")
                f.write("\n")
            
            # URLs
            if app_data['urls']['namespace'] or app_data['urls']['patterns']:
                f.write("### 🔗 URLs\n\n")
                if app_data['urls']['namespace']:
                    f.write(f"**Namespace:** `{app_data['urls']['namespace']}`\n\n")
                
                if app_data['urls']['patterns']:
                    f.write("**Padrões:**\n\n")
                    for pattern in app_data['urls']['patterns']:
                        pattern_str = pattern['pattern']
                        name = pattern['name'] or '(sem nome)'
                        f.write(f"- `{pattern_str}` → `{name}`\n")
                    f.write("\n")
            
            # Admin
            if app_data['admin_registered']:
                f.write("### 👨‍💼 Admin Registrado\n\n")
                for admin in app_data['admin_registered']:
                    f.write(f"- `{admin['model']}` ({admin['admin_class']})\n")
                f.write("\n")
            
            f.write("---\n\n")
