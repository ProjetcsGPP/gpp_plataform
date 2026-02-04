"""
Forms do módulo Carga Org/Lot
"""

from django import forms
from django.core.exceptions import ValidationError
import uuid
from .models import TblPatriarca, TblStatusProgresso


class PatriarcaForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Patriarca
    
    Campos disponíveis:
    - str_sigla_patriarca: Sigla do patriarca (ex: SEGER)
    - str_nome: Nome completo do órgão
    - id_externo_patriarca: UUID do patriarca no sistema PRODEST
    
    Campo id_status_progresso foi removido:
    - Novo patriarca sempre começa com status 1 (Nova Carga)
    - Edição não pode alterar status (gerenciado pelo sistema)
    """
    
    class Meta:
        model = TblPatriarca
        fields = ['str_sigla_patriarca', 'str_nome', 'id_externo_patriarca']
        labels = {
            'str_sigla_patriarca': 'Sigla do Patriarca',
            'str_nome': 'Nome Completo',
            'id_externo_patriarca': 'Id Patriarca - PRODEST',
        }
        widgets = {
            'str_sigla_patriarca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: SEGER, SEDU, SEJUS',
                'maxlength': '20',
                'style': 'text-transform: uppercase;',
                'required': True
            }),
            'str_nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Secretaria de Estado de Gestão e Recursos Humanos',
                'maxlength': '255',
                'required': True
            }),
            'id_externo_patriarca': forms.TextInput(attrs={
                'class': 'form-control font-monospace',
                'placeholder': 'Ex: 123e4567-e89b-12d3-a456-426614174000',
                'maxlength': '36',
                'required': True,
                'pattern': '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'
            }),
        }
        help_texts = {
            'str_sigla_patriarca': 'Sigla única que identifica o órgão patriarca (máx. 20 caracteres)',
            'str_nome': 'Nome completo do órgão ou entidade',
            'id_externo_patriarca': 'UUID do patriarca no sistema PRODEST (formato: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)',
        }
    
    def clean_str_sigla_patriarca(self):
        """
        Validação customizada para sigla
        """
        sigla = self.cleaned_data.get('str_sigla_patriarca', '').strip().upper()
        
        if not sigla:
            raise ValidationError('A sigla é obrigatória.')
        
        if len(sigla) < 2:
            raise ValidationError('A sigla deve ter pelo menos 2 caracteres.')
        
        # Verificar duplicação
        qs = TblPatriarca.objects.filter(str_sigla_patriarca=sigla)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        
        if qs.exists():
            raise ValidationError(f'Já existe um patriarca com a sigla "{sigla}".')
        
        return sigla
    
    def clean_str_nome(self):
        """
        Validação customizada para nome
        """
        nome = self.cleaned_data.get('str_nome', '').strip()
        
        if not nome:
            raise ValidationError('O nome é obrigatório.')
        
        if len(nome) < 3:
            raise ValidationError('O nome deve ter pelo menos 3 caracteres.')
        
        return nome
    
    def clean_id_externo_patriarca(self):
        """
        Validação customizada para ID externo (UUID)
        """
        id_externo = self.cleaned_data.get('id_externo_patriarca', '').strip()
        
        if not id_externo:
            raise ValidationError('O Id Patriarca - PRODEST é obrigatório.')
        
        # Validar formato UUID
        try:
            uuid_obj = uuid.UUID(id_externo, version=4)
            # Garantir que o UUID está no formato correto (lowercase, com hifens)
            id_externo_formatado = str(uuid_obj)
        except (ValueError, AttributeError):
            raise ValidationError(
                'Formato inválido. O Id Patriarca - PRODEST deve ser um UUID válido '
                '(formato: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx).'
            )
        
        # Verificar duplicação
        qs = TblPatriarca.objects.filter(id_externo_patriarca=uuid_obj)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        
        if qs.exists():
            raise ValidationError(
                f'Já existe um patriarca com o Id Patriarca - PRODEST "{id_externo_formatado}".'
            )
        
        return uuid_obj


class OrganogramaUploadForm(forms.Form):
    """
    Formulário para upload de arquivo de organograma
    """
    
    FONTE_CHOICES = [
        ('LOCAL', 'Upload do Computador'),
        ('GOOGLE_DRIVE', 'Google Drive'),
    ]
    
    fonte = forms.ChoiceField(
        choices=FONTE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Origem do Arquivo',
        initial='LOCAL'
    )
    
    arquivo_local = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls,.ods,.docx,.doc'
        }),
        label='Selecionar Arquivo',
        help_text='Formatos aceitos: Excel (.xlsx, .xls), LibreOffice Calc (.ods), Word (.docx, .doc)'
    )
    
    arquivo_google_drive_id = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ID do arquivo no Google Drive'
        }),
        label='ID do Arquivo (Google Drive)',
        help_text='Cole o ID do arquivo compartilhado no Google Drive'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        fonte = cleaned_data.get('fonte')
        arquivo_local = cleaned_data.get('arquivo_local')
        arquivo_google_drive_id = cleaned_data.get('arquivo_google_drive_id')
        
        if fonte == 'LOCAL' and not arquivo_local:
            raise ValidationError('Selecione um arquivo do computador.')
        
        if fonte == 'GOOGLE_DRIVE' and not arquivo_google_drive_id:
            raise ValidationError('Informe o ID do arquivo do Google Drive.')
        
        # Validar extensão do arquivo local
        if arquivo_local:
            nome_arquivo = arquivo_local.name.lower()
            extensoes_validas = ['.xlsx', '.xls', '.ods', '.docx', '.doc']
            
            if not any(nome_arquivo.endswith(ext) for ext in extensoes_validas):
                raise ValidationError(
                    f'Formato de arquivo inválido. Use: {", ".join(extensoes_validas)}'
                )
        
        return cleaned_data


class LotacaoUploadForm(forms.Form):
    """
    Formulário para upload de arquivo de lotação
    """
    
    FONTE_CHOICES = [
        ('LOCAL', 'Upload do Computador'),
        ('GOOGLE_DRIVE', 'Google Drive'),
    ]
    
    fonte = forms.ChoiceField(
        choices=FONTE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Origem do Arquivo',
        initial='LOCAL'
    )
    
    arquivo_local = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls,.ods'
        }),
        label='Selecionar Arquivo',
        help_text='Formatos aceitos: Excel (.xlsx, .xls), LibreOffice Calc (.ods)'
    )
    
    arquivo_google_drive_id = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ID do arquivo no Google Drive'
        }),
        label='ID do Arquivo (Google Drive)',
        help_text='Cole o ID do arquivo compartilhado no Google Drive'
    )
    
    abas_selecionadas = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='Abas do Excel para Processar',
        help_text='Selecione as abas que contêm dados de lotação'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        fonte = cleaned_data.get('fonte')
        arquivo_local = cleaned_data.get('arquivo_local')
        arquivo_google_drive_id = cleaned_data.get('arquivo_google_drive_id')
        
        if fonte == 'LOCAL' and not arquivo_local:
            raise ValidationError('Selecione um arquivo do computador.')
        
        if fonte == 'GOOGLE_DRIVE' and not arquivo_google_drive_id:
            raise ValidationError('Informe o ID do arquivo do Google Drive.')
        
        # Validar extensão do arquivo local
        if arquivo_local:
            nome_arquivo = arquivo_local.name.lower()
            extensoes_validas = ['.xlsx', '.xls', '.ods']
            
            if not any(nome_arquivo.endswith(ext) for ext in extensoes_validas):
                raise ValidationError(
                    f'Formato de arquivo inválido. Use: {", ".join(extensoes_validas)}'
                )
        
        return cleaned_data
