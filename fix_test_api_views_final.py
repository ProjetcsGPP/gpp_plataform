# fix_test_api_views_final.py
import re

filepath = r"C:\Projects\gpp_plataform\acoes_pngi\tests\test_api_views_acoes.py"

print("Lendo arquivo...")
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print("Aplicando correções...")

# ===== 1. CORRIGIR get_or_create em vez de create =====
# Base class setup_test_data
content = re.sub(
    r'if not hasattr\(self, \'eixo\'\) or self\.eixo is None:\s+self\.eixo = Eixo\.objects\.create\(',
    'if not hasattr(self, \'eixo\'\) or self.eixo is None:\n            self.eixo, _ = Eixo.objects.get_or_create(',
    content
)

content = re.sub(
    r'if not hasattr\(self, \'situacao\'\) or self\.situacao is None:\s+self\.situacao = SituacaoAcao\.objects\.create\(',
    'if not hasattr(self, \'situacao\'\) or self.situacao is None:\n            self.situacao, _ = SituacaoAcao.objects.get_or_create(',
    content
)

# TipoEntraveAlertaAPITests.setup_test_data
content = content.replace(
    '''    def setup_test_data(self):
        # Criar Eixo (se não existe)
        if not hasattr(self, 'eixo') or self.eixo is None:
            self.eixo, _ = Eixo.objects.get_or_create(
                stralias='E1',
                strdescricaoeixo='Eixo 1 - Gestão'
            )

        # Criar SituacaoAcao (se não existe)
        if not hasattr(self, 'situacao') or self.situacao is None:
            self.situacao, _ = SituacaoAcao.objects.get_or_create(
                strdescricaosituacao='Em Andamento'
            )

        """Cria tipo de entrave/alerta de teste"""
        self.tipo_entrave = TipoEntraveAlerta.objects.create(
            strdescricaotipoentravealerta='Alerta de Teste'
        )''',
    '''    def setup_test_data(self):
        """Cria tipo de entrave/alerta de teste"""
        super().setup_test_data()  # Chama setup da base
        self.tipo_entrave = TipoEntraveAlerta.objects.create(
            strdescricaotipoentravealerta='Alerta de Teste'
        )'''
)

# ===== 2. CORRIGIR AcoesAPITests.setup_test_data =====
# Encontrar o método setup_test_data de AcoesAPITests
acoes_setup = '''    def setup_test_data(self):
        """Cria dados COMPLETOS necessários para ações - simula ambiente real"""
        
        # ✅ 1. Criar Vigência (OBRIGATÓRIO para Acao)        
        # ✅ 2. Criar Eixo (OPCIONAL, mas usado na prática)        
        # ✅ 3. Criar Situação (OPCIONAL, mas usado na prática)        
        # ✅ 4. Criar Tipo Entrave (OPCIONAL)
        self.tipo_entrave = TipoEntraveAlerta.objects.create(
            strdescricaotipoentravealerta='Alerta Teste'
        )
        
        # ✅ 5. Criar Ação COMPLETA com TODOS relacionamentos
        self.acao = Acoes.objects.create(
            strapelido='ACAO-001',
            strdescricaoacao='Ação de Teste',
            strdescricaoentrega='Entrega de Teste',
            idvigenciapngi=self.vigencia_base,  # OBRIGATÓRIO
            ideixo=self.eixo_base,              # OPCIONAL (mas comum,
            idsituacaoacao=self.situacao_base,  # OPCIONAL (mas comum)
            idtipoentravealerta=self.tipo_entrave,  # OPCIONAL
            datdataentrega=date(2026, 6, 30)
        )'''

acoes_setup_correto = '''    def setup_test_data(self):
        """Cria dados COMPLETOS necessários para ações - simula ambiente real"""
        super().setup_test_data()  # Chama setup da base
        
        # Criar Vigência (OBRIGATÓRIO para Acao)
        self.vigencia, _ = VigenciaPNGI.objects.get_or_create(
            strdescricaovigenciapngi='PNGI 2026',
            defaults={
                'datiniciovigencia': date(2026, 1, 1),
                'datfinalvigencia': date(2026, 12, 31)
            }
        )
        
        # Criar Tipo Entrave (OPCIONAL)
        self.tipo_entrave = TipoEntraveAlerta.objects.create(
            strdescricaotipoentravealerta='Alerta Teste'
        )
        
        # Criar Ação COMPLETA com TODOS relacionamentos
        self.acao = Acoes.objects.create(
            strapelido='ACAO-001',
            strdescricaoacao='Ação de Teste',
            strdescricaoentrega='Entrega de Teste',
            idvigenciapngi=self.vigencia,
            ideixo=self.eixo,
            idsituacaoacao=self.situacao,
            idtipoentravealerta=self.tipo_entrave,
            datdataentrega=date(2026, 6, 30)
        )'''

content = content.replace(acoes_setup, acoes_setup_correto)

# ===== 3. CORRIGIR referencias a self.vigencia_base, self.eixo_base, etc =====
# Em AcoesAPITests
content = re.sub(
    r"idvigenciapngi=self\.vigencia_base,",
    "idvigenciapngi=self.vigencia,",
    content
)
content = re.sub(
    r"ideixo=self\.eixo_base,",
    "ideixo=self.eixo,",
    content
)
content = re.sub(
    r"idsituacaoacao=self\.situacao_base",
    "idsituacaoacao=self.situacao",
    content
)
content = re.sub(
    r"idsituacaoacao=self\.situacao   # Adicionar para consistência",
    "idsituacaoacao=self.situacao",
    content
)

# ===== 4. CORRIGIR AcaoPrazoAPITests.setup_test_data =====
prazo_setup_old = '''    def setup_test_data(self):
        """Cria TODOS relacionamentos necessários - simula ambiente real"""
        
        # ✅ 1. Criar Vigência (necessária para Acao)
        self.vigencia_base = VigenciaPNGI.objects.create(
            strdescricaovigenciapngi='PNGI 2026',
            datiniciovigencia=date(2026, 1, 1),
            datfinalvigencia=date(2026, 12, 31),        )
        
        # ✅ 2. Criar Eixo (opcional mas comum)
        eixo = Eixo.objects.create(
            stralias='E1',
            strdescricaoeixoEixo 1 - Gestão'
        )
        
        # ✅ 3. Criar Situação (opcional mas comum)
        situacao = SituacaoAcao.objects.create(
            strdescricaosituacao='Em Andamento'
        )
        
        # ✅ 4. Criar Acao COMPLETA (AcaoPrazo.idacao é obrigatório)
        self.acao = Acoes.objects.create(
            strapelido='ACAO-001',
            strdescricaoacao='Ação Teste',
            strdescricaoentrega='Entrega Teste',
            idvigenciapngi=self.vigencia_base,  # OBRIGATÓRIO
            ideixo=eixo,              # Adicionar para consistência
            idsituacaoacao=situacao   # Adicionar para consistência
        )
        
        # ✅ 5. Criar Prazo vinculado à Acao
        self.prazo = AcaoPrazo.objects.create(
            idacao=self.acao,  # OBRIGATÓRIO
            strprazo='2026-06-30',
            isacaoprazoativo=True
        )'''

prazo_setup_new = '''    def setup_test_data(self):
        """Cria TODOS relacionamentos necessários - simula ambiente real"""
        super().setup_test_data()  # Chama setup da base
        
        # Criar Vigência (necessária para Acao)
        self.vigencia, _ = VigenciaPNGI.objects.get_or_create(
            strdescricaovigenciapngi='PNGI 2026',
            defaults={
                'datiniciovigencia': date(2026, 1, 1),
                'datfinalvigencia': date(2026, 12, 31)
            }
        )
        
        # Criar Acao COMPLETA (AcaoPrazo.idacao é obrigatório)
        self.acao = Acoes.objects.create(
            strapelido='ACAO-001',
            strdescricaoacao='Ação Teste',
            strdescricaoentrega='Entrega Teste',
            idvigenciapngi=self.vigencia,
            ideixo=self.eixo,
            idsituacaoacao=self.situacao
        )
        
        # Criar Prazo vinculado à Acao
        self.prazo = AcaoPrazo.objects.create(
            idacao=self.acao,
            strprazo='2026-06-30',
            isacaoprazoativo=True
        )'''

content = content.replace(prazo_setup_old, prazo_setup_new)

# ===== 5. CORRIGIR AcaoDestaqueAPITests.setup_test_data =====
destaque_setup_old = '''    def setup_test_data(self):
        """Cria TODOS relacionamentos necessários - simula ambiente real"""
        
        # ✅ 1. Criar Vigência (necessária para Acao)
        self.vigencia_base = VigenciaPNGI.objects.create(
            strdescricaovigenciapngi='PNGI 2026',
            datiniciovigencia=date(2026, 1, 1),
            datfinalvigencia=date(2026, 12, 31),        )
        
        # ✅ 2. Criar Eixo (opcional mas comum)
        eixo = Eixo.objects.create(
            stralias='E1',
            strdescricaoeixo='Eixo 1 - Gestão'
        )
        
        # ✅ 3. Criar Situação (opcional mas comum)
        situacao = SituacaoAcao.objects.create(
            strdescricaosituacao='Em Andamento'
        )
        
        # ✅ 4. Criar Acao COMPLETA (AcaoDestaque.idacao é obrigatório)
        self.acao = Acoes.objects.create(
            strapelido='ACAO-001',
            strdescricaoacao='Ação Teste',
            strdescricaoentrega='Entrega Teste',
            idvigenciapngi=self.vigencia_base,  # OBRIGATÓRIO
            ideixo=eixo,              # Adicionar para consistência
            idsituacaoacao=situacao   # Adicionar para consistência
        )
        
        # ✅ 5. Criar Destaque vinculado à Acao
        self.destaque = AcaoDestaque.objects.create(
            idacao=self.acao,  # OBRIGATÓRIO
            datdatadestaque=timezone.now()
        )'''

destaque_setup_new = '''    def setup_test_data(self):
        """Cria TODOS relacionamentos necessários - simula ambiente real"""
        super().setup_test_data()  # Chama setup da base
        
        # Criar Vigência (necessária para Acao)
        self.vigencia, _ = VigenciaPNGI.objects.get_or_create(
            strdescricaovigenciapngi='PNGI 2026',
            defaults={
                'datiniciovigencia': date(2026, 1, 1),
                'datfinalvigencia': date(2026, 12, 31)
            }
        )
        
        # Criar Acao COMPLETA (AcaoDestaque.idacao é obrigatório)
        self.acao = Acoes.objects.create(
            strapelido='ACAO-001',
            strdescricaoacao='Ação Teste',
            strdescricaoentrega='Entrega Teste',
            idvigenciapngi=self.vigencia,
            ideixo=self.eixo,
            idsituacaoacao=self.situacao
        )
        
        # Criar Destaque vinculado à Acao
        self.destaque = AcaoDestaque.objects.create(
            idacao=self.acao,
            datdatadestaque=timezone.now()
        )'''

content = content.replace(destaque_setup_old, destaque_setup_new)

# ===== 6. CORRIGIR defaults nas chamadas get_or_create =====
content = content.replace(
    "self.eixo, _ = Eixo.objects.get_or_create(\n                stralias='E1',\n                strdescricaoeixo='Eixo 1 - Gestão'\n            )",
    "self.eixo, _ = Eixo.objects.get_or_create(\n                stralias='E1',\n                defaults={'strdescricaoeixo': 'Eixo 1 - Gestão'}\n            )"
)

content = content.replace(
    "self.situacao, _ = SituacaoAcao.objects.get_or_create(\n                strdescricaosituacao='Em Andamento'\n            )",
    "self.situacao, _ = SituacaoAcao.objects.get_or_create(\n                strdescricaosituacao='Em Andamento'\n            )"
)

print("Salvando arquivo...")
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ CORREÇÕES APLICADAS!")
print("\nResumo das correções:")
print("1. ✅ get_or_create() para Eixo e Situacao na BaseAPITestCase")
print("2. ✅ super().setup_test_data() nas subclasses")
print("3. ✅ Corrigidos atributos self.vigencia, self.eixo, self.situacao")
print("4. ✅ Removidas duplicações de criação de objetos")
print("5. ✅ Corrigidos defaults no get_or_create")
