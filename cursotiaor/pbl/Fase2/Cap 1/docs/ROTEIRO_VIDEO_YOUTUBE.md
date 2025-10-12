# 🎥 Roteiro para Vídeo - Sistema de Irrigação Inteligente FarmTech

## 📋 Informações do Vídeo

- **Duração:** Máximo 5 minutos
- **Plataforma:** YouTube (não listado)
- **Objetivo:** Demonstrar funcionamento completo do sistema
- **Público:** Avaliadores FIAP

---

## 🎬 Estrutura do Vídeo (5 minutos)

### **0:00-0:30 - Introdução (30 segundos)**
- Nome do projeto: "FarmTech Solutions - Sistema de Irrigação Inteligente"
- Grupo 59 FIAP - Fase 2
- Objetivo: Otimizar irrigação agrícola usando IoT

### **0:30-1:30 - Visão Geral do Circuito (1 minuto)**
- Mostrar circuito completo no Wokwi
- Identificar componentes principais
- Explicar conexões

### **1:30-3:00 - Demonstração dos Sensores (1 minuto e 30 segundos)**
- Botões NPK
- LDR (pH)
- DHT22 (Temperatura/Umidade)

### **3:00-4:30 - Lógica de Decisão (1 minuto e 30 segundos)**
- Condições de irrigação
- Serial Monitor ao vivo
- Relé ligando/desligando

### **4:30-5:00 - Conclusão (30 segundos)**
- Resultados alcançados
- Tecnologias utilizadas
- Agradecimentos

---

## 📝 Script Detalhado

### **CENA 1: Introdução (0:00-0:30)**

**[Mostrar tela inicial com circuito Wokwi]**

**Narração:**
> "Olá, somos o Grupo 59 da FIAP e desenvolvemos o FarmTech Solutions, um sistema de irrigação inteligente para agricultura de precisão. Utilizando ESP32 e sensores IoT, nosso sistema monitora em tempo real as condições do solo e decide automaticamente quando irrigar, otimizando o uso de água e maximizando a produtividade agrícola."

---

### **CENA 2: Componentes do Circuito (0:30-1:30)**

**[Zoom no circuito, destacar cada componente]**

**Narração:**
> "Nosso sistema é composto por 5 componentes principais integrados ao ESP32. Vamos conhecer cada um deles:"

#### **Tabela para Mostrar na Tela:**

| Componente | Pino GPIO | Função |
|------------|-----------|--------|
| **ESP32 DevKit v1** | - | Microcontrolador principal |
| **3 Botões Verdes** | GPIO 2, 4, 5 | Simulam sensores NPK (N, P, K) |
| **LDR (Photoresistor)** | GPIO 34 (A0) | Simula sensor de pH do solo |
| **DHT22** | GPIO 21 | Temperatura e umidade do ar |
| **Relé Azul** | GPIO 18 | Controla bomba d'água |

**[Apontar cada componente no circuito enquanto fala]**

**Narração:**
> "Os três botões verdes simulam sensores NPK que medem Nitrogênio, Fósforo e Potássio no solo. O LDR simula o sensor de pH através da luminosidade. O DHT22 mede temperatura e umidade do ar, que usamos para estimar a umidade do solo. E o relé azul controla a bomba d'água para irrigação."

---

### **CENA 3A: Demonstração NPK (1:30-2:00)**

**[Clicar nos botões NPK um por vez]**

**Narração:**
> "Vamos testar os sensores NPK. Nosso sistema está configurado para cultura de BANANA, que exige muito Potássio."

#### **Tabela NPK - Banana:**

| Nutriente | Dosagem | Criticidade | Botão |
|-----------|---------|-------------|-------|
| **Nitrogênio (N)** | 15 g/m² | Alta | GPIO 2 |
| **Fósforo (P)** | 10 g/m² | Média | GPIO 4 |
| **Potássio (K)** | 20 g/m² | **CRÍTICA** | GPIO 5 |

**[Pressionar botão K (Potássio) e mostrar Serial Monitor]**

**Serial Monitor mostrará:**
```
🧪 NPK - Níveis de Nutrientes:
   🔵 Nitrogênio (N): ❌ BAIXO
   🟡 Fósforo (P):    ❌ BAIXO
   🟢 Potássio (K):   ✅ OK [CRÍTICO p/ banana]

   📋 Status NPK: ⚠️ INSUFICIENTE - Aplicar fertilizantes!
```

**Narração:**
> "Com apenas o Potássio OK, o sistema detecta que os nutrientes estão INSUFICIENTES. Para banana, todos os três elementos são necessários, mas o Potássio é crítico."

---

### **CENA 3B: Demonstração LDR/pH (2:00-2:30)**

**[Clicar no LDR e ajustar o slider]**

**Narração:**
> "Agora vamos testar o sensor de pH simulado pelo LDR. Quanto mais luz, mais ácido o solo."

#### **Tabela LDR → pH:**

| Luminosidade | ADC | pH | Status | Irrigação |
|--------------|-----|-----|--------|-----------|
| 10 lux | 50 | 8.9 | 🟦 ALCALINO | Liga |
| **500 lux** | **1527** | **6.8** | **🟩 NEUTRO ✅** | **Desliga** |
| 100000 lux | 3500 | 4.2 | 🟥 ÁCIDO | Liga |

**[Ajustar LDR para 500 lux]**

**Serial Monitor mostrará:**
```
📊 [SENSOR LDR/pH]
   💡 Luminosidade: 500 lux
   📈 ADC Value: 1527 / 4095 (37.3%)
   🧪 pH Calculado: 6.8 → 🟩 NEUTRO (IDEAL)

🧪 pH do Solo:
   📋 Status: 🟩 NEUTRO (5.5-7.5) - IDEAL
```

**Narração:**
> "Com 500 lux, obtemos um pH de 6.8, que está na faixa NEUTRA ideal para agricultura. Entre 5.5 e 7.5 é considerado adequado."

**[Ajustar LDR para 100000 lux]**

**Serial Monitor mostrará:**
```
📊 [SENSOR LDR/pH]
   💡 Luminosidade: 100000 lux
   📈 ADC Value: 3500 / 4095 (85.5%)
   🧪 pH Calculado: 4.2 → 🟥 ÁCIDO

🧪 pH do Solo:
   📋 Status: 🟥 ÁCIDO (< 5.5)
   💡 Recomendação: Aplicar Fósforo (P) e Potássio (K)
```

**Narração:**
> "Com muita luz, o pH cai para 4.2, indicando solo ÁCIDO. O sistema recomenda aplicar Fósforo e Potássio para correção."

---

### **CENA 3C: Demonstração DHT22 (2:30-3:00)**

**[Clicar no DHT22 e ajustar sliders]**

**Narração:**
> "O DHT22 mede temperatura e umidade do ar. O sistema converte a umidade do ar em umidade do solo multiplicando por 0.8, pois o solo é tipicamente 20% menos úmido que o ar."

#### **Tabela Umidade:**

| DHT22 (Ar) | Cálculo | Solo | Status |
|------------|---------|------|--------|
| 30% | 30 × 0.8 | 24% | 🏜️ MUITO SECO |
| **40%** | **40 × 0.8** | **32%** | **🏜️ SECO - IRRIGAR!** |
| 75% | 75 × 0.8 | 60% | ✅ IDEAL |
| 100% | 100 × 0.8 | 80% | ☔ ENCHARCADO |

**[Configurar DHT22: Temperatura 24°C, Umidade 40%]**

**Serial Monitor mostrará:**
```
🌡️ Condições Ambientais:
   🌡️  Temperatura: 24.0 °C ✅ IDEAL
   💧 Umidade Solo: 32.0 % 🏜️ SECO - IRRIGAR!
```

**Narração:**
> "Com umidade do ar em 40%, o solo fica com 32%. Como está abaixo de 40% (mínimo), o sistema detecta solo SECO e aciona a irrigação."

---

### **CENA 4: Lógica de Decisão (3:00-4:30)**

**[Mostrar Serial Monitor com status completo]**

**Narração:**
> "O sistema analisa 6 condições diferentes para decidir se deve irrigar ou não. Vamos ver cada uma delas:"

#### **Tabela de Condições de Irrigação:**

| Condição | Quando Liga | Prioridade |
|----------|-------------|------------|
| **1. Umidade Baixa** | Solo < 40% | 🔴 CRÍTICA |
| **2. Solo Encharcado** | Solo > 80% | 🔴 NUNCA IRRIGA |
| **3. NPK Insuficiente** | NPK ruim + Solo < 60% | 🟡 MÉDIA |
| **4. pH Inadequado** | pH < 5.5 ou > 7.5 + Solo < 60% | 🟡 MÉDIA |
| **5. Temperatura Alta** | Temp > 30°C + Solo < 60% | 🟠 BAIXA |
| **6. Tudo OK** | Condições adequadas | ✅ DESLIGA |

**[Demonstrar cenário com múltiplas condições ativadas]**

**Serial Monitor mostrará:**
```
💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧
  🚨 IRRIGAÇÃO LIGADA!
💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧
  📌 Motivo: Umidade solo baixa (32.0% < 40%)
💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧

💡 Recomendações:
   ⚠️ Aplicar fertilizantes NPK conforme necessidade
   🍌 URGENTE: Aplicar Potássio (20 g/m²)
   ⚠️ Corrigir pH do solo com NPK adequado
   💧 Irrigação necessária AGORA
```

**Narração:**
> "Neste momento, o sistema identificou solo seco com 32% de umidade, abaixo do mínimo de 40%. A irrigação foi LIGADA automaticamente. Além disso, o sistema fornece recomendações: aplicar fertilizantes NPK, com urgência para Potássio por se tratar de cultura de banana."

---

### **CENA 5: Cenário Ideal (4:00-4:30)**

**[Ajustar sensores para condições ideais]**

**Configuração:**
- Botões NPK: Todos pressionados ✅
- LDR: 500 lux (pH 6.8) ✅
- DHT22: 75% umidade (solo 60%) ✅
- Temperatura: 24°C ✅

**Serial Monitor mostrará:**
```
🧪 NPK - Níveis de Nutrientes:
   🔵 Nitrogênio (N): ✅ OK
   🟡 Fósforo (P):    ✅ OK
   🟢 Potássio (K):   ✅ OK [CRÍTICO p/ banana]
   📋 Status NPK: ✅ ADEQUADO para a cultura

🧪 pH do Solo:
   📋 Status: 🟩 NEUTRO (5.5-7.5) - IDEAL

🌡️ Condições Ambientais:
   🌡️  Temperatura: 24.0 °C ✅ IDEAL
   💧 Umidade Solo: 60.0 % ✅ IDEAL

⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️
  ✅ IRRIGAÇÃO DESLIGADA
⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️
  📌 Motivo: Condições adequadas (umidade: 60.0%)
⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️
```

**Narração:**
> "Com todos os parâmetros na faixa ideal - NPK adequado, pH neutro, umidade em 60% e temperatura ideal - o sistema DESLIGA a irrigação automaticamente, economizando água e energia."

---

### **CENA 6: Diferenças entre Culturas (4:30-4:50)**

**[Mostrar código com culturas diferentes]**

**Narração:**
> "O sistema diferencia as necessidades de cada cultura. Para BANANA, o Potássio é crítico. Para MILHO, o Nitrogênio é essencial."

#### **Tabela Comparativa:**

| Cultura | N (g/m²) | P (g/m²) | K (g/m²) | Elemento Crítico |
|---------|----------|----------|----------|------------------|
| **🍌 Banana** | 15 (Alta) | 10 (Média) | **20 (CRÍTICA)** | **Potássio (K)** |
| **🌽 Milho** | **12 (CRÍTICA)** | 8 (Alta) | 10 (Média) | **Nitrogênio (N)** |

**Narração:**
> "Essas dosagens são baseadas em dados científicos da EMBRAPA, garantindo precisão e eficiência no manejo agrícola."

---

### **CENA 7: Conclusão (4:50-5:00)**

**[Mostrar circuito completo funcionando]**

**Narração:**
> "O FarmTech Solutions demonstra como IoT e automação podem revolucionar a agricultura, otimizando recursos, aumentando produtividade e promovendo sustentabilidade. Tecnologias utilizadas: ESP32, sensores NPK, LDR, DHT22, e lógica de decisão inteligente baseada em dados agronômicos reais. Obrigado!"

**[Fade out com informações na tela]**

**Texto na tela:**
```
FarmTech Solutions
Grupo 59 - FIAP 2025
Fase 2: Sistema de Irrigação Inteligente

GitHub: github.com/Phemassa/fiap-farmtech-fase2
Wokwi: wokwi.com
```

---

## 📊 Tabelas de Referência Rápida

### **Limites do Sistema:**

| Parâmetro | Mínimo | Ideal | Máximo |
|-----------|--------|-------|--------|
| **Umidade Solo** | 40% | 60% | 80% |
| **pH** | 5.5 | 6.5 | 7.5 |
| **Temperatura** | 15°C | 20-25°C | 35°C |

### **Pinout ESP32:**

| Sensor/Atuador | Pino | Tipo |
|----------------|------|------|
| Botão N | GPIO 2 | Digital (INPUT_PULLUP) |
| Botão P | GPIO 4 | Digital (INPUT_PULLUP) |
| Botão K | GPIO 5 | Digital (INPUT_PULLUP) |
| LDR | GPIO 34 (A0) | Analógico (0-4095) |
| DHT22 | GPIO 21 | Digital (protocolo DHT) |
| Relé | GPIO 18 | Digital (OUTPUT) |

---

## 🎯 Dicas para Gravação

### **Preparação:**
1. ✅ Testar circuito no Wokwi antes de gravar
2. ✅ Preparar configurações de sensores com antecedência
3. ✅ Deixar Serial Monitor visível e com fonte legível
4. ✅ Ter script impresso ou em segunda tela

### **Durante Gravação:**
1. 🎤 Falar claramente e pausadamente
2. 🖱️ Movimentos de mouse suaves
3. 📊 Mostrar tabelas na tela quando mencionar números
4. ⏱️ Controlar tempo (máximo 5 minutos!)

### **Edição:**
1. ✂️ Adicionar legendas com valores importantes
2. 🔍 Zoom em componentes quando explicar
3. 🎵 Música de fundo suave (opcional)
4. 📝 Adicionar créditos no final

---

## 📝 Checklist Final

- [ ] Circuito funcionando no Wokwi
- [ ] Serial Monitor configurado (115200 baud)
- [ ] Script revisado e cronometrado
- [ ] Tabelas preparadas para inserir na edição
- [ ] Software de gravação testado
- [ ] Áudio claro e sem ruídos
- [ ] Vídeo renderizado em HD (1080p)
- [ ] Upload no YouTube (não listado)
- [ ] Link adicionado no README.md
- [ ] Vídeo testado (assistir completo)

---

**Boa sorte na gravação! 🎬🚀**

**Tempo estimado de preparação:** 1-2 horas  
**Tempo de gravação:** 10-15 minutos (com retakes)  
**Tempo de edição:** 30-60 minutos  
**Total:** 2-3 horas para vídeo profissional

---

**Criado em:** 11/10/2025  
**Para:** Entrega FIAP - Fase 2 Cap 1  
**Prazo:** 15/10/2025
