"""
Forms do módulo Carga Org/Lot
"""

from django import forms
from django.core.exceptions import ValidationError
from .models import TblPatriarca, TblStatusProgresso


class PatriarcaForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Patriarca
    """
    
    class Meta:
        model = TblPatriarca
        fields = ['str_sigla_patriarca', 'str_nome', 'id_status_progresso']
        labels = {
            'str_sigla_patriarca': 'Sigla do Patriarca',
            'str_nome': 'Nome Completo',
            'id_status_progresso': 'Status',
        }
        widgets = {
            'str_sigla_patriarca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: SEGER, SEDU, SEJUS',
                'maxlength': '20',
                'style': 'text-transform: uppercase;'
            }),
            'str_nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Secretaria de Estado de Gestão e Recursos Humanos',
                'maxlength': '255'
            }),
            'id_status_progresso': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        help_texts = {
            'str_sigla_patriarca': 'Sigla única que identifica o órgão patriarca (máx. 20 caracteres)',
            'str_nome': 'Nome completo do órgão ou entidade',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar apenas status relevantes para criação/edição
        # 1 = Novo, 2 = Em Progresso
        self.fields['id_status_progresso'].queryset = TblStatusProgresso.objects.filter(
            id_status_progresso__in=[1, 2]
        )
        
        # Definir valor padrão para novos registros
        if not self.instance.pk:
            try:
                self.fields['id_status_progresso'].initial = TblStatusProgresso.objects.get(
                    id_status_progresso=1  # Status "Novo"
                )
            except TblStatusProgresso.DoesNotExist:
                pass
    
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
