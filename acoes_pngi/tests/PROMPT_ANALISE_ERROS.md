# 🔍 Prompt para Análise de Erros nos Testes

## 📋 Como Usar Este Prompt

1. Execute os testes e capture o log completo
2. Copie o prompt abaixo
3. Anexe o log dos testes
4. Envie para análise

---

## 📝 Prompt para Copiar

```markdown
Ao rodar meus testes ainda estão dando problemas.

Contexto:
- Branch: fix/correcao-massiva-testes-pngi
- GitHub: https://github.com/ProjetcsGPP/gpp_plataform/tree/fix/correcao-massiva-testes-pngi
- Já executei o script fix_all_test_errors.py
- Arquivos de referência 100% OK: test_api_views_acoes.py, test_api_alinhamento_views.py, test_api_responsavel_views.py

Por favor:
1. Analise o log anexado e identifique os PADRÕES de erro
2. Agrupe os erros por tipo (ValidationError, AttributeError, AssertionError, etc)
3. Para cada tipo de erro:
   - Identifique a causa raiz
   - Liste todos os arquivos afetados
   - Sugira a correção específica
4. Crie um script Python automatizado para corrigir TODOS os erros encontrados
5. Siga o padrão dos arquivos que estão funcionando (test_api_views_acoes.py)

LOG DOS TESTES:
```

[COLE AQUI O LOG COMPLETO DOS TESTES]

```
```

---

## 🔧 Como Gerar o Log Completo

### Opção 1: Log Detalhado com Verbosidade Máxima (RECOMENDADO)

```bash
# No diretório raiz do projeto
cd /caminho/para/gpp_plataform

# Checkout da branch
git checkout fix/correcao-massiva-testes-pngi

# Rodar testes com verbosidade máxima e salvar log
python manage.py test acoes_pngi.tests --verbosity=2 2>&1 | tee teste_log_completo.txt

# O arquivo teste_log_completo.txt conterá o log completo
```

### Opção 2: Log Resumido (mais rápido)

```bash
# Rodar apenas para ver resumo
python manage.py test acoes_pngi.tests 2>&1 | tee teste_log_resumo.txt
```

### Opção 3: Log de Arquivo Específico

```bash
# Se quiser testar apenas um arquivo problemático
python manage.py test acoes_pngi.tests.test_api_views --verbosity=2 2>&1 | tee teste_api_views_log.txt
```

---

## 📊 Formato do Log Esperado

O log deve conter:

```
Ran XXX tests in XX.XXXs

FAILED (failures=XX, errors=XX)

======================================================================
ERROR: test_nome_do_teste (acoes_pngi.tests.test_arquivo.ClasseDeTeste)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/caminho/para/arquivo.py", line XXX, in test_nome
    ...
TipoDeErro: Mensagem de erro

======================================================================
FAIL: test_outro_teste (acoes_pngi.tests.test_arquivo.OutraClasse)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/caminho/para/arquivo.py", line XXX, in test_outro
    ...
AssertionError: Mensagem de asserção

...
```

---

## 🎯 Informações Úteis para Incluir

### Status Atual
```
Total de testes: XXX
Falhas: XX
Erros: XX
Arquivos com 100% OK: test_api_views_acoes.py, test_api_alinhamento_views.py, test_api_responsavel_views.py
```

### Correções Já Aplicadas
- ✅ Script fix_all_test_errors.py executado
- ✅ ValidationError datfinalvigencia corrigido em ALGUNS arquivos
- ✅ AttributeError self.eixo/vigencia corrigido em test_api_views.py

### Arquivos Problemáticos Conhecidos
- test_diagnostic_api.py
- test_web_acoes_views.py
- test_web_views_complete.py
- test_api_views.py (parcialmente corrigido)
- test_context_processors.py
- test_permissions.py

---

## 💡 Dicas para Melhor Análise

1. **Incluir o log COMPLETO**: Não corte o início nem o fim
2. **Incluir estatísticas**: "Ran XXX tests in XX.XXXs"
3. **Incluir TODOS os tracebacks**: Não omita erros
4. **Mencionar alterações**: Se fez alguma correção manual, mencione
5. **Contexto adicional**: Se algum teste específico é crítico, mencione

---

## 🔄 Workflow Completo

```bash
# 1. Atualizar branch
git checkout fix/correcao-massiva-testes-pngi
git pull origin fix/correcao-massiva-testes-pngi

# 2. Executar script de correção (se não executou ainda)
python acoes_pngi/tests/fix_all_test_errors.py

# 3. Rodar testes e capturar log
python manage.py test acoes_pngi.tests --verbosity=2 2>&1 | tee teste_log_$(date +%Y%m%d_%H%M%S).txt

# 4. Copiar conteúdo do arquivo teste_log_*.txt
cat teste_log_*.txt

# 5. Usar o prompt acima com o log anexado
```

---

## 📁 Exemplo de Estrutura de Resposta Esperada

Após enviar o prompt com o log, espere uma resposta estruturada assim:

```markdown
## Análise dos Erros

### Grupo 1: ValidationError (15 ocorrências)
**Arquivos afetados:** file1.py, file2.py, file3.py
**Causa:** Campo X está faltando
**Correção:** Adicionar campo X em todas as ocorrências

### Grupo 2: AttributeError (8 ocorrências)
**Arquivos afetados:** file4.py, file5.py
**Causa:** Atributo Y não inicializado
**Correção:** Inicializar Y no setUp()

### Grupo 3: AssertionError (20 ocorrências)
**Arquivos afetados:** file6.py, file7.py
**Causa:** Fixtures incompletas
**Correção:** Adicionar relacionamentos obrigatórios

## Script de Correção Automatizado

[Script Python completo para corrigir todos os erros]
```

---

## ⚠️ Notas Importantes

- **Backup**: Sempre faça commit antes de aplicar correções em massa
- **Revisão**: Revise o diff antes de commitar as correções
- **Testes incrementais**: Após correções, rode os testes novamente
- **Documentação**: Mantenha registro das correções aplicadas

---

**Criado em:** 12/02/2026  
**Branch:** fix/correcao-massiva-testes-pngi  
**Última atualização:** 12/02/2026
