# acoes_pngi/migrations/0002_load_config_data.py
from django.db import migrations


def load_situacao_acao(apps, schema_editor):
    SituacaoAcao = apps.get_model("acoes_pngi", "SituacaoAcao")
    data = [
        {"idsituacaoacao": 1, "strdescricaosituacao": "Não Iniciada"},
        {"idsituacaoacao": 2, "strdescricaosituacao": "Em Andamento"},
        {"idsituacaoacao": 3, "strdescricaosituacao": "Concluída"},
        {"idsituacaoacao": 4, "strdescricaosituacao": "Cancelada"},
    ]
    for item in data:
        SituacaoAcao.objects.create(**item)


def load_tipo_entrave_alerta(apps, schema_editor):
    TipoEntraveAlerta = apps.get_model("acoes_pngi", "TipoEntraveAlerta")
    data = [
        {"idtipoentravealerta": 1, "strdescricaotipoentravealerta": "Entrave"},
        {"idtipoentravealerta": 2, "strdescricaotipoentravealerta": "Alerta"},
    ]
    for item in data:
        TipoEntraveAlerta.objects.create(**item)


def load_eixos(apps, schema_editor):
    Eixo = apps.get_model("acoes_pngi", "Eixo")
    data = [
        {"ideixo": 1, "strdescricaoeixo": "Eixo 1", "stralias": "E1"},
        {"ideixo": 2, "strdescricaoeixo": "Eixo 2", "stralias": "E2"},
        {"ideixo": 3, "strdescricaoeixo": "Eixo 3", "stralias": "E3"},
    ]
    for item in data:
        Eixo.objects.create(**item)


def load_vigencia_pngi(apps, schema_editor):
    VigenciaPNGI = apps.get_model("acoes_pngi", "VigenciaPNGI")
    from datetime import date

    data = [
        {
            "idvigenciapngi": 1,
            "strdescricaovigenciapngi": "2024-2027",
            "datiniciovigencia": date(2024, 1, 1),
            "datfinalvigencia": date(2027, 12, 31),
            "isvigenciaativa": True,
        },
    ]
    for item in data:
        VigenciaPNGI.objects.create(**item)


def load_tipo_anotacao_alinhamento(apps, schema_editor):
    TipoAnotacaoAlinhamento = apps.get_model("acoes_pngi", "TipoAnotacaoAlinhamento")
    data = [
        {
            "idtipoanotacaoalinhamento": 1,
            "strdescricaotipoanotacaoalinhamento": "Reunião",
        },
        {
            "idtipoanotacaoalinhamento": 2,
            "strdescricaotipoanotacaoalinhamento": "E-mail",
        },
        {
            "idtipoanotacaoalinhamento": 3,
            "strdescricaotipoanotacaoalinhamento": "Ofício",
        },
    ]
    for item in data:
        TipoAnotacaoAlinhamento.objects.create(**item)


class Migration(migrations.Migration):
    dependencies = [
        ("acoes_pngi", "0001_initial"),
        ("accounts", "0002_load_domain_data"),
    ]

    operations = [
        migrations.RunPython(
            load_situacao_acao, reverse_code=migrations.RunPython.noop
        ),
        migrations.RunPython(
            load_tipo_entrave_alerta, reverse_code=migrations.RunPython.noop
        ),
        migrations.RunPython(load_eixos, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(
            load_vigencia_pngi, reverse_code=migrations.RunPython.noop
        ),
        migrations.RunPython(
            load_tipo_anotacao_alinhamento, reverse_code=migrations.RunPython.noop
        ),
    ]
