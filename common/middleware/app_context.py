"""
Middleware de Contexto de Aplicação
Detecta automaticamente qual aplicação está sendo acessada
baseado na URL da requisição.
"""

from typing import Optional
from django.http import HttpRequest
from accounts.models import Aplicacao
import logging

logger = logging.getLogger(__name__)


class AppContextMiddleware:
    """
    Middleware que adiciona contexto da aplicação atual em cada requisição.
    
    Detecta a aplicação através da URL:
    - /api/v1/acoes_pngi/*  → ACOES_PNGI
    - /api/v1/carga/*       → CARGA_ORG_LOT
    - /acoes-pngi/*         → ACOES_PNGI
    - /carga_org_lot/*      → CARGA_ORG_LOT
    - /api/v1/portal/*      → PORTAL
    - /                     → PORTAL
    
    Adiciona à requisição:
    - request.app_context: dict com 'code' e 'instance'
    """
    
    # Mapeamento de URLs para códigos de aplicação
    URL_TO_APP = {
        '/api/v1/acoes_pngi/': 'ACOES_PNGI',
        '/acoes-pngi/': 'ACOES_PNGI',
        '/api/v1/carga/': 'CARGA_ORG_LOT',
        '/carga_org_lot/': 'CARGA_ORG_LOT',
        '/api/v1/portal/': 'PORTAL',
        '/api/v1/auth/': 'PORTAL',
    }
    
    # Cache de objetos Aplicacao (para performance)
    _apps_cache = {}
    
    def __init__(self, get_response):
        self.get_response = get_response
        self._load_apps_cache()
    
    def __call__(self, request: HttpRequest):
        # Detecta e adiciona contexto da aplicação
        self._add_app_context(request)
        
        # Processa a requisição
        response = self.get_response(request)
        
        return response
    
    def _load_apps_cache(self):
        """Carrega aplicações em cache para evitar queries repetidas"""
        try:
            apps = Aplicacao.objects.all()
            self._apps_cache = {app.codigointerno: app for app in apps}
            logger.info(f"App cache carregado: {list(self._apps_cache.keys())}")
        except Exception as e:
            logger.warning(f"Erro ao carregar cache de aplicações: {e}")
            self._apps_cache = {}
    
    def _add_app_context(self, request: HttpRequest):
        """
        Adiciona contexto da aplicação à requisição
        
        Adiciona request.app_context com:
        - code: str - Código da aplicação (ex: 'ACOES_PNGI')
        - instance: Aplicacao - Objeto da aplicação
        - name: str - Nome da aplicação (ex: 'Gestão de Ações PNGI')
        """
        app_code = self._detect_app_from_url(request.path)
        
        if app_code:
            # Tenta buscar do cache
            app_instance = self._apps_cache.get(app_code)
            
            # Se não está em cache, busca do banco
            if not app_instance:
                try:
                    app_instance = Aplicacao.objects.get(codigointerno=app_code)
                    self._apps_cache[app_code] = app_instance
                except Aplicacao.DoesNotExist:
                    logger.warning(f"Aplicação '{app_code}' não encontrada no banco")
                    app_instance = None
            
            request.app_context = {
                'code': app_code,
                'instance': app_instance,
                'name': app_instance.nomeaplicacao if app_instance else None,
            }
        else:
            # Sem contexto (ex: /admin/, /static/)
            request.app_context = {
                'code': None,
                'instance': None,
                'name': None,
            }
        
        logger.debug(f"Request {request.path} → App: {request.app_context['code']}")
    
    def _detect_app_from_url(self, path: str) -> Optional[str]:
        """
        Detecta código da aplicação baseado na URL
        
        Args:
            path: Caminho da URL (ex: '/api/v1/acoes_pngi/eixos/')
        
        Returns:
            Código da aplicação ou None
        """
        # Verifica cada prefixo mapeado
        for url_prefix, app_code in self.URL_TO_APP.items():
            if path.startswith(url_prefix):
                return app_code
        
        # URL raiz (/) é do Portal
        if path == '/' or path == '':
            return 'PORTAL'
        
        # Não identificado
        return None
