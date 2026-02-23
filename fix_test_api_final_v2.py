# fix_test_api_final_v2.py

filepath = r"C:\Projects\gpp_plataform\acoes_pngi\tests\test_api_views_acoes.py"

print("Lendo arquivo...")
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print("Aplicando correções...")

# ===== 1. CORRIGIR BaseAPITestCase.setup_test_data =====
old_base_setup = '''    def setup_test_data(self):
        # Criar Eixo (se não existe)
        if not hasattr(self, 'eixo') or self.eixo is None:
            self.eixo = Eixo.objects.create(
                stralias='E1',
                strdescricaoeixo='Eixo 1 - Gestão'
            )

        # Criar SituacaoAcao (se não existe)
        if not hasattr(self, 'situacao') or self.situacao is None:
            self.situacao = SituacaoAcao.objects.create(
                strdescricaosituacao='Em Andamento'
            )

        """Override em subclasses"""
        pass'''

new_base_setup = '''    def setup_test_data(self):
        """Cria dados base compartilhados - Override em subclasses"""
        # Criar Eixo (compartilhado)
        self.eixo, _ = Eixo.objects.get_or_create(
            stralias='E1',
            defaults={'strdescricaoeixo': 'Eixo 1 - Gestão'}
        )

        # Criar SituacaoAcao (compartilhada)
        self.situacao, _ = SituacaoAcao.objects.get_or_create(
            strdescricaosituacao='Em Andamento'
        )'''

content = content.replace(old_base_setup, new_base_setup)

# ===== 2. CORRIGIR TipoEntraveAlertaAPITests.setup_test_data =====
old_tipo = '''    def setup_test_data(self):
        # Criar Eixo (se não existe)
        if not hasattr(self, 'eixo') or self.eixo is None:
            self.eixo = Eixo.objects.create(
                stralias='E1',
                strdescricaoeixo='Eixo 1 - Gestão'
            )

        # Criar SituacaoAcao (se não existe)
        if not hasattr(self, 'situacao') or self.situacao is None:
            self.situacao = SituacaoAcao.objects.create(
                strdescricaosituacao='Em Andamento'
            )

        """Cria tipo de entrave/alerta de teste"""
        self.tipo_entrave = TipoEntraveAlerta.objects.create(
            strdescricaotipoentravealerta='Alerta de Teste'
        )'''

new_tipo = '''    def setup_test_data(self):
        """Cria tipo de entrave/alerta de teste"""
        super().setup_test_data()
        self.tipo_entrave = TipoEntraveAlerta.objects.create(
            strdescricaotipoentravealerta='Alerta de Teste'
        )'''

content = content.replace(old_tipo, new_tipo)

# ===== 3. CORRIGIR AcoesAPITests.setup_test_data =====
old_acoes = '''    def setup_test_data(self):
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

new_acoes = '''    def setup_test_data(self):
        """Cria dados COMPLETOS necessários para ações - simula ambiente real"""
        super().setup_test_data()
        
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

content = content.replace(old_acoes, new_acoes)

# ===== 4. Corrigir referências no resto do código =====
# Substituir self.vigencia_base por self.vigencia
content = content.replace('self.vigencia_base', 'self.vigencia')
content = content.replace('self.eixo_base', 'self.eixo')
content = content.replace('self.situacao_base', 'self.situacao')
content = content.replace('self.situacao   # Adicionar para consistência', 'self.situacao')

# ===== 5. CORRIGIR AcaoPrazoAPITests.setup_test_data =====
old_prazo = '''    def setup_test_data(self):
        """Cria TODOS relacionamentos necessários - simula ambiente real"""
        
        # ✅ 1. Criar Vigência (necessária para Acao)
        self.vigencia = VigenciaPNGI.objects.create(
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
        
        # ✅ 4. Criar Acao COMPLETA (AcaoPrazo.idacao é obrigatório)
        self.acao = Acoes.objects.create(
            strapelido='ACAO-001',
            strdescricaoacao='Ação Teste',
            strdescricaoentrega='Entrega Teste',
            idvigenciapngi=self.vigencia,  # OBRIGATÓRIO
            ideixo=eixo,              # Adicionar para consistência
            idsituacaoacao=situacao   # Adicionar para consistência
        )
        
        # ✅ 5. Criar Prazo vinculado à Acao
        self.prazo = AcaoPrazo.objects.create(
            idacao=self.acao,  # OBRIGATÓRIO
            strprazo='2026-06-30',
            isacaoprazoativo=True
        )'''

new_prazo = '''    def setup_test_data(self):
        """Cria TODOS relacionamentos necessários - simula ambiente real"""
        super().setup_test_data()
        
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

content = content.replace(old_prazo, new_prazo)

# ===== 6. CORRIGIR AcaoDestaqueAPITests.setup_test_data =====
old_destaque = '''    def setup_test_data(self):
        """Cria TODOS relacionamentos necessários - simula ambiente real"""
        
        # ✅ 1. Criar Vigência (necessária para Acao)
        self.vigencia = VigenciaPNGI.objects.create(
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
            idvigenciapngi=self.vigencia,  # OBRIGATÓRIO
            ideixo=eixo,              # Adicionar para consistência
            idsituacaoacao=situacao   # Adicionar para consistência
        )
        
        # ✅ 5. Criar Destaque vinculado à Acao
        self.destaque = AcaoDestaque.objects.create(
            idacao=self.acao,  # OBRIGATÓRIO
            datdatadestaque=timezone.now()
        )'''

new_destaque = '''    def setup_test_data(self):
        """Cria TODOS relacionamentos necessários - simula ambiente real"""
        super().setup_test_data()
        
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

content = content.replace(old_destaque, new_destaque)

print("Salvando arquivo...")
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ ARQUIVO CORRIGIDO!")
