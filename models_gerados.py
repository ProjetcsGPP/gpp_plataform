# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountsAttribute(models.Model):
    id = models.BigAutoField(primary_key=True)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=255)
    aplicacao = models.ForeignKey('Tblaplicacao', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Tblusuario', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_attribute'
        unique_together = (('user', 'aplicacao', 'key'),)


class AccountsRole(models.Model):
    id = models.BigAutoField(primary_key=True)
    nomeperfil = models.CharField(max_length=100)
    codigoperfil = models.CharField(max_length=100)
    aplicacao = models.ForeignKey('Tblaplicacao', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_role'
        unique_together = (('aplicacao', 'codigoperfil'),)


class AccountsUserrole(models.Model):
    id = models.BigAutoField(primary_key=True)
    aplicacao = models.ForeignKey('Tblaplicacao', models.DO_NOTHING)
    role = models.ForeignKey(AccountsRole, models.DO_NOTHING)
    user = models.ForeignKey('Tblusuario', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_userrole'
        unique_together = (('user', 'aplicacao', 'role'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField('Tblusuario', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class DbServiceAppclient(models.Model):
    id = models.BigAutoField(primary_key=True)
    client_id = models.CharField(unique=True, max_length=100)
    client_secret_hash = models.CharField(max_length=255)
    is_active = models.BooleanField()
    aplicacao = models.OneToOneField('Tblaplicacao', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'db_service_appclient'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Tblusuario', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Tblaplicacao(models.Model):
    idaplicacao = models.BigAutoField(primary_key=True)
    codigointerno = models.CharField(unique=True, max_length=50)
    nomeaplicacao = models.CharField(max_length=200)
    base_url = models.CharField(max_length=500, blank=True, null=True)
    isshowinportal = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblaplicacao'


class Tblcargapatriarca(models.Model):
    idcargapatriarca = models.BigAutoField(primary_key=True)
    idpatriarca = models.ForeignKey('Tblpatriarca', models.DO_NOTHING, db_column='idpatriarca')
    idtokenenviocarga = models.ForeignKey('Tbltokenenviocarga', models.DO_NOTHING, db_column='idtokenenviocarga')
    idstatuscarga = models.ForeignKey('Tblstatuscarga', models.DO_NOTHING, db_column='idstatuscarga')
    idtipocarga = models.ForeignKey('Tbltipocarga', models.DO_NOTHING, db_column='idtipocarga')
    strmensagemretorno = models.TextField(blank=True, null=True)
    datdatahorainicio = models.DateTimeField()
    datdatahorafim = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblcargapatriarca'
        unique_together = (('idpatriarca', 'idtokenenviocarga', 'idtipocarga'),)


class Tblclassificacaousuario(models.Model):
    idclassificacaousuario = models.SmallIntegerField(primary_key=True)
    strdescricao = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tblclassificacaousuario'


class Tbldetalhestatuscarga(models.Model):
    iddetalhestatuscarga = models.BigAutoField(primary_key=True)
    idcargapatriarca = models.ForeignKey(Tblcargapatriarca, models.DO_NOTHING, db_column='idcargapatriarca')
    idstatuscarga = models.ForeignKey('Tblstatuscarga', models.DO_NOTHING, db_column='idstatuscarga')
    datregistro = models.DateTimeField()
    strmensagem = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbldetalhestatuscarga'


class Tbleixos(models.Model):
    ideixo = models.AutoField(primary_key=True)
    strdescricaoeixo = models.CharField(max_length=100)
    stralias = models.CharField(unique=True, max_length=5)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbleixos'
        db_table_comment = 'Eixos estratégicos do PNGI'


class Tbllotacao(models.Model):
    idlotacao = models.BigAutoField(primary_key=True)
    idlotacaoversao = models.ForeignKey('Tbllotacaoversao', models.DO_NOTHING, db_column='idlotacaoversao')
    idorganogramaversao = models.ForeignKey('Tblorganogramaversao', models.DO_NOTHING, db_column='idorganogramaversao')
    idpatriarca = models.ForeignKey('Tblpatriarca', models.DO_NOTHING, db_column='idpatriarca')
    idorgaolotacao = models.ForeignKey('Tblorgaounidade', models.DO_NOTHING, db_column='idorgaolotacao')
    idunidadelotacao = models.ForeignKey('Tblorgaounidade', models.DO_NOTHING, db_column='idunidadelotacao', related_name='tbllotacao_idunidadelotacao_set', blank=True, null=True)
    strcpf = models.CharField(max_length=14)
    strcargooriginal = models.CharField(max_length=255, blank=True, null=True)
    strcargonormalizado = models.CharField(max_length=255, blank=True, null=True)
    flgvalido = models.BooleanField()
    strerrosvalidacao = models.TextField(blank=True, null=True)
    datreferencia = models.DateField(blank=True, null=True)
    datcriacao = models.DateTimeField()
    idusuariocriacao = models.BigIntegerField(blank=True, null=True)
    datalteracao = models.DateTimeField(blank=True, null=True)
    idusuarioalteracao = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbllotacao'


class Tbllotacaoinconsistencia(models.Model):
    idinconsistencia = models.BigAutoField(primary_key=True)
    idlotacao = models.ForeignKey(Tbllotacao, models.DO_NOTHING, db_column='idlotacao')
    strtipo = models.CharField(max_length=100)
    strdetalhe = models.TextField()
    datregistro = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbllotacaoinconsistencia'


class Tbllotacaojsonorgao(models.Model):
    idlotacaojsonorgao = models.BigAutoField(primary_key=True)
    idlotacaoversao = models.ForeignKey('Tbllotacaoversao', models.DO_NOTHING, db_column='idlotacaoversao')
    idorganogramaversao = models.ForeignKey('Tblorganogramaversao', models.DO_NOTHING, db_column='idorganogramaversao')
    idpatriarca = models.ForeignKey('Tblpatriarca', models.DO_NOTHING, db_column='idpatriarca')
    idorgaolotacao = models.ForeignKey('Tblorgaounidade', models.DO_NOTHING, db_column='idorgaolotacao')
    jsconteudo = models.JSONField()
    datcriacao = models.DateTimeField()
    datenvioapi = models.DateTimeField(blank=True, null=True)
    strstatusenvio = models.CharField(max_length=30, blank=True, null=True)
    strmensagemretorno = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbllotacaojsonorgao'
        unique_together = (('idlotacaoversao', 'idorgaolotacao'),)


class Tbllotacaoversao(models.Model):
    idlotacaoversao = models.BigAutoField(primary_key=True)
    idpatriarca = models.ForeignKey('Tblpatriarca', models.DO_NOTHING, db_column='idpatriarca')
    idorganogramaversao = models.ForeignKey('Tblorganogramaversao', models.DO_NOTHING, db_column='idorganogramaversao')
    strorigem = models.CharField(max_length=50)
    strtipoarquivooriginal = models.CharField(max_length=20, blank=True, null=True)
    strnomearquivooriginal = models.CharField(max_length=255, blank=True, null=True)
    datprocessamento = models.DateTimeField()
    strstatusprocessamento = models.CharField(max_length=30)
    strmensagemprocessamento = models.TextField(blank=True, null=True)
    flgativo = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'tbllotacaoversao'


class Tblorganogramajson(models.Model):
    idorganogramajson = models.BigAutoField(primary_key=True)
    idorganogramaversao = models.OneToOneField('Tblorganogramaversao', models.DO_NOTHING, db_column='idorganogramaversao')
    jsconteudo = models.JSONField()
    datcriacao = models.DateTimeField()
    datenvioapi = models.DateTimeField(blank=True, null=True)
    strstatusenvio = models.CharField(max_length=30, blank=True, null=True)
    strmensagemretorno = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblorganogramajson'


class Tblorganogramaversao(models.Model):
    idorganogramaversao = models.BigAutoField(primary_key=True)
    idpatriarca = models.ForeignKey('Tblpatriarca', models.DO_NOTHING, db_column='idpatriarca')
    strorigem = models.CharField(max_length=50)
    strtipoarquivooriginal = models.CharField(max_length=20, blank=True, null=True)
    strnomearquivooriginal = models.CharField(max_length=255, blank=True, null=True)
    datprocessamento = models.DateTimeField()
    strstatusprocessamento = models.CharField(max_length=30)
    strmensagemprocessamento = models.TextField(blank=True, null=True)
    flgativo = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'tblorganogramaversao'


class Tblorgaounidade(models.Model):
    idorgaounidade = models.BigAutoField(primary_key=True)
    idorganogramaversao = models.ForeignKey(Tblorganogramaversao, models.DO_NOTHING, db_column='idorganogramaversao')
    idpatriarca = models.ForeignKey('Tblpatriarca', models.DO_NOTHING, db_column='idpatriarca')
    strnome = models.CharField(max_length=255)
    strsigla = models.CharField(max_length=50)
    idorgaounidadepai = models.ForeignKey('self', models.DO_NOTHING, db_column='idorgaounidadepai', blank=True, null=True)
    strnumerohierarquia = models.CharField(max_length=50, blank=True, null=True)
    intnivelhierarquia = models.IntegerField(blank=True, null=True)
    flgativo = models.BooleanField()
    datcriacao = models.DateTimeField()
    idusuariocriacao = models.BigIntegerField(blank=True, null=True)
    datalteracao = models.DateTimeField(blank=True, null=True)
    idusuarioalteracao = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblorgaounidade'
        unique_together = (('idorganogramaversao', 'strsigla'),)


class Tblpatriarca(models.Model):
    idpatriarca = models.BigAutoField(primary_key=True)
    idexternopatriarca = models.UUIDField(unique=True)
    strsiglapatriarca = models.CharField(unique=True, max_length=20)
    strnome = models.CharField(max_length=255)
    idstatusprogresso = models.ForeignKey('Tblstatusprogresso', models.DO_NOTHING, db_column='idstatusprogresso')
    datcriacao = models.DateTimeField()
    idusuariocriacao = models.BigIntegerField()
    datalteracao = models.DateTimeField(blank=True, null=True)
    idusuarioalteracao = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblpatriarca'


class Tblsituacaoacao(models.Model):
    idsituacaoacao = models.AutoField(primary_key=True)
    strdescricaosituacao = models.CharField(unique=True, max_length=15)

    class Meta:
        managed = False
        db_table = 'tblsituacaoacao'
        db_table_comment = 'Situações possíveis de uma ação PNGI'


class Tblstatuscarga(models.Model):
    idstatuscarga = models.SmallIntegerField(primary_key=True)
    strdescricao = models.CharField(max_length=150)
    flgsucesso = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tblstatuscarga'


class Tblstatusprogresso(models.Model):
    idstatusprogresso = models.SmallIntegerField(primary_key=True)
    strdescricao = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tblstatusprogresso'


class Tblstatustokenenviocarga(models.Model):
    idstatustokenenviocarga = models.SmallIntegerField(primary_key=True)
    strdescricao = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tblstatustokenenviocarga'


class Tblstatususuario(models.Model):
    idstatususuario = models.SmallIntegerField(primary_key=True)
    strdescricao = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tblstatususuario'


class Tbltipocarga(models.Model):
    idtipocarga = models.SmallIntegerField(primary_key=True)
    strdescricao = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tbltipocarga'


class Tbltipousuario(models.Model):
    idtipousuario = models.SmallIntegerField(primary_key=True)
    strdescricao = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tbltipousuario'


class Tbltokenenviocarga(models.Model):
    idtokenenviocarga = models.BigAutoField(primary_key=True)
    idpatriarca = models.ForeignKey(Tblpatriarca, models.DO_NOTHING, db_column='idpatriarca')
    idstatustokenenviocarga = models.ForeignKey(Tblstatustokenenviocarga, models.DO_NOTHING, db_column='idstatustokenenviocarga')
    strtokenretorno = models.CharField(max_length=1000)
    datdatahorainicio = models.DateTimeField()
    datdatahorafim = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbltokenenviocarga'


class Tblusuario(models.Model):
    idusuario = models.BigAutoField(primary_key=True)
    strnome = models.CharField(max_length=200)
    stremail = models.CharField(unique=True, max_length=200)
    strsenha = models.CharField(max_length=200)
    idstatususuario = models.ForeignKey(Tblstatususuario, models.DO_NOTHING, db_column='idstatususuario')
    idtipousuario = models.ForeignKey(Tbltipousuario, models.DO_NOTHING, db_column='idtipousuario')
    idclassificacaousuario = models.ForeignKey(Tblclassificacaousuario, models.DO_NOTHING, db_column='idclassificacaousuario')
    datacriacao = models.DateTimeField()
    idusuariocriacao = models.ForeignKey('self', models.DO_NOTHING, db_column='idusuariocriacao', blank=True, null=True)
    data_alteracao = models.DateTimeField(blank=True, null=True)
    idusuarioalteracao = models.ForeignKey('self', models.DO_NOTHING, db_column='idusuarioalteracao', related_name='tblusuario_idusuarioalteracao_set', blank=True, null=True)
    is_active = models.BooleanField()
    is_staff = models.BooleanField()
    is_superuser = models.BooleanField()
    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblusuario'


class TblusuarioGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(Tblusuario, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tblusuario_groups'
        unique_together = (('user', 'group'),)


class TblusuarioUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(Tblusuario, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tblusuario_user_permissions'
        unique_together = (('user', 'permission'),)


class Tblvigenciapngi(models.Model):
    idvigenciapngi = models.AutoField(primary_key=True)
    strdescricaovigenciapngi = models.CharField(max_length=100)
    datiniciovigencia = models.DateField()
    datfinalvigencia = models.DateField()
    isvigenciaativa = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblvigenciapngi'
        db_table_comment = 'Períodos de vigência do PNGI'
