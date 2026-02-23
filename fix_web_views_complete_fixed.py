# fix_web_views_complete_fixed.py
# Corrige erros em test_web_views_complete_fixed.py

filepath = r"C:\Projects\gpp_plataform\acoes_pngi\tests\test_web_views_complete_fixed.py"

print("Lendo arquivo...")
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print("Aplicando correções...")

# 1. Adicionar import de Client
old_import = "from django.test import TestCase"
new_import = "from django.test import TestCase, Client"
content = content.replace(old_import, new_import)
print("  ✅ Adicionado import Client")

# 2. Remover parênteses extras nas linhas 216, 323
content = content.replace(
    "self.client.login(email='coord@test.com', password='test123')        )",
    "self.client.login(email='coord@test.com', password='test123')"
)
print("  ✅ Removido parênteses extra linha 216")

# Linha 323 - limpar espaços extras
content = content.replace(
    "self.client.login(email='coord@test.com', password='test123')    ",
    "self.client.login(email='coord@test.com', password='test123')"
)
print("  ✅ Limpado espaços extras linha 323")

# 3. Adicionar dados de teste faltantes
if "# Criar eixo para testes    " in content:
    content = content.replace(
        "# Criar eixo para testes    ",
        """# Criar eixo para testes
        self.eixo = Eixo.objects.create(
            strdescricaoeixo='Eixo Teste',
            stralias='TESTE'
        )
    """
    )
    print("  ✅ Adicionado setup de eixo")

print("\nSalvando arquivo...")
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ ARQUIVO CORRIGIDO COM SUCESSO!")
