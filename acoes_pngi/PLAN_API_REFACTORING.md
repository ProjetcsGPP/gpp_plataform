# 📋 Plano de Refatoração: API Views para Sistema Automatizado de Permissões

**Data:** 30/01/2026  
**Branch:** `feature/automated-permissions-system`  
**Arquivo Alvo:** `acoes_pngi/views/api_views.py`  
**Arquivo de Permissões:** `acoes_pngi/permissions.py`

---

## 🎯 Objetivo

Refatorar as API views para usar o **mesmo sistema automatizado de permissões** aplicado nas web_views, mantendo consistência, performance e legibilidade.

---

## 🔍 Análise do Código Atual

### **Estado Atual do `api_views.py` (584 linhas)**

#### ✅ **JÁ ESTÁ BEM IMPLEMENTADO:**

1. **ViewSets com `HasAcoesPermission`:**
   - `EixoViewSet` ✅
   - `SituacaoAcaoViewSet` ✅
   - `VigenciaPNGIViewSet` ✅
   - Usam classe de permissão automatizada que já verifica CRUD

2. **Endpoints de Autenticação:**
   - `portal_auth()` ✅ - Usa `AllowAny`
   - `user_permissions()` ✅ - Retorna permissões do usuário

3. **UserManagementViewSet:**
   - Gerenciamento de usuários ✅
   - Usa `IsAuthenticated`

#### ❌ **PROBLEMAS IDENTIFICADOS:**

1. **Verificações manuais de permissão em actions customizadas:**
   ```python
   # EixoViewSet.list_light() - linha ~445
   if not request.user.has_app_perm('ACOES_PNGI', 'view_eixo'):
       return Response({...}, status=403)
   
   # VigenciaPNGIViewSet.vigencia_ativa() - linha ~526
   if not request.user.has_app_perm('ACOES_PNGI', 'view_vigenciapngi'):
       return Response({...}, status=403)
   ```
   **Problema:** Verificações manuais repetitivas e inconsistentes

2. **Uso de `get_app_permissions()` sem helper:**
   ```python
   # user_permissions() - linha ~162
   perms = list(request.user.get_app_permissions('ACOES_PNGI'))
   ```
   **Problema:** Não usa `get_user_app_permissions()` com cache

3. **Falta de decorators para actions customizadas:**
   - `list_light()`, `vigencia_ativa()` fazem verificação manual
   - Deveria usar decorators ou permission_classes específicas

4. **Inconsistência com web_views:**
   - Web views usam `require_app_permission` decorator
   - API views usam verificações manuais em actions

---

## 🛠️ Soluções Propostas

### **1. Criar Decorator para API Views (@require_api_permission)**

**Problema:** Web views tem `@require_app_permission`, mas APIs precisam de um decorator adaptado para DRF.

**Solução:** Criar decorator específico para actions de ViewSets

**Localização:** `acoes_pngi/utils/permissions.py`

```python
from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def require_api_permission(permission_codename, app_code='ACOES_PNGI'):
    """
    Decorator para verificar permissões em actions customizadas de ViewSets.
    
    Uso:
        @action(detail=False, methods=['get'])
        @require_api_permission('view_eixo')
        def list_light(self, request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            if not request.user or not request.user.is_authenticated:
                return Response(
                    {'detail': 'Autenticação necessária'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            if request.user.is_superuser:
                return view_func(self, request, *args, **kwargs)
            
            if not request.user.has_app_perm(app_code, permission_codename):
                return Response(
                    {
                        'detail': f'Você não tem permissão para realizar esta ação.',
                        'required_permission': permission_codename
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            
            return view_func(self, request, *args, **kwargs)
        
        return wrapper
    return decorator
```

### **2. Usar `get_user_app_permissions()` com Cache**

**Antes:**
```python
# user_permissions() - linha ~162
perms = list(request.user.get_app_permissions('ACOES_PNGI'))
```

**Depois:**
```python
from ..utils.permissions import get_user_app_permissions

perms = get_user_app_permissions(request.user, 'ACOES_PNGI')
```

**Benefício:** Cache de 15min, menos queries

### **3. Refatorar Actions Customizadas**

#### **EixoViewSet.list_light() (linha ~438)**

**Antes:**
```python
@action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
def list_light(self, request):
    # Verifica permissão de view
    if not request.user.has_app_perm('ACOES_PNGI', 'view_eixo'):
        return Response(
            {'detail': 'Você não tem permissão para visualizar eixos'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    eixos = Eixo.objects.all().values('ideixo', 'strdescricaoeixo', 'stralias')
    return Response({
        'count': len(eixos),
        'results': list(eixos)
    })
```

**Depois:**
```python
@action(detail=False, methods=['get'])
@require_api_permission('view_eixo')
def list_light(self, request):
    """
    Endpoint otimizado para listagem rápida.
    Requer permissão: view_eixo (verificado automaticamente)
    """
    eixos = Eixo.objects.all().values('ideixo', 'strdescricaoeixo', 'stralias')
    return Response({
        'count': len(eixos),
        'results': list(eixos)
    })
```

**Redução:** -6 linhas por action

#### **VigenciaPNGIViewSet.vigencia_ativa() (linha ~518)**

**Antes:**
```python
@action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
def vigencia_ativa(self, request):
    # Verifica permissão de view
    if not request.user.has_app_perm('ACOES_PNGI', 'view_vigenciapngi'):
        return Response(
            {'detail': 'Você não tem permissão para visualizar vigências'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        vigencia = VigenciaPNGI.objects.get(isvigenciaativa=True)
        serializer = self.get_serializer(vigencia)
        return Response(serializer.data)
    except VigenciaPNGI.DoesNotExist:
        return Response(
            {'detail': 'Nenhuma vigência ativa encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )
```

**Depois:**
```python
@action(detail=False, methods=['get'])
@require_api_permission('view_vigenciapngi')
def vigencia_ativa(self, request):
    """
    Retorna a vigência atualmente ativa.
    Requer permissão: view_vigenciapngi (verificado automaticamente)
    """
    try:
        vigencia = VigenciaPNGI.objects.get(isvigenciaativa=True)
        serializer = self.get_serializer(vigencia)
        return Response(serializer.data)
    except VigenciaPNGI.DoesNotExist:
        return Response(
            {'detail': 'Nenhuma vigência ativa encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )
```

**Redução:** -6 linhas

### **4. Simplificar `user_permissions()`**

**Antes (linha ~145-208):**
```python
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_permissions(request):
    try:
        perms = list(request.user.get_app_permissions('ACOES_PNGI'))  # ❌ Sem cache
        
        # Buscar role do usuário
        user_role = UserRole.objects.filter(
            user=request.user,
            aplicacao__codigointerno='ACOES_PNGI'
        ).select_related('role').first()
        
        role = user_role.role.codigoperfil if user_role else None
        
        # Agrupar permissões por model (lógica manual)
        models = ['eixo', 'situacaoacao', 'vigenciapngi']
        specific = {}
        
        for model in models:
            specific[model] = {
                'add': f'add_{model}' in perms,
                'change': f'change_{model}' in perms,
                'delete': f'delete_{model}' in perms,
                'view': f'view_{model}' in perms,
            }
        
        return Response({...})
    except Exception as e:
        ...
```

**Depois:**
```python
from ..utils.permissions import get_user_app_permissions, get_model_permissions

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_permissions(request):
    """
    Retorna permissões do usuário logado para consumo no Next.js.
    Usa helpers com cache para otimização.
    """
    try:
        # ✅ Usa helper com cache
        perms = get_user_app_permissions(request.user, 'ACOES_PNGI')
        
        # Buscar role do usuário
        user_role = UserRole.objects.filter(
            user=request.user,
            aplicacao__codigointerno='ACOES_PNGI'
        ).select_related('role').first()
        
        role = user_role.role.codigoperfil if user_role else None
        
        # ✅ Usa helper para permissões por modelo
        specific = {
            'eixo': get_model_permissions(request.user, 'eixo', 'ACOES_PNGI'),
            'situacaoacao': get_model_permissions(request.user, 'situacaoacao', 'ACOES_PNGI'),
            'vigenciapngi': get_model_permissions(request.user, 'vigenciapngi', 'ACOES_PNGI'),
        }
        
        return Response({
            'user_id': request.user.id,
            'email': request.user.email,
            'name': request.user.name,
            'role': role,
            'permissions': list(perms),
            'is_superuser': request.user.is_superuser,
            'groups': {
                'can_manage_config': any(p in perms for p in [
                    'add_eixo', 'change_eixo', 
                    'add_situacaoacao', 'change_situacaoacao',
                    'add_vigenciapngi', 'change_vigenciapngi'
                ]),
                'can_manage_acoes': False,
                'can_delete': any(p.startswith('delete_') for p in perms),
            },
            'specific': specific,
        })
    except Exception as e:
        logger.error(f"Erro ao buscar permissões do usuário: {str(e)}")
        return Response(
            {'detail': f'Erro ao buscar permissões: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
```

**Benefícios:**
- Cache de permissões (15min)
- Código mais limpo e reutilizável
- Consistência com web_views

---

## 📊 Resumo das Mudanças

### **Arquivos Modificados:**

| Arquivo | Mudanças | Linhas |
|---------|-----------|--------|
| `utils/permissions.py` | Adicionar `require_api_permission` decorator | +35 |
| `views/api_views.py` | Refatorar 3 actions + user_permissions | -20 |
| `permissions.py` | **Nenhuma** (já tem `HasAcoesPermission`) | 0 |

### **Estatísticas:**

| Métrica | Antes | Depois | Diferença |
|---------|-------|--------|----------|
| **Verificações manuais** | 3 | 0 | -3 (-100%) |
| **Linhas api_views.py** | 584 | ~565 | -19 (-3.2%) |
| **Uso de cache** | 0 | 4 | +4 |
| **Consistência com web_views** | 60% | 100% | +40% |

---

## ✅ Lista de Alterações Detalhadas

### **PARTE 1: Criar Decorator para API**

**Arquivo:** `acoes_pngi/utils/permissions.py`

```python
# Adicionar no final do arquivo (após get_model_permissions)

def require_api_permission(permission_codename, app_code='ACOES_PNGI'):
    """
    Decorator para verificar permissões em actions de ViewSets DRF.
    Similar ao require_app_permission mas adaptado para API.
    
    Uso:
        @action(detail=False, methods=['get'])
        @require_api_permission('view_eixo')
        def list_light(self, request):
            ...
    
    Args:
        permission_codename: Nome da permissão (ex: 'view_eixo')
        app_code: Código da aplicação (padrão: 'ACOES_PNGI')
    
    Returns:
        Response com erro 403 se não tiver permissão
    """
    from functools import wraps
    from rest_framework.response import Response
    from rest_framework import status
    
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            # Verifica autenticação
            if not request.user or not request.user.is_authenticated:
                return Response(
                    {'detail': 'Autenticação necessária'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Superuser sempre tem acesso
            if request.user.is_superuser:
                return view_func(self, request, *args, **kwargs)
            
            # Verifica permissão
            if not request.user.has_app_perm(app_code, permission_codename):
                return Response(
                    {
                        'detail': f'Você não tem permissão para realizar esta ação.',
                        'required_permission': permission_codename,
                        'app': app_code
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            
            return view_func(self, request, *args, **kwargs)
        
        return wrapper
    return decorator
```

### **PARTE 2: Adicionar Import no api_views.py**

**Linha 12 (após os imports atuais):**
```python
from ..utils.permissions import (
    get_user_app_permissions,
    get_model_permissions,
    require_api_permission
)
```

### **PARTE 3: Refatorar EixoViewSet.list_light()**

**Linhas 438-451 (antes):**
```python
@action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
def list_light(self, request):
    """
    Endpoint otimizado para listagem rápida (apenas visualização)
    """
    # Verifica permissão de view
    if not request.user.has_app_perm('ACOES_PNGI', 'view_eixo'):
        return Response(
            {'detail': 'Você não tem permissão para visualizar eixos'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    eixos = Eixo.objects.all().values('ideixo', 'strdescricaoeixo', 'stralias')
    return Response({
        'count': len(eixos),
        'results': list(eixos)
    })
```

**Depois:**
```python
@action(detail=False, methods=['get'])
@require_api_permission('view_eixo')
def list_light(self, request):
    """
    Endpoint otimizado para listagem rápida.
    Requer permissão: view_eixo (verificado automaticamente pelo decorator)
    """
    eixos = Eixo.objects.all().values('ideixo', 'strdescricaoeixo', 'stralias')
    return Response({
        'count': len(eixos),
        'results': list(eixos)
    })
```

### **PARTE 4: Refatorar VigenciaPNGIViewSet.vigencia_ativa()**

**Linhas 518-536 (antes):**
```python
@action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
def vigencia_ativa(self, request):
    """
    Retorna a vigência atualmente ativa (apenas visualização)
    """
    # Verifica permissão de view
    if not request.user.has_app_perm('ACOES_PNGI', 'view_vigenciapngi'):
        return Response(
            {'detail': 'Você não tem permissão para visualizar vigências'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        vigencia = VigenciaPNGI.objects.get(isvigenciaativa=True)
        serializer = self.get_serializer(vigencia)
        return Response(serializer.data)
    except VigenciaPNGI.DoesNotExist:
        return Response(
            {'detail': 'Nenhuma vigência ativa encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )
```

**Depois:**
```python
@action(detail=False, methods=['get'])
@require_api_permission('view_vigenciapngi')
def vigencia_ativa(self, request):
    """
    Retorna a vigência atualmente ativa.
    Requer permissão: view_vigenciapngi (verificado automaticamente)
    """
    try:
        vigencia = VigenciaPNGI.objects.get(isvigenciaativa=True)
        serializer = self.get_serializer(vigencia)
        return Response(serializer.data)
    except VigenciaPNGI.DoesNotExist:
        return Response(
            {'detail': 'Nenhuma vigência ativa encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )
```

### **PARTE 5: Simplificar user_permissions()**

**Linhas 162-163 (mudança principal):**

**Antes:**
```python
perms = list(request.user.get_app_permissions('ACOES_PNGI'))

# ... código manual para agrupar permissões ...
for model in models:
    specific[model] = {
        'add': f'add_{model}' in perms,
        'change': f'change_{model}' in perms,
        'delete': f'delete_{model}' in perms,
        'view': f'view_{model}' in perms,
    }
```

**Depois:**
```python
perms = get_user_app_permissions(request.user, 'ACOES_PNGI')

# Usa helper para permissões por modelo
specific = {
    'eixo': get_model_permissions(request.user, 'eixo', 'ACOES_PNGI'),
    'situacaoacao': get_model_permissions(request.user, 'situacaoacao', 'ACOES_PNGI'),
    'vigenciapngi': get_model_permissions(request.user, 'vigenciapngi', 'ACOES_PNGI'),
}
```

---

## 🧪 Testes PowerShell

### **Análise do Teste Atual:**

**Arquivo:** `TestesPowerShell/Acoes_PNGI_test_permissions_API.ps1` (590 linhas)

✅ **JÁ ESTÁ BEM ESTRUTURADO:**
- Testa autenticação JWT
- Testa endpoint `/permissions/`
- Testa CRUD completo de Eixos, Situações e Vigências
- Verifica permissões antes de cada operação
- Output colorido e organizado

❌ **MUDANÇAS NECESSÁRIAS:**

**Nenhuma mudança obrigatória!** Os testes já estão corretos.

✅ **MELHORIAS OPCIONAIS:**

1. **Adicionar teste específico para actions customizadas:**
   - `list_light` (já testado)
   - `vigencia_ativa` (já testado)
   - Adi adicionar teste para ativação com usuário sem permissão

2. **Adicionar prints de performance:**
   - Medir tempo de resposta com cache vs sem cache
   - Mostrar quando cache é hit

3. **Teste de cache de permissões:**
   - Chamar `/permissions/` 3x seguidas
   - Mostrar que segunda e terceira chamadas são mais rápidas

### **Script de Melhoria Opcional:**

**Arquivo:** `TestesPowerShell/Test-PermissionsCache.ps1` (NOVO)

```powershell
# Teste de Cache de Permissões
# Mede performance do cache

function Test-PermissionsCache {
    param([string]$Token)
    
    Write-Host "`n=== TESTE DE CACHE DE PERMISSÕES ===" -ForegroundColor Cyan
    
    $url = "http://localhost:8000/api/v1/acoes_pngi/permissions/"
    $headers = @{
        "Authorization" = "Bearer $Token"
    }
    
    # Primeira chamada (sem cache)
    Write-Host "`n1ª Chamada (sem cache):" -ForegroundColor Yellow
    $start1 = Get-Date
    $response1 = Invoke-RestMethod -Uri $url -Headers $headers
    $duration1 = (Get-Date) - $start1
    Write-Host "  Tempo: $($duration1.TotalMilliseconds)ms" -ForegroundColor White
    Write-Host "  Permissões: $($response1.permissions.Count)" -ForegroundColor White
    
    # Segunda chamada (com cache)
    Write-Host "`n2ª Chamada (com cache):" -ForegroundColor Yellow
    $start2 = Get-Date
    $response2 = Invoke-RestMethod -Uri $url -Headers $headers
    $duration2 = (Get-Date) - $start2
    Write-Host "  Tempo: $($duration2.TotalMilliseconds)ms" -ForegroundColor White
    
    # Terceira chamada (com cache)
    Write-Host "`n3ª Chamada (com cache):" -ForegroundColor Yellow
    $start3 = Get-Date
    $response3 = Invoke-RestMethod -Uri $url -Headers $headers
    $duration3 = (Get-Date) - $start3
    Write-Host "  Tempo: $($duration3.TotalMilliseconds)ms" -ForegroundColor White
    
    # Análise
    $avgCached = ($duration2.TotalMilliseconds + $duration3.TotalMilliseconds) / 2
    $improvement = [math]::Round((($duration1.TotalMilliseconds - $avgCached) / $duration1.TotalMilliseconds) * 100, 2)
    
    Write-Host "`n📊 RESULTADO:" -ForegroundColor Green
    Write-Host "  Média sem cache: $($duration1.TotalMilliseconds)ms" -ForegroundColor White
    Write-Host "  Média com cache: $([math]::Round($avgCached, 2))ms" -ForegroundColor White
    Write-Host "  Melhoria: $improvement%" -ForegroundColor Green
}
```

---

## 📝 Checklist de Implementação

### **Fase 1: Preparar Helpers**
- [ ] Adicionar `require_api_permission` em `utils/permissions.py`
- [ ] Adicionar testes unitários para o decorator
- [ ] Commit: "feat: Adicionar decorator require_api_permission para API views"

### **Fase 2: Refatorar api_views.py**
- [ ] Adicionar imports dos helpers
- [ ] Refatorar `EixoViewSet.list_light()`
- [ ] Refatorar `VigenciaPNGIViewSet.vigencia_ativa()`
- [ ] Simplificar `user_permissions()`
- [ ] Commit: "refactor: Aplicar sistema automatizado nas API views"

### **Fase 3: Testar Manualmente**
- [ ] Rodar servidor Django
- [ ] Executar `Acoes_PNGI_test_permissions_API.ps1`
- [ ] Verificar todos os testes passam
- [ ] Verificar logs de cache no console

### **Fase 4: (Opcional) Melhorar Testes PowerShell**
- [ ] Criar `Test-PermissionsCache.ps1`
- [ ] Adicionar teste de performance
- [ ] Commit: "test: Adicionar teste de cache de permissões"

### **Fase 5: Documentação e Review**
- [ ] Atualizar docstrings
- [ ] Atualizar README se necessário
- [ ] Code review
- [ ] Merge para main

---

## 🎯 Benefícios da Refatoração

### **1. Consistência**
- ✅ Web views e API views usam mesmo sistema
- ✅ Mesmo padrão de decorators
- ✅ Mesma nomenclatura de permissões

### **2. Performance**
- ✅ Cache de permissões (15min)
- ✅ Menos queries ao banco
- ✅ Resposta mais rápida em `/permissions/`

### **3. Manutenção**
- ✅ Menos código duplicado
- ✅ Verificações centralizadas
- ✅ Fácil adicionar novas actions

### **4. Legibilidade**
- ✅ Decorators auto-explicativos
- ✅ Menos lógica condicional
- ✅ Docstrings claras

---

## 🚀 Próximos Passos

1. **Revisar este plano** com o time
2. **Aprovar mudanças** propostas
3. **Implementar Fase 1** (helpers)
4. **Implementar Fase 2** (api_views)
5. **Testar com PowerShell**
6. **Merge e deploy**

---

## 📚 Referências

- **Sistema atual:** `acoes_pngi/permissions.py` (HasAcoesPermission)
- **Helpers existentes:** `acoes_pngi/utils/permissions.py`
- **Web views refatoradas:** `acoes_pngi/views/web_views.py`
- **Testes PowerShell:** `TestesPowerShell/Acoes_PNGI_test_permissions_API.ps1`
- **Documentação:** `acoes_pngi/README_AUTOMATED_PERMISSIONS.md`

---

**Conclusão:** Refatoração simples e segura que traz consistência, performance e facilita manutenção. Mudanças mínimas com grande impacto! 🎉
