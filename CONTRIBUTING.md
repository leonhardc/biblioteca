# Contribuindo para o Projeto Biblioteca Universitária

## 🚀 Diagnóstico Rápido

Execute o script de diagnóstico para verificar automaticamente sua configuração:

```bash
# Tornar o script executável (se necessário)
chmod +x check-contributions.sh

# Executar o script
./check-contributions.sh
```

Este script verificará seu email, configurações do Git e identificará possíveis problemas.

---

## Por que minhas contribuições não aparecem no meu perfil do GitHub?

Se suas contribuições para este projeto não estão aparecendo na sua página inicial do GitHub, existem várias razões possíveis:

### 1. Verifique seu email do Git

O email configurado no Git deve estar **verificado** na sua conta do GitHub. Para verificar:

```bash
# Verifique o email configurado atualmente
git config user.email

# Se necessário, configure o email correto (use o email verificado no GitHub)
git config user.email "seu-email@exemplo.com"

# Para configurar globalmente (todos os repositórios)
git config --global user.email "seu-email@exemplo.com"
```

**Importante:** Vá em [GitHub Settings → Emails](https://github.com/settings/emails) e verifique se o email está listado e verificado.

### 2. Repositório Fork

Se este repositório for um **fork**, as contribuições não aparecerão automaticamente no seu perfil do GitHub. Existem duas soluções:

**Opção A:** Fazer commits no branch principal (main/master) do fork  
**Opção B:** Transformar o fork em um repositório independente (detached fork)

Para a opção B, você precisará entrar em contato com o suporte do GitHub para separar o fork.

### 3. Repositório Privado

Se o repositório for privado, você precisa:

1. Ir em [GitHub Settings → Profile](https://github.com/settings/profile)
2. Marcar a opção "Show private contributions on my profile"
3. Suas contribuições privadas começarão a aparecer

### 4. Commits em branches não-padrão

Contribuições só aparecem se:
- O commit está no branch padrão (main/master), OU
- O commit foi feito em um Pull Request que foi mesclado

### 5. Data do commit

Commits com datas futuras ou muito antigas (mais de 1 ano antes da criação da sua conta) não aparecem no gráfico de contribuições.

## Como garantir que suas contribuições futuras apareçam?

### Passo 1: Configure seu email corretamente

```bash
# Use o email verificado no GitHub
git config user.email "seu-email-verificado@exemplo.com"
git config user.name "Seu Nome"
```

### Passo 2: Verifique a configuração

```bash
# Liste todos os emails associados aos commits
git log --format="%ae" | sort -u
```

Se você ver um email diferente do seu email do GitHub, você precisa reconfigurar.

### Passo 3: Para commits antigos (opcional)

Se você quiser corrigir commits antigos com email errado:

**⚠️ AVISO:** Reescrever o histórico do Git é uma operação avançada e pode causar problemas em projetos colaborativos. Só faça isso se você tiver certeza do que está fazendo.

**Método Recomendado: Usar arquivo `.mailmap`**

A maneira mais segura é usar o arquivo `.mailmap` (já incluído neste projeto), que mapeia emails antigos para o email correto sem reescrever o histórico:

```bash
# O arquivo .mailmap já está configurado neste projeto
# Você pode adicionar suas próprias mapeamentos editando o arquivo:
echo "Seu Nome <email-correto@exemplo.com> <email-antigo@exemplo.com>" >> .mailmap
```

**Método Alternativo: git filter-repo (avançado)**

Se você realmente precisa reescrever o histórico, use `git filter-repo` (mais seguro que `git filter-branch`):

```bash
# Instale git-filter-repo primeiro
# No Linux/Mac: pip install git-filter-repo
# Ou baixe de: https://github.com/newren/git-filter-repo

# Criar arquivo de mapeamento
echo "email-antigo@exemplo.com=email-novo@exemplo.com" > email-map.txt

# Reescrever histórico
git filter-repo --email-callback '
  return email.replace(b"email-antigo@exemplo.com", b"email-novo@exemplo.com")
'

# Depois você precisa forçar o push (CUIDADO!)
# git push --force-with-lease
```

**Nota:** Reescrever histórico requer `git push --force`, que pode causar problemas em projetos colaborativos. **Prefira sempre usar `.mailmap` quando possível.**

## Verificação Rápida

Execute estes comandos para verificar seu setup:

```bash
# 1. Verifique seu email local
echo "Email configurado no Git:"
git config user.email

# 2. Verifique emails nos commits recentes
echo -e "\nEmails usados nos últimos 5 commits:"
git log -5 --format="%ae"

# 3. Verifique a URL do repositório
echo -e "\nURL do repositório:"
git remote get-url origin
```

## Links Úteis

- [Documentação GitHub: Por que minhas contribuições não aparecem?](https://docs.github.com/pt/account-and-profile/setting-up-and-managing-your-github-profile/managing-contribution-graphs-on-your-profile/why-are-my-contributions-not-showing-up-on-my-profile)
- [Configurar email no Git](https://docs.github.com/pt/account-and-profile/setting-up-and-managing-your-github-account/managing-email-preferences/setting-your-commit-email-address)
- [Adicionar email no GitHub](https://docs.github.com/pt/account-and-profile/setting-up-and-managing-your-github-account/managing-email-preferences/adding-an-email-address-to-your-github-account)

## Precisa de ajuda?

Se depois de seguir todos esses passos suas contribuições ainda não aparecem, considere:

1. Aguardar até 24 horas (o GitHub pode levar tempo para processar)
2. Verificar se o repositório não é um fork
3. Entrar em contato com o suporte do GitHub

## Estrutura do Arquivo .mailmap

Este projeto inclui um arquivo `.mailmap` que ajuda a mapear diferentes emails para a identidade correta. Se você contribuir com diferentes emails, adicione uma linha neste formato:

```
Seu Nome Completo <email-principal@exemplo.com> Nome do Commit <email-do-commit@exemplo.com>
```
