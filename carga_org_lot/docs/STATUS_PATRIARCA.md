# Documentação: Ciclo de Vida dos Status de Patriarca

## 📊 Visão Geral

Este documento descreve o ciclo de vida completo dos status de um Patriarca no sistema GPP Plataform, incluindo a relação entre os status do Google App Script (GAS) original e os status da tabela `tblstatusprogresso`.

---

## 📊 Tabela de Status (`tblstatusprogresso`)

| ID | Descrição | Status GAS Equivalente | Quando Ocorre |
|----|-----------|----------------------|---------------|
| **1** | Nova Carga | `novo` | Patriarca recém-criado, sem nenhum processamento |
| **2** | Organograma em Progresso | `em progresso` | Usuário enviou arquivo de organograma e está sendo processado |
| **3** | Lotação em Progresso | `em progresso` | Usuário enviou arquivo de lotação e está sendo processado |
| **4** | Pronto para Carga | - | Organograma versionado E lotação importada estão prontos |
| **5** | Carga em Processamento | `enviando carga` | Sistema está enviando dados para API externa |
| **6** | Carga Finalizada | `carga processada` | Processo de envio foi concluído com sucesso |

---

## 🔄 Fluxo Completo do Ciclo de Vida

```
┌─────────────────────────┐
│   1. Nova Carga          │
│   (Patriarca Criado)    │
└────────────┬────────────┘
             │
             │ Usuário seleciona patriarca
             │ e envia organograma
             │
             │
┌────────────┴──────────────────────┐
│   2. Organograma em Progresso   │
│   (Processando organograma)    │
└────────────┬──────────────────────┘
             │
             │ Organograma processado
             │ Usuário envia lotação
             │
             │
┌────────────┴─────────────────────┐
│   3. Lotação em Progresso    │
│   (Processando lotação)      │
└────────────┬─────────────────────┘
             │
             │ Lotação processada
             │ Dados validados
             │
             │
┌────────────┴─────────────────────┐
│   4. Pronto para Carga        │
│   (Organograma + Lotação OK) │
└────────────┬─────────────────────┘
             │
             │ Usuário aciona envio de carga
             │ Sistema inicia transmissão
             │
             │
┌────────────┴──────────────────────┐
│   5. Carga em Processamento   │
│   (Enviando para API)         │
└────────────┬──────────────────────┘
             │
             │ Carga finalizada
             │ API confirmou recebimento
             │
             │
┌────────────┴─────────────────────┐
│   6. Carga Finalizada        │
│   (Processo Concluído)       │
└────────────┬─────────────────────┘
             │
             │ Usuário quer nova carga?
             │ Aciona RESET
             │
             │
┌────────────┴─────────────────────┐
│   RESET para Status 2        │
│   (Novo ciclo de carga)      │
└──────────────────────────────────┘
```

---

## 📝 Detalhamento de Cada Status

### **Status 1: Nova Carga**
- **GAS Equivalente:** `novo`
- **Gatilho:** Criação do patriarca
- **Próximo passo:** Usuário seleciona o patriarca e envia organograma
- **Ações disponíveis:**
  - ✅ Selecionar patriarca
  - ✅ Editar informações
  - ❌ Visualizar detalhes (sem histórico)

---

### **Status 2: Organograma em Progresso**
- **GAS Equivalente:** `em progresso`
- **Gatilho:** Upload de arquivo de organograma
- **Processo:**
  1. Sistema recebe planilha Excel
  2. Valida estrutura hierárquica
  3. Cria versão do organograma
  4. Armazena em `tblorganogramaversao`
- **Próximo passo:** Enviar arquivo de lotação
- **Ações disponíveis:**
  - ✅ Selecionar patriarca
  - ✅ Editar informações
  - ❌ Visualizar detalhes (ainda processando)

---

### **Status 3: Lotação em Progresso**
- **GAS Equivalente:** `em progresso`
- **Gatilho:** Upload de arquivo de lotação
- **Processo:**
  1. Sistema recebe planilha Excel
  2. Valida consistência com organograma
  3. Verifica regras de negócio
  4. Armazena em `tbllotacaoversao`
- **Transição automática:** Status 4 quando processamento OK
- **Ações disponíveis:**
  - ✅ Selecionar patriarca
  - ✅ Editar informações
  - ❌ Visualizar detalhes (ainda processando)

---

### **Status 4: Pronto para Carga**
- **GAS Equivalente:** (não existe no GAS original)
- **Condições para atingir:**
  - ✅ Organograma versionado e validado
  - ✅ Lotação importada e consistente
  - ✅ Todas as validações passaram
- **Próximo passo:** Usuário aciona envio de carga
- **Ações disponíveis:**
  - ✅ Iniciar envio de carga
  - ✅ Editar informações
  - ❌ Visualizar detalhes (sem envio ainda)

---

### **Status 5: Carga em Processamento**
- **GAS Equivalente:** `enviando carga`
- **Gatilho:** Usuário aciona envio de carga
- **Processo:**
  1. Sistema prepara payload JSON
  2. Envia para API externa (ACOES_PNGI)
  3. Monitora progresso em tempo real
  4. Registra logs em `tblcargapatriarca`
- **Timeout:** 1 hora
  - Se `dat_alteracao` > 1 hora: patriarca expira
  - Usuário deve usar "Atualizar e Selecionar" (reset)
- **Ações disponíveis:**
  - ✅ Selecionar (se < 1 hora)
  - 🔄 Atualizar e Selecionar (se ≥ 1 hora)
  - ✅ Editar informações
  - ❌ Visualizar detalhes (ainda enviando)

---

### **Status 6: Carga Finalizada**
- **GAS Equivalente:** `carga processada`
- **Gatilho:** API externa confirma recebimento
- **Indicação:** Processo completo concluído
- **Próximo passo:**
  - Usuário pode consultar detalhes do envio
  - Para nova carga: deve usar função RESET
- **Timeout:** 1 hora
  - Se `dat_alteracao` > 1 hora: patriarca expira
  - Usuário deve usar "Atualizar e Selecionar" (reset)
- **Ações disponíveis:**
  - ✅ Visualizar detalhes ⭐ **(DISPONÍVEL)**
  - ✅ Selecionar (se < 1 hora)
  - 🔄 Atualizar e Selecionar (se ≥ 1 hora)
  - ✅ Editar informações

---

## ⏰ Lógica de Timeout (1 Hora)

### **Cenários**

#### **Status 5 ou 6 com < 1 hora:**
```python
tempo_decorrido = timezone.now() - patriarca.dat_alteracao
horas = tempo_decorrido.total_seconds() / 3600

if horas < 1:
    # Botão: "Selecionar" (verde)
    # Ação: Permite seleção direta
```

#### **Status 5 ou 6 com ≥ 1 hora (EXPIRADO):**
```python
if horas >= 1:
    # Botão: "Atualizar e Selecionar" (azul)
    # Badge: "Expirado" (vermelho)
    # Ação: Reseta para Status 2 + seleciona automaticamente
```

---

## 🎯 Cenários de Ações na Lista de Patriarcas

### **Cenário 1: Status 1 ou 2**
- **Botão:** 🟢 "Selecionar" (verde)
- **Comportamento:** Seleciona patriarca imediatamente
- **Próximo passo:** Upload de organograma/lotação

### **Cenário 2: Status 3 ou 4**
- **Botão:** 🟢 "Selecionar" (verde)
- **Comportamento:** Seleciona patriarca imediatamente
- **Próximo passo:** Continuar processo de carga

### **Cenário 3: Status 5 ou 6 (< 1 hora)**
- **Botão:** 🟢 "Selecionar" (verde)
- **Comportamento:** Seleciona patriarca imediatamente
- **Indicação:** Processo ainda ativo

### **Cenário 4: Status 5 ou 6 (≥ 1 hora)**
- **Botão:** 🔵 "Atualizar e Selecionar" (azul)
- **Badge:** 🔴 "Expirado" (vermelho)
- **Comportamento:**
  1. Reseta `id_status_progresso` para 2
  2. Atualiza `dat_alteracao`
  3. Seleciona patriarca automaticamente
- **Próximo passo:** Nova carga com organograma/lotação

### **Cenário 5: Outros Status**
- **Botão:** ⚪ "Bloqueado" (cinza, desabilitado)
- **Comportamento:** Nenhuma ação possível
- **Indicação:** Status inválido ou corrompido

---

## 🔍 Condições para Visualização de Detalhes

### **Botão "Visualizar Detalhes" Habilitado:**
- ✅ **Status 5:** Carga em Processamento
- ✅ **Status 6:** Carga Finalizada

### **Botão "Visualizar Detalhes" Desabilitado:**
- ❌ **Status 1:** Nova Carga (sem histórico)
- ❌ **Status 2:** Organograma em Progresso (processando)
- ❌ **Status 3:** Lotação em Progresso (processando)
- ❌ **Status 4:** Pronto para Carga (sem envio)

**Tooltip quando desabilitado:**
> "Detalhes disponíveis apenas após envio de carga (status 5 ou 6)"

---

## 🔄 Função RESET

### **Quando usar:**
- Patriarca em Status 5 ou 6 expirado (> 1 hora)
- Usuário deseja fazer nova carga com novos dados

### **O que acontece:**
```python
# 1. Reseta status
patriarca.id_status_progresso = 2  # Organograma em Progresso

# 2. Atualiza timestamp
patriarca.dat_alteracao = timezone.now()

# 3. Seleciona automaticamente
request.session['patriarca_selecionado'] = {...}

# 4. Redireciona para dashboard
return redirect('carga_org_lot:dashboard')
```

### **Modal de confirmação:**
```
⚠️ Atenção:
- O status será alterado para "Em Progresso"
- O patriarca será selecionado automaticamente
- Você poderá realizar novo envio de cargas
```

---

## 📊 Controle de Versões

### **Status 2 e 3: Controlados por versões**

```python
# Status 2: Organograma em Progresso
if patriarca.tem_organograma_ativo:
    # Existe versão ativa em tblorganogramaversao
    status = 2

# Status 3: Lotação em Progresso  
if patriarca.tem_lotacao_ativa:
    # Existe versão ativa em tbllotacaoversao
    # para o organograma versionado
    status = 3
```

### **Relacionamento:**
```
tblpatriarca (1) ---< (N) tblorganogramaversao
                            (1) ---< (N) tbllotacaoversao
```

---

## 🛠️ Implementação Técnica

### **Arquivos Relevantes:**

1. **`carga_org_lot/models.py`**
   - `TblPatriarca`
   - `TblStatusProgresso`
   - `TblOrganogramaVersao`
   - `TblLotacaoVersao`

2. **`carga_org_lot/views/web_views/patriarca_views.py`**
   - `patriarca_list()` - Lógica de ações
   - `patriarca_select()` - Seleção
   - `patriarca_reset()` - Reset para novo ciclo

3. **`carga_org_lot/templates/carga_org_lot/patriarca_list.html`**
   - Renderização de botões condicionais
   - Modal de confirmação
   - Badges de status

---

## 📝 Referências

- **Código GAS Original:** `carregarPatriarcas()`, `setSelectedPatriarca()`, `resetPatriarca()`
- **Branch:** `feature/menu-sistema-carga`
- **Issues relacionadas:** Migração GAS para Django

---

## 📅 Versionamento

| Versão | Data | Autor | Alterações |
|---------|------|-------|-------------|
| 1.0 | 04/02/2026 | GPP Team | Documentação inicial do ciclo de vida |

---

**Última atualização:** 04 de fevereiro de 2026
