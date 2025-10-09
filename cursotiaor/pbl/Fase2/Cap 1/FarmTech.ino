/**
 * ═══════════════════════════════════════════════════════════════════════════
 * FarmTech Solutions - Sistema de Irrigação Inteligente
 * ═══════════════════════════════════════════════════════════════════════════
 * 
 * PROJETO: Fase 2 - Coleta de Dados e Irrigação Automatizada
 * CULTURAS: Milho e Banana
 * PLATAFORMA: ESP32 (Simulação Wokwi.com)
 * 
 * COMPONENTES:
 * - 3 Botões Verdes: Simulam sensores NPK (Nitrogênio, Fósforo, Potássio)
 * - LDR: Simula sensor de pH do solo (0-14)
 * - DHT22: Sensor de temperatura e umidade (simulando umidade do solo)
 * - Relé Azul: Controla bomba d'água para irrigação
 * 
 * LÓGICA DE DECISÃO:
 * - Analisa níveis de NPK e pH
 * - Monitora umidade do solo (DHT22)
 * - Liga/desliga irrigação automaticamente
 * - Baseado em dados científicos (EMBRAPA, IAC)
 * 
 * AUTORES: Grupo 59 FIAP
 * DATA: Outubro 2025
 * ═══════════════════════════════════════════════════════════════════════════
 */

#include <Arduino.h>
#include <DHT.h>

// ═══════════════════════════════════════════════════════════════════════════
// CONFIGURAÇÃO DE PINOS
// ═══════════════════════════════════════════════════════════════════════════

// Sensores NPK (3 Botões Verdes)
#define BTN_NITROGEN 2       // GPIO 2  - Botão Nitrogênio (N)
#define BTN_PHOSPHORUS 4     // GPIO 4  - Botão Fósforo (P)
#define BTN_POTASSIUM 5      // GPIO 5  - Botão Potássio (K)

// Sensor de pH (LDR)
#define LDR_PIN 34           // GPIO 34 - Entrada analógica (ADC1)

// Sensor de Umidade/Temperatura (DHT22)
#define DHT_PIN 21           // GPIO 21 - Corrigido para corresponder ao diagram.json
#define DHT_TYPE DHT22

// Relé (Bomba d'água)
#define RELAY_PIN 18         // GPIO 18 - Controla irrigação

// ═══════════════════════════════════════════════════════════════════════════
// CONFIGURAÇÕES DO SISTEMA
// ═══════════════════════════════════════════════════════════════════════════

// Cultura atual (0 = Banana, 1 = Milho)
#define CULTURA_BANANA 0
#define CULTURA_MILHO 1
int culturaAtual = CULTURA_BANANA;  // Trocar para CULTURA_MILHO se necessário

// Intervalo de leituras (milissegundos)
#define INTERVALO_LEITURA 5000    // 5 segundos

// Limites de umidade do solo (%)
#define UMIDADE_MINIMA 40.0       // Abaixo disso: irrigar
#define UMIDADE_IDEAL 60.0        // Faixa ideal
#define UMIDADE_MAXIMA 80.0       // Acima disso: solo encharcado

// Limites de pH
#define PH_MINIMO 5.5             // pH mínimo adequado
#define PH_MAXIMO 7.5             // pH máximo adequado
#define PH_IDEAL 6.5              // pH ideal

// ═══════════════════════════════════════════════════════════════════════════
// TABELA DE DOSAGENS NPK (Baseado em dados científicos)
// ═══════════════════════════════════════════════════════════════════════════

// BANANA: Alta exigência em Potássio (K)
#define BANANA_N 15  // 15 g/m² Nitrogênio
#define BANANA_P 10  // 10 g/m² Fósforo
#define BANANA_K 20  // 20 g/m² Potássio (CRÍTICO para banana!)

// MILHO: Alta exigência em Nitrogênio (N)
#define MILHO_N 12   // 12 g/m² Nitrogênio (CRÍTICO para milho!)
#define MILHO_P 8    // 8 g/m² Fósforo
#define MILHO_K 10   // 10 g/m² Potássio

// ═══════════════════════════════════════════════════════════════════════════
// INICIALIZAÇÃO DE OBJETOS
// ═══════════════════════════════════════════════════════════════════════════

DHT dht(DHT_PIN, DHT_TYPE);

// ═══════════════════════════════════════════════════════════════════════════
// VARIÁVEIS GLOBAIS
// ═══════════════════════════════════════════════════════════════════════════

// Sensores NPK (estado dos botões)
bool nitrogenioOK = false;
bool fosforoOK = false;
bool potassioOK = false;

// Dados do solo
float temperaturaAr = 0.0;
float umidadeSolo = 0.0;        // DHT22 simula umidade do solo
float phSolo = 0.0;             // Calculado a partir do LDR
int ldrValue = 0;

// Estado da irrigação
bool releLigado = false;
bool irrigacaoAutomatica = true;

// Controle de tempo
unsigned long ultimaLeitura = 0;
int contadorLeituras = 0;

// ═══════════════════════════════════════════════════════════════════════════
// DECLARAÇÕES DE FUNÇÕES
// ═══════════════════════════════════════════════════════════════════════════

void lerSensores();
void decidirIrrigacao();
bool verificarNPKAdequado();
void ligarIrrigacao(String motivo);
void desligarIrrigacao(String motivo);
void exibirStatus();
void exibirBanner();
void exibirRequisitosBanana();
void exibirRequisitosMilho();

// ═══════════════════════════════════════════════════════════════════════════
// SETUP - INICIALIZAÇÃO
// ═══════════════════════════════════════════════════════════════════════════

void setup() {
  // Inicializa Serial Monitor
  Serial.begin(115200);
  delay(1000);  // Delay maior para estabilização
  
  Serial.println("🔄 Iniciando sistema...");
  delay(500);
  
  // Banner inicial
  exibirBanner();
  
  // Configuração de pinos
  pinMode(BTN_NITROGEN, INPUT_PULLUP);     // Botão com pull-up interno
  pinMode(BTN_PHOSPHORUS, INPUT_PULLUP);
  pinMode(BTN_POTASSIUM, INPUT_PULLUP);
  pinMode(LDR_PIN, INPUT);                 // LDR analógico
  pinMode(RELAY_PIN, OUTPUT);              // Relé saída
  
  // Estado inicial do relé (desligado)
  digitalWrite(RELAY_PIN, LOW);
  releLigado = false;
  
  // Inicializa DHT22 com verificação
  Serial.println("[INIT] 🔄 Inicializando DHT22...");
  dht.begin();
  delay(2000);  // DHT22 precisa de tempo para estabilizar
  
  Serial.println("[INIT] ✅ Pinos configurados");
  Serial.println("[INIT] ✅ DHT22 inicializado");
  Serial.println("[INIT] ✅ Sistema pronto para operação");
  
  // Exibe cultura selecionada
  Serial.println();
  Serial.print("🌾 Cultura selecionada: ");
  if (culturaAtual == CULTURA_BANANA) {
    Serial.println("BANANA 🍌");
    exibirRequisitosBanana();
  } else {
    Serial.println("MILHO 🌽");
    exibirRequisitosMilho();
  }
  
  Serial.println();
  Serial.println("═══════════════════════════════════════════════════════════════");
  Serial.println("  < 📊 INICIANDO MONITORAMENTO...>");
  Serial.println("═══════════════════════════════════════════════════════════════");
  Serial.println();
  
  delay(2000);  // Aguarda estabilização
}

// ═══════════════════════════════════════════════════════════════════════════
// LOOP PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════════

void loop() {
  unsigned long tempoAtual = millis();
  
  // Verifica se é hora de fazer leitura
  if (tempoAtual - ultimaLeitura >= INTERVALO_LEITURA) {
    ultimaLeitura = tempoAtual;
    contadorLeituras++;
    
    // Realiza leitura de sensores
    lerSensores();
    
    // Analisa condições e decide irrigação
    if (irrigacaoAutomatica) {
      decidirIrrigacao();
    }
    
    // Exibe status
    exibirStatus();
    
    Serial.println();
  }
  
  delay(10);  // Pequeno delay para não sobrecarregar
}

// ═══════════════════════════════════════════════════════════════════════════
// FUNÇÕES DE LEITURA DE SENSORES
// ═══════════════════════════════════════════════════════════════════════════

void lerSensores() {
  // ─────────────────────────────────────────────────────────────────────────
  // 1. Leitura de NPK (Botões)
  // ─────────────────────────────────────────────────────────────────────────
  // Nota: INPUT_PULLUP inverte lógica (LOW = pressionado)
  nitrogenioOK = !digitalRead(BTN_NITROGEN);
  fosforoOK = !digitalRead(BTN_PHOSPHORUS);
  potassioOK = !digitalRead(BTN_POTASSIUM);
  
  // ─────────────────────────────────────────────────────────────────────────
  // 2. Leitura de pH (LDR)
  // ─────────────────────────────────────────────────────────────────────────
  ldrValue = analogRead(LDR_PIN);
  
  // Conversão LDR → pH (0-4095 para ESP32 ADC 12-bit)
  // LDR baixo (escuro) = pH alto (alcalino)
  // LDR alto (claro) = pH baixo (ácido)
  // Fórmula: pH = 9.0 - (ldrValue / 4095.0) * 6.0
  // Resultado: 0-4095 → pH 9.0-3.0
  phSolo = 9.0 - (ldrValue / 4095.0) * 6.0;
  
  // ─────────────────────────────────────────────────────────────────────────
  // 3. Leitura de Umidade e Temperatura (DHT22)
  // ─────────────────────────────────────────────────────────────────────────
  temperaturaAr = dht.readTemperature();
  float umidadeAr = dht.readHumidity();
  
  // Validação
  if (isnan(temperaturaAr) || isnan(umidadeAr)) {
    Serial.println("❌ [ERRO] Falha na leitura do DHT22!");
    temperaturaAr = 25.0;   // Valor padrão
    umidadeAr = 60.0;
  }
  
  // Simula umidade do solo baseada na umidade do ar
  // Em produção real, usar sensor de umidade de solo capacitivo
  umidadeSolo = umidadeAr * 0.8;  // Solo geralmente 20% menos úmido que ar
}

// ═══════════════════════════════════════════════════════════════════════════
// LÓGICA DE DECISÃO DE IRRIGAÇÃO
// ═══════════════════════════════════════════════════════════════════════════

void decidirIrrigacao() {
  bool deveIrrigar = false;
  String motivo = "";
  
  // ─────────────────────────────────────────────────────────────────────────
  // CONDIÇÃO 1: Umidade do solo baixa
  // ─────────────────────────────────────────────────────────────────────────
  if (umidadeSolo < UMIDADE_MINIMA) {
    deveIrrigar = true;
    motivo = "Umidade solo baixa (" + String(umidadeSolo, 1) + "% < " + String(UMIDADE_MINIMA, 0) + "%)";
  }
  
  // ─────────────────────────────────────────────────────────────────────────
  // CONDIÇÃO 2: Solo encharcado (NÃO irrigar)
  // ─────────────────────────────────────────────────────────────────────────
  else if (umidadeSolo > UMIDADE_MAXIMA) {
    deveIrrigar = false;
    motivo = "Solo encharcado (" + String(umidadeSolo, 1) + "% > " + String(UMIDADE_MAXIMA, 0) + "%)";
  }
  
  // ─────────────────────────────────────────────────────────────────────────
  // CONDIÇÃO 3: NPK insuficiente + Umidade abaixo do ideal
  // ─────────────────────────────────────────────────────────────────────────
  else if (umidadeSolo < UMIDADE_IDEAL && !verificarNPKAdequado()) {
    deveIrrigar = true;
    motivo = "NPK insuficiente + umidade subótima";
  }
  
  // ─────────────────────────────────────────────────────────────────────────
  // CONDIÇÃO 4: pH inadequado (ajustar com irrigação)
  // ─────────────────────────────────────────────────────────────────────────
  else if ((phSolo < PH_MINIMO || phSolo > PH_MAXIMO) && umidadeSolo < UMIDADE_IDEAL) {
    deveIrrigar = true;
    motivo = "pH fora da faixa (" + String(phSolo, 1) + ") + umidade baixa";
  }
  
  // ─────────────────────────────────────────────────────────────────────────
  // CONDIÇÃO 5: Temperatura alta + Umidade baixa
  // ─────────────────────────────────────────────────────────────────────────
  else if (temperaturaAr > 30.0 && umidadeSolo < UMIDADE_IDEAL) {
    deveIrrigar = true;
    motivo = "Temperatura alta (" + String(temperaturaAr, 1) + "°C) + umidade baixa";
  }
  
  // ─────────────────────────────────────────────────────────────────────────
  // CONDIÇÃO 6: Tudo OK - Desligar irrigação
  // ─────────────────────────────────────────────────────────────────────────
  else {
    deveIrrigar = false;
    motivo = "Condições adequadas (umidade: " + String(umidadeSolo, 1) + "%)";
  }
  
  // ─────────────────────────────────────────────────────────────────────────
  // Executa decisão
  // ─────────────────────────────────────────────────────────────────────────
  if (deveIrrigar && !releLigado) {
    ligarIrrigacao(motivo);
  } else if (!deveIrrigar && releLigado) {
    desligarIrrigacao(motivo);
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// VERIFICAÇÃO DE NPK ADEQUADO
// ═══════════════════════════════════════════════════════════════════════════

bool verificarNPKAdequado() {
  // Lógica específica por cultura
  
  if (culturaAtual == CULTURA_BANANA) {
    // BANANA: Exige MUITO Potássio (K)
    // Prioridade: K > N > P
    if (!potassioOK) {
      return false;  // Potássio é CRÍTICO para banana
    }
    if (!nitrogenioOK || !fosforoOK) {
      return false;  // N e P também necessários
    }
    return true;
    
  } else if (culturaAtual == CULTURA_MILHO) {
    // MILHO: Exige MUITO Nitrogênio (N)
    // Prioridade: N > P > K
    if (!nitrogenioOK) {
      return false;  // Nitrogênio é CRÍTICO para milho
    }
    if (!fosforoOK || !potassioOK) {
      return false;  // P e K também necessários
    }
    return true;
  }
  
  return false;
}

// ═══════════════════════════════════════════════════════════════════════════
// CONTROLE DE IRRIGAÇÃO
// ═══════════════════════════════════════════════════════════════════════════

void ligarIrrigacao(String motivo) {
  digitalWrite(RELAY_PIN, HIGH);
  releLigado = true;
  
  Serial.println();
  Serial.println("💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧");
  Serial.println("  🚨 IRRIGAÇÃO LIGADA!");
  Serial.println("💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧");
  Serial.print("  📌 Motivo: ");
  Serial.println(motivo);
  Serial.println("💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧💧");
  Serial.println();
}

void desligarIrrigacao(String motivo) {
  digitalWrite(RELAY_PIN, LOW);
  releLigado = false;
  
  Serial.println();
  Serial.println("⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️");
  Serial.println("  ✅ IRRIGAÇÃO DESLIGADA");
  Serial.println("⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️");
  Serial.print("  📌 Motivo: ");
  Serial.println(motivo);
  Serial.println("⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️⏸️");
  Serial.println();
}

// ═══════════════════════════════════════════════════════════════════════════
// EXIBIÇÃO DE STATUS
// ═══════════════════════════════════════════════════════════════════════════

void exibirStatus() {
  Serial.println("═══════════════════════════════════════════════════════════════");
  Serial.print("  📊 LEITURA #");
  Serial.print(contadorLeituras);
  Serial.print(" - ");
  Serial.print(millis() / 1000);
  Serial.println("s");
  Serial.println("═══════════════════════════════════════════════════════════════");
  
  // ─────────────────────────────────────────────────────────────────────────
  // Sensores NPK
  // ─────────────────────────────────────────────────────────────────────────
  Serial.println("\n🧪 NPK - Níveis de Nutrientes:");
  Serial.print("   🔵 Nitrogênio (N): ");
  Serial.print(nitrogenioOK ? "✅ OK" : "❌ BAIXO");
  if (culturaAtual == CULTURA_MILHO) Serial.print(" [CRÍTICO p/ milho]");
  Serial.println();
  
  Serial.print("   🟡 Fósforo (P):    ");
  Serial.println(fosforoOK ? "✅ OK" : "❌ BAIXO");
  
  Serial.print("   🟢 Potássio (K):   ");
  Serial.print(potassioOK ? "✅ OK" : "❌ BAIXO");
  if (culturaAtual == CULTURA_BANANA) Serial.print(" [CRÍTICO p/ banana]");
  Serial.println();
  
  // Status geral NPK
  bool npkAdequado = verificarNPKAdequado();
  Serial.print("\n   📋 Status NPK: ");
  if (npkAdequado) {
    Serial.println("✅ ADEQUADO para a cultura");
  } else {
    Serial.println("⚠️  INSUFICIENTE - Aplicar fertilizantes!");
  }
  
  // ─────────────────────────────────────────────────────────────────────────
  // pH do Solo
  // ─────────────────────────────────────────────────────────────────────────
  Serial.println("\n🧪 pH do Solo:");
  Serial.print("   📊 LDR Value: ");
  Serial.print(ldrValue);
  Serial.print(" → pH ");
  Serial.println(phSolo, 1);
  
  Serial.print("   📋 Status: ");
  if (phSolo < PH_MINIMO) {
    Serial.println("🟥 ÁCIDO (< " + String(PH_MINIMO, 1) + ")");
    Serial.println("   💡 Recomendação: Aplicar Fósforo (P) e Potássio (K)");
  } else if (phSolo > PH_MAXIMO) {
    Serial.println("🟦 ALCALINO (> " + String(PH_MAXIMO, 1) + ")");
    Serial.println("   💡 Recomendação: Aplicar Nitrogênio (N)");
  } else {
    Serial.println("🟩 NEUTRO (" + String(PH_MINIMO, 1) + "-" + String(PH_MAXIMO, 1) + ") - IDEAL");
  }
  
  // ─────────────────────────────────────────────────────────────────────────
  // Temperatura e Umidade
  // ─────────────────────────────────────────────────────────────────────────
  Serial.println("\n🌡️ Condições Ambientais:");
  Serial.print("   🌡️  Temperatura: ");
  Serial.print(temperaturaAr, 1);
  Serial.print(" °C ");
  if (temperaturaAr < 15) Serial.println("❄️ BAIXA");
  else if (temperaturaAr < 25) Serial.println("✅ IDEAL");
  else if (temperaturaAr < 35) Serial.println("🌡️ ELEVADA");
  else Serial.println("🔥 CRÍTICA");
  
  Serial.print("   💧 Umidade Solo: ");
  Serial.print(umidadeSolo, 1);
  Serial.print(" % ");
  if (umidadeSolo < UMIDADE_MINIMA) Serial.println("🏜️ SECO - IRRIGAR!");
  else if (umidadeSolo < UMIDADE_IDEAL) Serial.println("⚠️ ABAIXO DO IDEAL");
  else if (umidadeSolo < UMIDADE_MAXIMA) Serial.println("✅ IDEAL");
  else Serial.println("☔ ENCHARCADO");
  
  // ─────────────────────────────────────────────────────────────────────────
  // Estado da Irrigação
  // ─────────────────────────────────────────────────────────────────────────
  Serial.println("\n💧 Sistema de Irrigação:");
  Serial.print("   🔌 Relé: ");
  Serial.println(releLigado ? "⚡ LIGADO (irrigando)" : "⏸️ DESLIGADO");
  
  Serial.print("   🤖 Modo: ");
  Serial.println(irrigacaoAutomatica ? "AUTOMÁTICO ✅" : "MANUAL");
  
  // ─────────────────────────────────────────────────────────────────────────
  // Recomendações
  // ─────────────────────────────────────────────────────────────────────────
  Serial.println("\n💡 Recomendações:");
  
  if (!npkAdequado) {
    Serial.println("   ⚠️ Aplicar fertilizantes NPK conforme necessidade");
    if (culturaAtual == CULTURA_BANANA && !potassioOK) {
      Serial.println("   🍌 URGENTE: Aplicar Potássio (20 g/m²)");
    }
    if (culturaAtual == CULTURA_MILHO && !nitrogenioOK) {
      Serial.println("   🌽 URGENTE: Aplicar Nitrogênio (12 g/m²)");
    }
  }
  
  if (phSolo < PH_MINIMO || phSolo > PH_MAXIMO) {
    Serial.println("   ⚠️ Corrigir pH do solo com NPK adequado");
  }
  
  if (umidadeSolo < UMIDADE_MINIMA) {
    Serial.println("   💧 Irrigação necessária AGORA");
  } else if (umidadeSolo > UMIDADE_MAXIMA) {
    Serial.println("   ⏸️ Suspender irrigação - Solo encharcado");
  }
  
  if (temperaturaAr > 30) {
    Serial.println("   🌡️ Temperatura alta - Aumentar frequência de irrigação");
  }
  
  Serial.println("═══════════════════════════════════════════════════════════════");
}

// ═══════════════════════════════════════════════════════════════════════════
// FUNÇÕES AUXILIARES - EXIBIÇÃO
// ═══════════════════════════════════════════════════════════════════════════

void exibirBanner() {
  Serial.println("\n\n");
  Serial.println("═══════════════════════════════════════════════════════════════");
  Serial.println("  🚜 FARMTECH SOLUTIONS - SISTEMA DE IRRIGAÇÃO INTELIGENTE");
  Serial.println("═══════════════════════════════════════════════════════════════");
  Serial.println("  📡 Fase 2: Coleta de Dados e Automação");
  Serial.println("  🌾 Culturas: Milho e Banana");
  Serial.println("  📊 Sensores: NPK, pH (LDR), Umidade (DHT22), Relé");
  Serial.println("═══════════════════════════════════════════════════════════════");
  Serial.println("  👥 Grupo 59 FIAP - Outubro 2025");
  Serial.println("═══════════════════════════════════════════════════════════════");
  Serial.println();
}

void exibirRequisitosBanana() {
  Serial.println("\n📋 REQUISITOS NUTRICIONAIS - BANANA 🍌:");
  Serial.println("   🔵 Nitrogênio (N):  " + String(BANANA_N) + " g/m² (Alta)");
  Serial.println("   🟡 Fósforo (P):     " + String(BANANA_P) + " g/m² (Média)");
  Serial.println("   🟢 Potássio (K):    " + String(BANANA_K) + " g/m² (CRÍTICA!)");
  Serial.println("\n   ⚠️ BANANA = EXTREMAMENTE EXIGENTE EM POTÁSSIO!");
  Serial.println("   💡 K melhora sabor, tamanho e resistência ao transporte");
  Serial.println("   📊 pH ideal: 5.5-7.5");
  Serial.println("   💧 Umidade ideal: 60-70%");
}

void exibirRequisitosMilho() {
  Serial.println("\n📋 REQUISITOS NUTRICIONAIS - MILHO 🌽:");
  Serial.println("   🔵 Nitrogênio (N):  " + String(MILHO_N) + " g/m² (CRÍTICA!)");
  Serial.println("   🟡 Fósforo (P):     " + String(MILHO_P) + " g/m² (Alta)");
  Serial.println("   🟢 Potássio (K):    " + String(MILHO_K) + " g/m² (Média)");
  Serial.println("\n   ⚠️ MILHO = ALTA DEMANDA DE NITROGÊNIO!");
  Serial.println("   💡 N fundamental para produção de grãos e proteínas");
  Serial.println("   📊 pH ideal: 5.5-7.5");
  Serial.println("   💧 Umidade ideal: 50-60%");
}
