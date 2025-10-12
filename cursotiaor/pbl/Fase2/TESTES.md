# 🧪 GUIA COMPLETO DE TESTES - FarmTech Solutions

## 📋 Índice
1. [Testar Cap 1 - ESP32 FarmTech (Wokwi)](#1-testar-cap-1---esp32-farmtech-wokwi)
2. [Testar Cap 7 - Análise Estatística R](#2-testar-cap-7---análise-estatística-r)
3. [Testar Cap 6 - Python Backend](#3-testar-cap-6---python-backend)
4. [Checklist de Validação](#4-checklist-de-validação)

---

## 1️⃣ Testar Cap 1 - ESP32 FarmTech (Wokwi)

### 🌐 Método 1: Wokwi Online (RECOMENDADO)

#### Passo 1: Acessar Wokwi
1. Abra: **https://wokwi.com**
2. Clique em **"+ New Project"**
3. Selecione **"Arduino ESP32"**

#### Passo 2: Importar Código
1. Abra o arquivo `FarmTech.ino` (584 linhas)
2. Selecione tudo (**Ctrl+A**) e copie (**Ctrl+C**)
3. No Wokwi, cole no editor

#### Passo 3: Importar Circuito
1. No Wokwi, clique no botão **"diagram.json"** (ícone azul à esquerda)
2. Abra o arquivo `diagram.json` do projeto
3. Copie todo o conteúdo e cole no editor do Wokwi

#### Passo 4: Iniciar Simulação
1. Clique no botão verde **▶ Start Simulation**
2. Aguarde ~5 segundos (inicialização do DHT22)
3. Observe o **Serial Monitor** no canto inferior direito

---

### 🧪 Testes Funcionais

#### ✅ Teste 1: Sistema Inicializa
**Objetivo:** Verificar se ESP32 inicia corretamente

**Procedimento:**
1. Iniciar simulação
2. Aguardar 5 segundos

**Resultado Esperado:**
```
═══════════════════════════════════════════════════════════════
  🌱 FARMTECH SOLUTIONS - SISTEMA DE IRRIGAÇÃO INTELIGENTE 🌱
═══════════════════════════════════════════════════════════════
  Projeto: Monitoramento de Solo e Irrigação Automatizada
  Grupo: 59 FIAP | Fase 2 | Outubro 2025
═══════════════════════════════════════════════════════════════

[INIT] ✅ Pinos configurados
[INIT] ✅ DHT22 inicializado
[INIT] ✅ Sistema pronto para operação

🌾 Cultura selecionada: BANANA 🍌
```

**Status:** ✅ PASSA | ❌ FALHA

---

#### ✅ Teste 2: Leitura de Sensores
**Objetivo:** Verificar se sensores são lidos corretamente

**Procedimento:**
1. Aguardar 10 segundos (2 leituras completas)
2. Observar Serial Monitor

**Resultado Esperado:**
```
╔═══════════════════════════════════════════════════════════╗
║                    LEITURA #1                             ║
╠═══════════════════════════════════════════════════════════╣
║ 💧 Umidade do Solo:     XX.X%                             ║
║ 🌡️  Temperatura:         XX.X°C                            ║
║ 🧪 pH do Solo:           X.XX → 🟩 NEUTRO                ║
╚═══════════════════════════════════════════════════════════╝
```

**Validações:**
- [ ] Umidade do Solo: 0-100%
- [ ] Temperatura: 0-50°C
- [ ] pH: 3.0-9.0

**Status:** ✅ PASSA | ❌ FALHA

---

#### ✅ Teste 3: NPK Altera pH (NOVO v2.0!)
**Objetivo:** Verificar se botões NPK alteram pH automaticamente

**Procedimento:**
1. **Ajustar LDR** para pH base neutro:
   - Clique no LDR (círculo amarelo)
   - Ajuste slider para ~50% (ADC ≈ 2048)
   - pH Base deve ficar ~6.0

2. **Teste N (Nitrogênio):**
   - Clique no botão verde **N** (GPIO 2)
   - Aguardar próxima leitura (5 segundos)

**Resultado Esperado:**
```
📊 [SENSOR LDR/pH]
   💡 Luminosidade: 3162 lux
   📈 ADC Value: 2048 / 4095
   🧪 pH Base (LDR): 6.00
   ⚗️  Ajuste NPK: -0.40 (N↓)
   🎯 pH Final: 5.60 → 🟩 NEUTRO (IDEAL)
```

**Validações:**
- [ ] pH Base: 6.00 (do LDR)
- [ ] Ajuste NPK: -0.40
- [ ] pH Final: 5.60 (6.00 - 0.40)
- [ ] Display mostra "N↓"

3. **Teste N + P:**
   - Clique também no botão **P** (GPIO 4)
   - Aguardar próxima leitura

**Resultado Esperado:**
```
   ⚗️  Ajuste NPK: -0.70 (N↓ P↓)
   🎯 pH Final: 5.30
```

**Validações:**
- [ ] Ajuste NPK: -0.70 (N=-0.4 + P=-0.3)
- [ ] pH Final: 5.30 (6.00 - 0.70)
- [ ] Display mostra "N↓ P↓"

4. **Teste N + P + K:**
   - Clique também no botão **K** (GPIO 5)
   - Aguardar próxima leitura

**Resultado Esperado:**
```
   ⚗️  Ajuste NPK: -0.60 (N↓ P↓ K↑)
   🎯 pH Final: 5.40
```

**Validações:**
- [ ] Ajuste NPK: -0.60 (N=-0.4 + P=-0.3 + K=+0.1)
- [ ] pH Final: 5.40 (6.00 - 0.60)
- [ ] Display mostra "N↓ P↓ K↑"

5. **Teste Soltar Todos:**
   - Solte todos os botões NPK
   - Aguardar próxima leitura

**Resultado Esperado:**
```
   🧪 pH Base (LDR): 6.00
   🎯 pH Final: 6.00
```
(Sem linha "Ajuste NPK")

**Validações:**
- [ ] pH volta para pH Base (6.00)
- [ ] Sem ajuste NPK

**Status:** ✅ PASSA | ❌ FALHA

---

#### ✅ Teste 4: Irrigação Automática
**Objetivo:** Verificar lógica de decisão de irrigação

**Cenário 4.1: Umidade Crítica (<40%)**

**Procedimento:**
1. Clique no **DHT22** (sensor azul)
2. Ajuste **Humidity** para **35%** (ar)
3. Aguardar próxima leitura

**Resultado Esperado:**
```
║ 💧 Umidade do Solo:     28.0% (35% × 0.8)                 ║
║ 💧 Decisão Irrigação:   🟢 LIGADA                         ║
║    Motivo: Umidade crítica (28.0%) < 40.0%                ║
```

**Validações:**
- [ ] Relé muda para **vermelho** (LIGADO)
- [ ] Display mostra "💧💧💧 IRRIGAÇÃO LIGADA"
- [ ] Motivo correto: "Umidade crítica"

**Cenário 4.2: Solo Encharcado (>80%)**

**Procedimento:**
1. Ajuste **Humidity** do DHT22 para **100%**
2. Aguardar próxima leitura

**Resultado Esperado:**
```
║ 💧 Umidade do Solo:     80.0%                             ║
║ 💧 Decisão Irrigação:   🔴 DESLIGADA                      ║
║    Motivo: Solo encharcado (80.0%) > 80.0%                ║
```

**Validações:**
- [ ] Relé muda para **cinza** (DESLIGADO)
- [ ] Display mostra "⏸️⏸️⏸️ IRRIGAÇÃO DESLIGADA"
- [ ] Motivo correto: "Solo encharcado"

**Cenário 4.3: Banana sem Potássio**

**Procedimento:**
1. Verificar cultura: BANANA
2. Ajuste DHT22: Humidity = 70% (umidade solo = 56%)
3. Botões NPK: **N = SIM**, **P = SIM**, **K = NÃO**
4. Aguardar próxima leitura

**Resultado Esperado:**
```
║ 🌿 NPK (BANANA 🍌):                                       ║
║    • Nitrogênio (N):    ✅ 15 g/m² OK                     ║
║    • Fósforo (P):       ✅ 10 g/m² OK                     ║
║    • Potássio (K):      ❌ 20 g/m² FALTA!                 ║
║                                                            ║
║ 💧 Decisão Irrigação:   🟢 LIGADA                         ║
║    Motivo: Potássio crítico para BANANA + umidade subótima║
```

**Validações:**
- [ ] K marcado como **FALTA**
- [ ] Relé LIGADO (potássio crítico para banana)
- [ ] Motivo menciona "Potássio crítico"

**Status:** ✅ PASSA | ❌ FALHA

---

#### ✅ Teste 5: pH Fora da Faixa
**Objetivo:** Verificar detecção de pH inadequado

**Procedimento:**
1. Ajuste LDR para pH muito ácido:
   - Slider do LDR para **90%** (muito claro)
   - pH deve ficar ~3.5
2. Ajuste DHT22: Humidity = 70% (umidade solo = 56%)
3. Aguardar próxima leitura

**Resultado Esperado:**
```
║ 🧪 pH do Solo:           3.50 → 🟥 ÁCIDO                  ║
║ 💧 Decisão Irrigação:   🟢 LIGADA                         ║
║    Motivo: pH fora da faixa (3.5) + umidade subótima      ║
```

**Validações:**
- [ ] pH < 5.5 (classificado como ÁCIDO)
- [ ] Relé LIGADO
- [ ] Motivo menciona "pH fora da faixa"

**Status:** ✅ PASSA | ❌ FALHA

---

### 📊 Resumo de Testes Cap 1

| Teste | Descrição | Status |
|-------|-----------|--------|
| 1 | Sistema Inicializa | ⬜ |
| 2 | Leitura de Sensores | ⬜ |
| 3 | NPK Altera pH (v2.0) | ⬜ |
| 4 | Irrigação Automática | ⬜ |
| 5 | pH Fora da Faixa | ⬜ |

**Total:** ___ / 5 testes passaram ✅

---

## 2️⃣ Testar Cap 7 - Análise Estatística R

### 🖥️ Pré-requisitos

**Verificar R instalado:**
```powershell
where.exe R
```

**Resultado esperado:**
```
C:\Program Files\R\R-4.5.1\bin\R.exe
```

Se não estiver instalado: https://cran.r-project.org/

---

### 🧪 Método 1: Teste Rápido (Validação)

**Objetivo:** Verificar se dados e cálculos estão corretos

**Comando:**
```powershell
cd "C:\Fiap Projeto\Fase2\cursotiaor\pbl\Fase2\Cap 7"
Rscript teste_rapido.R
```

**Resultado Esperado:**
```
╔═══════════════════════════════════════════════════════════════╗
║       FARMTECH SOLUTIONS - TESTE RÁPIDO CAP 7                ║
╚═══════════════════════════════════════════════════════════════╝

📂 [1/5] Carregando dados...
   ✅ Dados carregados:  35  linhas x  4  colunas

📊 [2/5] Validando estrutura dos dados...
   ✅ Número de linhas OK:  35  >= 30
   ✅ Todas as 4 colunas presentes

🧮 [3/5] Testando cálculos estatísticos...
   ✅ Média > 0
   ✅ Mediana > 0
   ✅ Desvio Padrão > 0
   ✅ CV razoável (0-200%)
   ✅ Quartis em ordem crescente

📋 [4/5] Testando variáveis qualitativas...
   ✅ Variável nominal OK ( 5  categorias)
   ✅ Variável ordinal OK ( 3  categorias)

   🎉 TODOS OS TESTES PASSARAM! Sistema OK.
```

**Validações:**
- [ ] 5/5 testes estatísticos passaram
- [ ] 35 linhas de dados
- [ ] 4 colunas corretas
- [ ] 5 regiões (nominal)
- [ ] 3 portes (ordinal)

**Status:** ✅ PASSA | ❌ FALHA

---

### 🧪 Método 2: Análise Completa

**Objetivo:** Executar análise estatística completa (8 gráficos)

**Comando:**
```powershell
cd "C:\Fiap Projeto\Fase2\cursotiaor\pbl\Fase2\Cap 7"
Rscript analise_RM98765.R
```

**Resultado Esperado:**
```
############################################################
##  ANÁLISE QUANTITATIVA: ÁREA PLANTADA (HECTARES)      ##
############################################################

========== MEDIDAS DE TENDÊNCIA CENTRAL ==========
Média Aritmética: 1769.84 ha
Mediana: 1876.90 ha
Moda: 198.50 ha

========== MEDIDAS DE DISPERSÃO ==========
Variância: 1109238.37 ha²
Desvio Padrão: 1053.20 ha
CV: 59.51%

========== GERANDO GRÁFICOS ==========
✅ Gráficos da variável quantitativa gerados com sucesso!
```

**Validações:**
- [ ] Média: 1769.84 ha
- [ ] Mediana: 1876.90 ha
- [ ] Desvio Padrão: 1053.20 ha
- [ ] CV: 59.51%
- [ ] 8 gráficos gerados

**Status:** ✅ PASSA | ❌ FALHA

---

### 🧪 Método 3: RStudio (Visual)

**Objetivo:** Visualizar gráficos interativamente

**Procedimento:**
1. Abrir **RStudio**
2. Menu: **File → Open File** → `analise_RM98765.R`
3. Clicar em **"Source"** (botão superior direito)
4. Aguardar execução (~30 segundos)
5. Usar **setas ← →** para navegar entre os 8 gráficos

**Gráficos Esperados:**
1. **Histograma** - Área Plantada (ha)
2. **Boxplot** - Área Plantada com outliers
3. **Densidade** - Curva de distribuição
4. **Q-Q Plot** - Normalidade
5. **Barplot** - Regiões (frequência)
6. **Pie Chart** - Regiões (percentual)
7. **Barplot** - Porte (frequência)
8. **Pie Chart** - Porte (percentual)

**Validações:**
- [ ] 8 gráficos gerados
- [ ] Títulos corretos
- [ ] Cores adequadas
- [ ] Legendas legíveis

**Status:** ✅ PASSA | ❌ FALHA

---

### 📊 Resumo de Testes Cap 7

| Teste | Descrição | Status |
|-------|-----------|--------|
| 1 | Teste Rápido (Validação) | ✅ |
| 2 | Análise Completa | ✅ |
| 3 | RStudio Visual | ⬜ |

**Total:** 2 / 3 testes passaram ✅

---

## 3️⃣ Testar Cap 6 - Python Backend

### 🐍 Pré-requisitos

**Verificar Python e ambiente virtual:**
```powershell
cd "C:\Fiap Projeto\Fase2"
.venv\Scripts\python.exe --version
```

**Resultado esperado:**
```
Python 3.11.x
```

---

### 🧪 Método 1: Testes Unitários

**Comando:**
```powershell
cd "C:\Fiap Projeto\Fase2\cursotiaor\pbl\Fase2\Cap 6"
..\..\..\..\.venv\Scripts\python.exe test_farmtech.py
```

**Resultado Esperado:**
```
...........................
----------------------------------------------------------------------
Ran 27 tests in 0.XXXs

OK
```

**Validações:**
- [ ] 27 testes executados
- [ ] 0 falhas
- [ ] 0 erros

**Status:** ✅ PASSA | ❌ FALHA

---

### 🧪 Método 2: Sistema Completo

**Comando:**
```powershell
cd "C:\Fiap Projeto\Fase2\cursotiaor\pbl\Fase2\Cap 6"
..\..\..\..\.venv\Scripts\python.exe main.py
```

**Resultado Esperado:**
```
╔═══════════════════════════════════════════════════════════════╗
║       FARMTECH SOLUTIONS - SISTEMA DE GESTÃO AGRÍCOLA        ║
╚═══════════════════════════════════════════════════════════════╝

1. Gerenciar Cultivos
2. Monitorar Sensores
3. Controlar Irrigação
4. Gerenciar Estoque
5. Configurações
0. Sair

Escolha uma opção: _
```

**Validações:**
- [ ] Menu exibido corretamente
- [ ] Opções 1-5 e 0 presentes
- [ ] Sistema aguarda input

**Status:** ✅ PASSA | ❌ FALHA

---

## 4️⃣ Checklist de Validação Completa

### ✅ Cap 1 - ESP32 FarmTech

- [ ] Sistema inicializa sem erros
- [ ] Sensores leem valores corretos
- [ ] **NPK altera pH automaticamente (v2.0)**
  - [ ] N → pH -0.4
  - [ ] P → pH -0.3
  - [ ] K → pH +0.1
  - [ ] N+P+K → pH -0.6
- [ ] Irrigação automática funciona (6 condições)
- [ ] Relé liga/desliga corretamente
- [ ] Display formatado e legível

**Status:** ___/6 itens ✅

---

### ✅ Cap 6 - Python Backend

- [ ] 27 testes unitários passam
- [ ] Sistema CRUD funciona (Create, Read, Update, Delete)
- [ ] Persistência JSON funciona
- [ ] Oracle opcional configurado (se desejado)
- [ ] Menu interativo funciona
- [ ] Validações de dados corretas

**Status:** ___/6 itens ✅

---

### ✅ Cap 7 - Análise Estatística R

- [ ] Dados carregam corretamente (35 linhas × 4 colunas)
- [ ] Cálculos estatísticos corretos
  - [ ] Média: 1769.84 ha
  - [ ] Mediana: 1876.90 ha
  - [ ] Desvio Padrão: 1053.20 ha
  - [ ] CV: 59.51%
- [ ] 4 tipos de variáveis presentes
  - [ ] Quantitativa discreta (num_propriedades)
  - [ ] Quantitativa contínua (area_plantada_ha)
  - [ ] Qualitativa nominal (regiao)
  - [ ] Qualitativa ordinal (porte_propriedade)
- [ ] 8 gráficos gerados
- [ ] Relatório final completo

**Status:** ___/5 itens ✅

---

## 🎯 Resumo Geral

| Capítulo | Testes | Status |
|----------|--------|--------|
| **Cap 1 - ESP32** | 5 cenários | ⬜ |
| **Cap 6 - Python** | 27 testes unitários | ✅ |
| **Cap 7 - R** | 3 métodos | ✅ |

**TOTAL:** ___/3 capítulos validados ✅

---

## 📅 Antes da Entrega (15/10/2025)

### Testes Obrigatórios

- [ ] **Cap 1**: Executar todos os 5 cenários no Wokwi
- [ ] **Cap 1**: Testar especialmente NPK-pH (v2.0)
- [ ] **Cap 6**: Rodar `test_farmtech.py` (27 testes)
- [ ] **Cap 7**: Executar `teste_rapido.R`
- [ ] **Cap 7**: Gerar 8 gráficos via RStudio

### Documentação

- [ ] Screenshots do Wokwi (2 imagens)
- [ ] Vídeo YouTube (5 minutos)
- [ ] README.md atualizado
- [ ] RELACAO_NPK_PH.md revisado

---

## 🆘 Troubleshooting

### Problema: R não encontrado
**Solução:**
```powershell
# Verificar instalação
where.exe R

# Se não estiver instalado:
# Baixar de: https://cran.r-project.org/
```

### Problema: Python não encontrado
**Solução:**
```powershell
# Verificar ambiente virtual
cd "C:\Fiap Projeto\Fase2"
.venv\Scripts\python.exe --version

# Reativar se necessário:
.venv\Scripts\Activate.ps1
```

### Problema: Wokwi não simula
**Solução:**
- Verificar se `diagram.json` foi importado corretamente
- Limpar cache do navegador (Ctrl+Shift+Del)
- Tentar outro navegador (Chrome recomendado)

---

**FarmTech Solutions**  
*"Testado, validado, pronto para entregar!"* ✅🧪  
**Data:** 12/10/2025
