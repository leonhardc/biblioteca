#!/bin/bash
# Script de diagnóstico para verificar configuração de contribuições do GitHub
# GitHub Contributions Diagnostic Script

echo "========================================"
echo "Diagnóstico de Contribuições do GitHub"
echo "========================================"
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Verificar email configurado
echo "1. Email configurado no Git:"
GIT_EMAIL=$(git config user.email)
if [ -z "$GIT_EMAIL" ]; then
    echo -e "${RED}❌ Nenhum email configurado!${NC}"
    echo "   Configure com: git config user.email \"seu-email@exemplo.com\""
else
    echo -e "${GREEN}✓${NC} Email: $GIT_EMAIL"
fi
echo ""

# 2. Verificar nome configurado
echo "2. Nome configurado no Git:"
GIT_NAME=$(git config user.name)
if [ -z "$GIT_NAME" ]; then
    echo -e "${RED}❌ Nenhum nome configurado!${NC}"
    echo "   Configure com: git config user.name \"Seu Nome\""
else
    echo -e "${GREEN}✓${NC} Nome: $GIT_NAME"
fi
echo ""

# 3. Verificar emails nos commits recentes
echo "3. Emails usados nos últimos 10 commits:"
COMMIT_EMAILS=$(git log -10 --format="%ae" 2>/dev/null | sort -u)
if [ -z "$COMMIT_EMAILS" ]; then
    echo -e "${YELLOW}⚠${NC} Nenhum commit encontrado"
else
    echo "$COMMIT_EMAILS" | while read email; do
        if [ "$email" = "$GIT_EMAIL" ]; then
            echo -e "  ${GREEN}✓${NC} $email (corresponde ao email configurado)"
        else
            echo -e "  ${YELLOW}⚠${NC} $email (diferente do email configurado atual)"
        fi
    done
fi
echo ""

# 4. Verificar URL do repositório
echo "4. URL do repositório:"
REPO_URL=$(git remote get-url origin 2>/dev/null)
if [ -z "$REPO_URL" ]; then
    echo -e "${RED}❌ Nenhum remote 'origin' configurado${NC}"
else
    echo -e "${GREEN}✓${NC} $REPO_URL"
    
    # Verificar se é um fork (heurística simples)
    if echo "$REPO_URL" | grep -q "github.com"; then
        echo -e "   ${YELLOW}ℹ${NC} Para verificar se é um fork, visite: $REPO_URL"
    fi
fi
echo ""

# 5. Verificar branch atual
echo "5. Branch atual:"
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null)
if [ -z "$CURRENT_BRANCH" ]; then
    echo -e "${RED}❌ Não foi possível determinar o branch atual${NC}"
else
    echo -e "${GREEN}✓${NC} $CURRENT_BRANCH"
    
    # Verificar se é o branch padrão
    DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
    if [ -n "$DEFAULT_BRANCH" ]; then
        if [ "$CURRENT_BRANCH" = "$DEFAULT_BRANCH" ]; then
            echo -e "   ${GREEN}✓${NC} Este é o branch padrão"
        else
            echo -e "   ${YELLOW}⚠${NC} Branch padrão é '$DEFAULT_BRANCH', você está em '$CURRENT_BRANCH'"
            echo "      Contribuições só aparecem no branch padrão ou em PRs mesclados"
        fi
    fi
fi
echo ""

# 6. Resumo e recomendações
echo "========================================"
echo "Resumo e Recomendações:"
echo "========================================"
echo ""

ISSUES_FOUND=0

if [ -z "$GIT_EMAIL" ]; then
    echo -e "${RED}❌ Configure seu email do Git${NC}"
    echo "   git config user.email \"seu-email-verificado@exemplo.com\""
    ISSUES_FOUND=1
fi

if [ -z "$GIT_NAME" ]; then
    echo -e "${RED}❌ Configure seu nome do Git${NC}"
    echo "   git config user.name \"Seu Nome\""
    ISSUES_FOUND=1
fi

if [ -n "$COMMIT_EMAILS" ] && [ -n "$GIT_EMAIL" ]; then
    if ! echo "$COMMIT_EMAILS" | grep -q "^$GIT_EMAIL$"; then
        echo -e "${YELLOW}⚠ Seus commits usam emails diferentes do configurado atualmente${NC}"
        echo "   Certifique-se de que o email está verificado no GitHub:"
        echo "   https://github.com/settings/emails"
        ISSUES_FOUND=1
    fi
fi

if [ $ISSUES_FOUND -eq 0 ]; then
    echo -e "${GREEN}✓ Configuração parece estar correta!${NC}"
    echo ""
    echo "Se suas contribuições ainda não aparecem, verifique:"
    echo "1. O email usado nos commits está verificado no GitHub?"
    echo "   → https://github.com/settings/emails"
    echo ""
    echo "2. Este repositório é um fork?"
    echo "   → Contribuições em forks não aparecem por padrão"
    echo "   → Visite: $REPO_URL e verifique se há um aviso de fork"
    echo ""
    echo "3. O repositório é privado?"
    echo "   → Habilite em: https://github.com/settings/profile"
    echo "   → Marque: 'Show private contributions on my profile'"
    echo ""
    echo "4. Aguarde até 24 horas para o GitHub processar suas contribuições"
fi

echo ""
echo "Para mais informações, consulte o arquivo CONTRIBUTING.md"
echo "========================================"
