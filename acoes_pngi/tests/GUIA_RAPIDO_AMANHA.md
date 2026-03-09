# ⏰ Guia Rápido para Amanhã

## 🚀 Passos para Executar Amanhã

### 1️⃣ Atualizar e Preparar Ambiente (2 min)

```bash
# Navegar para o projeto
cd /caminho/para/gpp_plataform

# Atualizar branch
git checkout fix/correcao-massiva-testes-pngi
git pull origin fix/correcao-massiva-testes-pngi

# Verificar status
git status
```

### 2️⃣ Executar Script de Correção (1 min)

```bash
# Executar script de correção automatizada
python acoes_pngi/tests/fix_all_test_errors.py

# Verificar output do script
# Deve mostrar: "✅ Correções concluídas!"
```

### 3️⃣ Rodar Testes e Capturar Log (3-5 min)

```bash
# Rodar todos os testes com log detalhado
python manage.py test acoes_pngi.tests --verbosity=2 2>&1 | tee teste_log_$(date +%Y%m%d_%H%M%S).txt

# Aguardar conclusão...
# O arquivo teste_log_YYYYMMDD_HHMMSS.txt será criado automaticamente
```

### 4️⃣ Abrir e Copiar o Log (1 min)

```bash
# Listar arquivos de log criados
ls -lh teste_log_*.txt

# Abrir o último arquivo criado
cat teste_log_*.txt

# OU se preferir abrir no editor
code teste_log_*.txt  # VSCode
nano teste_log_*.txt  # Terminal
```

### 5️⃣ Usar o Prompt Pré-Pronto (2 min)

1. **Abrir arquivo:** `acoes_pngi/tests/PROMPT_ANALISE_ERROS.md`
2. **Copiar a seção:** "Prompt para Copiar"
3. **Colar no chat**
4. **Anexar o log completo** que você copiou no passo 4
5. **Enviar!**

---

## 📝 Prompt Pronto (Copiar e Colar)

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

[COLE AQUI O LOG COMPLETO]

```
```

---

## 📋 Checklist rápido

- [ ] Git pull na branch fix/correcao-massiva-testes-pngi
- [ ] Executar fix_all_test_errors.py
- [ ] Rodar testes com `--verbosity=2` e salvar log
- [ ] Copiar log completo do arquivo teste_log_*.txt
- [ ] Abrir PROMPT_ANALISE_ERROS.md
- [ ] Copiar prompt pré-pronto
- [ ] Anexar log completo
- [ ] Enviar para análise

---

## 🔗 Links Úteis

### Arquivos na Branch
- [Script de Correção](https://github.com/ProjetcsGPP/gpp_plataform/blob/fix/correcao-massiva-testes-pngi/acoes_pngi/tests/fix_all_test_errors.py)
- [Documentação do Script](https://github.com/ProjetcsGPP/gpp_plataform/blob/fix/correcao-massiva-testes-pngi/acoes_pngi/tests/README_FIX_ALL_ERRORS.md)
- [Prompt de Análise](https://github.com/ProjetcsGPP/gpp_plataform/blob/fix/correcao-massiva-testes-pngi/acoes_pngi/tests/PROMPT_ANALISE_ERROS.md)

### Arquivos de Referência (100% OK)
- [test_api_views_acoes.py](https://github.com/ProjetcsGPP/gpp_plataform/blob/fix/correcao-massiva-testes-pngi/acoes_pngi/tests/test_api_views_acoes.py)
- [test_api_alinhamento_views.py](https://github.com/ProjetcsGPP/gpp_plataform/blob/fix/correcao-massiva-testes-pngi/acoes_pngi/tests/test_api_alinhamento_views.py)
- [test_api_responsavel_views.py](https://github.com/ProjetcsGPP/gpp_plataform/blob/fix/correcao-massiva-testes-pngi/acoes_pngi/tests/test_api_responsavel_views.py)

---

## 💡 Dicas para Economizar Tempo

### Se Tiver Pouco Tempo
```bash
# Versão rápida (sem verbosidade)
python manage.py test acoes_pngi.tests 2>&1 | tee teste_log_quick.txt
```

### Se Quiser Testar Só Um Arquivo
```bash
# Testar arquivo específico
python manage.py test acoes_pngi.tests.test_api_views --verbosity=2
```

### Se Quiser Ver Apenas Resumo
```bash
# Ver apenas últimas linhas do log
tail -n 100 teste_log_*.txt
```

---

## ⚠️ Troubleshooting

### Problema: "No module named 'acoes_pngi'"
```bash
# Certifique-se de estar no diretório raiz
pwd  # Deve mostrar: /caminho/para/gpp_plataform
cd /caminho/para/gpp_plataform
```

### Problema: "Database not found"
```bash
# Rodar migrações
python manage.py migrate
python manage.py migrate --database=gpp_plataform_db
```

### Problema: Script não encontrado
```bash
# Verificar se arquivo existe
ls -lh acoes_pngi/tests/fix_all_test_errors.py

# Se não existe, fazer pull novamente
git pull origin fix/correcao-massiva-testes-pngi
```

---

## 📊 O Que Esperar

### Melhor Cenário 🎉
```
Ran 368 tests in ~14s
OK
```

### Cenário Realista 🔧
```
Ran 368 tests in ~14s
FAILED (failures=X, errors=Y)
# Onde X+Y < 76 (redução de erros)
```

### Pior Cenário ⚠️
```
Ran 368 tests in ~14s
FAILED (failures=25, errors=51)
# Mesma quantidade de erros
```

**Se for o pior cenário:** Use o prompt para análise detalhada!

---

## 🔄 Workflow Completo em 1 Comando

```bash
# Fazer TUDO de uma vez (recomendado)
git checkout fix/correcao-massiva-testes-pngi && \
git pull origin fix/correcao-massiva-testes-pngi && \
python acoes_pngi/tests/fix_all_test_errors.py && \
python manage.py test acoes_pngi.tests --verbosity=2 2>&1 | tee teste_log_$(date +%Y%m%d_%H%M%S).txt
```

**Depois:** Abrir `PROMPT_ANALISE_ERROS.md` e usar o prompt com o log

---

## 📞 Contato e Suporte

Se tiver dúvidas:
1. Revisar documentação: `README_FIX_ALL_ERRORS.md`
2. Verificar exemplos: Arquivos `test_api_views_acoes.py`
3. Usar o prompt de análise com log anexado

---

**Criado em:** 12/02/2026, 17:02
**Para usar em:** 13/02/2026 (amanhã)
**Tempo estimado:** 10-15 minutos
**Branch:** fix/correcao-massiva-testes-pngi

✅ **Tudo pronto para amanhã!**
