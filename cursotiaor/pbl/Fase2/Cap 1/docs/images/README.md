# 📸 Screenshots do Circuito Wokwi

Este diretório contém as capturas de tela do simulador Wokwi.com demonstrando o funcionamento do Sistema de Irrigação Inteligente FarmTech.

## 📋 Imagens Disponíveis

### 1. `wokwi-circuito-completo-ldr.png`
**Descrição:** Circuito completo mostrando configuração do LDR (Photoresistor)
- ✅ ESP32 DevKit v1 centralizado
- ✅ LED de status (azul) conectado ao GPIO
- ✅ 3 Botões verdes (N, P, K) para NPK
  - N = Nitrogênio (GPIO 2)
  - P = Fósforo (GPIO 4)
  - K = Potássio (GPIO 5)
- ✅ LDR (Photoresistor) simulando sensor de pH
  - Painel de controle mostrando "ILLUMINATION (LUX): 500 lux"
- ✅ DHT22 (sensor temperatura/umidade) à direita
- ✅ Relé (Module) vermelho/azul à direita inferior
- ✅ Tempo de simulação: 00:08.558

**Características Técnicas:**
- LDR conectado via resistor ao ESP32
- Fios coloridos: Azul (VCC), Preto (GND), Verde (sinais NPK), Laranja (Relé), Azul pontilhado (DHT22)

---

### 2. `wokwi-circuito-completo-dht22.png`
**Descrição:** Circuito completo mostrando configuração do DHT22
- ✅ Mesmo layout do circuito anterior
- ✅ Painel de controle do DHT22 aberto
  - Temperature: 24.0°C (ajustável via slider)
  - Humidity: 40.0% (ajustável via slider)
- ✅ DHT22 destacado com borda pontilhada
- ✅ Tempo de simulação: 00:40.617

**Características Técnicas:**
- DHT22 conectado ao GPIO 21 (conforme código)
- Valores simulados ajustáveis em tempo real
- Umidade do ar = base para cálculo de umidade do solo (× 0.8)

---

## 🔌 Mapa de Conexões Visualizado

Com base nas imagens, as conexões são:

| Componente | Pino ESP32 | Cor do Fio | Observação |
|------------|-----------|------------|------------|
| **LED Status** | GPIO (não especificado) | Azul | Indicador visual |
| **Botão N (Nitrogênio)** | GPIO 2 | Verde | Pull-up interno |
| **Botão P (Fósforo)** | GPIO 4 | Verde | Pull-up interno |
| **Botão K (Potássio)** | GPIO 5 | Verde | Pull-up interno |
| **LDR (pH)** | GPIO 34 (A0) | Conexão analógica | ADC 12-bit (0-4095) |
| **DHT22 Data** | GPIO 21 | Azul pontilhado | Temp + Umidade |
| **Relé IN** | GPIO 18 | Laranja | Controle bomba |
| **Relé VCC** | 3.3V/5V | Vermelho | Alimentação |
| **Relé GND** | GND | Preto | Terra |

---

## 🎯 Como Usar Estas Imagens

### Para o README.md Principal:
```markdown
## 📸 Circuito Wokwi

### Visão Geral do Circuito
![Circuito Completo - LDR](docs/images/wokwi-circuito-completo-ldr.png)
*Circuito mostrando sensor LDR (pH) configurado em 500 lux*

### Configuração DHT22
![Circuito Completo - DHT22](docs/images/wokwi-circuito-completo-dht22.png)
*DHT22 configurado: 24°C e 40% umidade (simulando solo a 32%)*
```

---

## 📝 Instruções para Adicionar Mais Screenshots

Se precisar adicionar novas imagens:

1. **Tire screenshot no Wokwi:**
   - Print da tela inteira (incluindo controles)
   - Print do Serial Monitor com saídas
   - Print mostrando relé ligado/desligado

2. **Nomeie adequadamente:**
   - `wokwi-serial-monitor-irrigacao-ligada.png`
   - `wokwi-serial-monitor-status-completo.png`
   - `wokwi-rele-ativo.png`

3. **Salve neste diretório:**
   - `c:\Fiap Projeto\Fase2\cursotiaor\pbl\Fase2\Cap 1\docs\images\`

4. **Documente aqui:**
   - Adicione descrição similar às acima
   - Inclua tempo de simulação e valores dos sensores

---

## ✅ Checklist de Screenshots Recomendados

### Obrigatórios (para entrega FIAP):
- [x] Circuito completo mostrando LDR
- [x] Circuito completo mostrando DHT22
- [ ] Serial Monitor com sistema iniciando (banner)
- [ ] Serial Monitor com leitura de sensores
- [ ] Serial Monitor com irrigação LIGADA
- [ ] Serial Monitor com irrigação DESLIGADA

### Opcionais (melhoram apresentação):
- [ ] Botões NPK pressionados (verde aceso)
- [ ] LDR em diferentes níveis de lux (pH diferentes)
- [ ] DHT22 em condições extremas (temp >30°C)
- [ ] Relé com LED indicador visível

---

## 🎥 Sugestão para Vídeo YouTube

Use estas imagens como referência para gravar o vídeo:
1. Mostrar circuito completo (0:00-0:30)
2. Explicar cada sensor (0:30-1:30)
3. Ajustar LDR e mostrar Serial (1:30-2:30)
4. Pressionar botões NPK (2:30-3:30)
5. Demonstrar irrigação liga/desliga (3:30-4:30)
6. Considerações finais (4:30-5:00)

---

**Última atualização:** 11/10/2025  
**Simulador:** [Wokwi.com](https://wokwi.com) - Community License
