# ✅ Checklist Rápido - Sincronização Git
 
## 🚀 Antes de Começar a Trabalhar
- [ ] `git pull origin main`
- [ ] `git status` (verificar se está limpo)
- [ ] Verificar se está na branch correta: `git branch`
 
## 💻 Durante o Trabalho
- [ ] Fazer commits pequenos e frequentes
- [ ] Testar código antes de commit
- [ ] Usar mensagens descritivas: `feat:`, `fix:`, `docs:`, etc.
 
## 📤 Antes de Sair/Trocar de Máquina
- [ ] `git status` (ver mudanças)
- [ ] `git add .` (adicionar mudanças)
- [ ] `git commit -m "mensagem clara"`
- [ ] `git push origin main`
- [ ] Verificar se push foi bem-sucedido
 
## 🔄 Ao Trocar de Ambiente
- [ ] 'git checkout phellype-dev'
- [ ] `git pull origin main`
- [ ] `git pull origin phellype-dev`
- [ ] `git pull origin carlos-dev`
- [ ] `git pull origin cesar-dev`
- [ ] `git status` (confirmar sincronização)
- [ ] Testar se aplicação funciona
- [ ] Continuar desenvolvimento
 
## ⚠️ Em Caso de Conflitos
- [ ] `git status` (ver arquivos conflituosos)
- [ ] Editar arquivos manualmente (remover `<<<`, `===`, `>>>`)
- [ ] `git add arquivo-resolvido.py`
- [ ] `git commit -m "merge: resolve conflitos"`
- [ ] `git push origin main`
 
## 🆘 Verificações de Emergência
- [ ] Commits não enviados: `git log origin/main..HEAD`
- [ ] Commits não baixados: `git log HEAD..origin/main`
- [ ] Diferenças: `git diff HEAD origin/main --name-only`
- [ ] Status geral: `git status`
 
---
 
## 🔥 Comandos Mais Usados
 
```bash
# Trio básico diário
git pull origin main
git add . && git commit -m "sua mensagem"
git push origin main
 
# Verificação rápida
git status
git log --oneline -5
 
# Em caso de problemas
git stash
git pull origin main
git stash pop
```
 
## 🎯 Metas de Boas Práticas
- ✅ Nunca trabalhar sem fazer pull primeiro
- ✅ Sempre fazer push antes de trocar de máquina
- ✅ Commits com mensagens claras e descritivas
- ✅ Resolver conflitos imediatamente
- ✅ Manter .gitignore atualizado


# 🌳 Workflow Git - Time FarmTech Solutions
**Equipe:** Phellype, Carlos, Cesar

---

## 📋 Estrutura de Branches

```
main (branch principal - código estável)
├── phellype-dev (desenvolvimento Phellype)
├── carlos-dev (desenvolvimento Carlos)
└── cesar-dev (desenvolvimento Cesar)
```

---

## 🚀 Setup Inicial (Fazer UMA VEZ)

### **1. Phellype (Criador do Repositório)**
```bash
# Já está na main, só precisa criar sua branch
git checkout -b phellype-dev
git push -u origin phellype-dev
git checkout main
```

> Nota: As branches `phellype-dev`, `carlos-dev` e `cesar-dev` já foram criadas no remoto e estão disponíveis em `origin`.

### **2. Carlos (Primeira Vez)**
```bash
# Clonar repositório
git clone https://github.com/Phemassa/FarmTechSolutions.git
cd FarmTechSolutions

# Criar sua branch
git checkout -b carlos-dev
git push -u origin carlos-dev
```

### **3. Cesar (Primeira Vez)**
```bash
# Clonar repositório
git clone https://github.com/Phemassa/FarmTechSolutions.git
cd FarmTechSolutions

# Criar sua branch
git checkout -b cesar-dev
git push -u origin cesar-dev
```

---

## 💻 Fluxo Diário Individual

### **Ao Começar a Trabalhar**
```bash
# 1. Ir para sua branch
git checkout seu-nome-dev

# 2. Atualizar com a main
git pull origin main

# 3. Se houver conflitos, resolver e continuar
git status
```

### **Durante o Trabalho**
```bash
# Commits frequentes na SUA branch
git add .
git commit -m "feat: implementa sensor de temperatura"
git push origin seu-nome-dev
```

### **Antes de Sair**
```bash
# Garantir que tudo está salvo no GitHub
git status
git add .
git commit -m "wip: trabalho em progresso"
git push origin seu-nome-dev
```

---

## 🔄 Integrando Trabalho na Main

### **Quando Sua Feature Está Pronta**
```bash
# 1. Certifique-se que sua branch está atualizada
git checkout seu-nome-dev
git pull origin main

# 2. Resolver conflitos se houver
git status

# 3. Ir para a main
git checkout main
git pull origin main

# 4. Fazer merge da sua branch
git merge seu-nome-dev

# 5. Testar se tudo funciona
# (rodar servidor, testes, etc)

# 6. Enviar para o GitHub
git push origin main

# 7. Voltar para sua branch de desenvolvimento
git checkout seu-nome-dev
```

---

## 🤝 Colaboração Entre Branches

### **Ver o que os colegas estão fazendo**
```bash
# Listar todas as branches
git branch -a

# Ver commits de um colega
git log origin/carlos-dev --oneline -5

# Baixar branch de um colega para testar
git checkout -b teste-carlos origin/carlos-dev
```

### **Integrar trabalho de um colega**
```bash
# Se você precisa do código que Carlos fez
git checkout sua-branch
git merge origin/carlos-dev

# Resolver conflitos se houver
# Continuar trabalhando
```

---

## ⚠️ Resolvendo Conflitos

### **Quando Acontecem**
- Dois desenvolvedores editam o mesmo arquivo
- Merge gera marcadores `<<<`, `===`, `>>>`

### **Como Resolver**
```bash
# 1. Ver arquivos conflituosos
git status

# 2. Abrir arquivo no VS Code
# Vai aparecer opções: "Accept Current" / "Accept Incoming" / "Accept Both"

# 3. Depois de resolver
git add arquivo-resolvido.py
git commit -m "merge: resolve conflito com branch X"
git push origin sua-branch
```

---

## 🎯 Boas Práticas do Time

### ✅ **SEMPRE Fazer**
- [ ] Pull da main antes de começar a trabalhar
- [ ] Trabalhar na SUA branch (não na main diretamente)
- [ ] Commits descritivos: `feat:`, `fix:`, `docs:`
- [ ] Push frequente na sua branch
- [ ] Avisar no grupo quando fizer merge na main
- [ ] Testar antes de fazer merge na main

### ❌ **NUNCA Fazer**
- Trabalhar diretamente na main
- Fazer force push (`git push -f`)
- Commitar arquivos temporários (__pycache__, .venv)
- Deixar conflitos sem resolver
- Fazer merge sem testar

---

## 📊 Comandos Úteis para o Time

### **Status Geral do Projeto**
```bash
# Ver todas as branches
git branch -a

# Ver quem fez os últimos commits
git log --oneline --all --graph -10

# Ver diferenças entre sua branch e a main
git diff main..sua-branch --name-only
```

### **Sincronização Rápida**
```bash
# Atualizar todas as branches
git fetch --all

# Ver o que mudou na main
git log HEAD..origin/main

# Atualizar sua branch com a main
git checkout sua-branch
git merge origin/main
```

---

## 🆘 Emergências Comuns

### **"Meu código sumiu!"**
```bash
# Ver todos os commits (até deletados)
git reflog

# Recuperar commit específico
git checkout <hash-do-commit>
git checkout -b recuperacao
```

### **"Commitei na main sem querer!"**
```bash
# Desfazer último commit (mantém alterações)
git reset --soft HEAD~1

# Ir para sua branch
git checkout sua-branch

# Commitar novamente
git add .
git commit -m "mensagem"
```

### **"Tem conflito e não sei resolver!"**
```bash
# Cancelar merge
git merge --abort

# OU guardar mudanças temporariamente
git stash
git pull origin main
git stash pop
```

---

## 📱 Comunicação do Time

### **Antes de Merge na Main, Avisar:**
```
💬 Grupo WhatsApp/Discord:
"Vou fazer merge da minha branch na main agora!
Feature: Sistema NPK completo
Aguardem 2 min antes de fazer pull"
```

### **Após Merge:**
```
💬 "Merge concluído! ✅
Todos podem fazer git pull origin main agora
Testei e está funcionando"
```

---

## 🔥 Comandos Rápidos por Pessoa

### **Phellype**
```bash
git checkout phellype-dev
git pull origin main
# trabalha...
git add . && git commit -m "feat: nova funcionalidade"
git push origin phellype-dev
```

### **Carlos**
```bash
git checkout carlos-dev
git pull origin main
# trabalha...
git add . && git commit -m "fix: corrige bug X"
git push origin carlos-dev
```

### **Cesar**
```bash
git checkout cesar-dev
git pull origin main
# trabalha...
git add . && git commit -m "docs: atualiza documentação"
git push origin cesar-dev
```

---

## 📚 Glossário

- **branch**: Linha paralela de desenvolvimento
- **main**: Branch principal (código de produção)
- **merge**: Juntar código de duas branches
- **pull**: Baixar código do GitHub
- **push**: Enviar código para o GitHub
- **conflict**: Quando duas pessoas editam a mesma linha
- **commit**: Salvar mudanças localmente
- **checkout**: Mudar de branch

---

## 🎓 Fluxo Completo - Exemplo Real

**Phellype vai implementar sensor de pH:**

```bash
# Dia 1 - Manhã
git checkout phellype-dev
git pull origin main
# cria arquivo sensor_ph.py
git add sensor_ph.py
git commit -m "feat: adiciona classe SensorPH"
git push origin phellype-dev

# Dia 1 - Tarde
# continua trabalhando
git add .
git commit -m "feat: integra sensor pH com dashboard"
git push origin phellype-dev

# Dia 2 - Feature pronta
git checkout phellype-dev
git pull origin main  # Atualiza com trabalho dos colegas
git checkout main
git merge phellype-dev
# Testa tudo
git push origin main

# Avisa no grupo: "Sensor pH integrado! ✅"
```

---

**Dúvidas? Consulte este guia ou pergunte no grupo!** 🚀
