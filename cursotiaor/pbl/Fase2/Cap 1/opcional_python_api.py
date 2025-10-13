"""
FarmTech Solutions - Opcional 1: Integração Python com API Pública
Cap 1 - Um Mapa do Tesouro
Atividade: Integração com API meteorológica para otimizar irrigação

Grupo 19 FIAP - 1 ano • 2025/2 - Fase 2 - de 18/09/2025 a 15/10/2025
RM566826 - Phellype Matheus Giacoia Flaibam Massarente
RM567005 - Carlos Alberto Florindo Costato
RM568140 - Cesar Martinho de Azeredo

Objetivo: Consultar previsão de chuva e enviar comando ao ESP32 via Serial
Funcionalidade: Se previsão de chuva > 50%, suspende irrigação automaticamente
"""

import requests
import json
from datetime import datetime
import sys
import argparse

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

# API OpenWeather (use sua chave gratuita de https://openweathermap.org/api)
API_KEY = "SUA_CHAVE_AQUI"  # Substitua por sua chave
CIDADE = "Campinas"  # Cidade da fazenda
PAIS = "BR"

# URL da API de previsão (5 dias)
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

# Arquivo de logs
LOG_FILE = 'logs_irrigacao_api.json'

# ============================================================================
# FUNÇÕES PRINCIPAIS
# ============================================================================

def obter_previsao_chuva():
    """
    Consulta API OpenWeather e retorna probabilidade de chuva nas próximas 24h
    
    Returns:
        dict: {
            'probabilidade': float (0-100),
            'descricao': str,
            'temperatura': float,
            'horario_previsto': str
        }
    """
    try:
        # Parâmetros da requisição
        params = {
            'q': f"{CIDADE},{PAIS}",
            'appid': API_KEY,
            'units': 'metric',  # Celsius
            'lang': 'pt_br'
        }
        
        # Fazer requisição
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        
        dados = response.json()
        
        # Analisar próximas 8 previsões (24 horas, intervalo 3h)
        previsoes_24h = dados['list'][:8]
        
        # Encontrar maior probabilidade de chuva
        max_probabilidade = 0
        melhor_previsao = None
        
        for previsao in previsoes_24h:
            # Probabilidade de precipitação (0-1, converter para 0-100)
            prob = previsao.get('pop', 0) * 100
            
            if prob > max_probabilidade:
                max_probabilidade = prob
                melhor_previsao = previsao
        
        if melhor_previsao:
            return {
                'probabilidade': max_probabilidade,
                'descricao': melhor_previsao['weather'][0]['description'],
                'temperatura': melhor_previsao['main']['temp'],
                'horario_previsto': melhor_previsao['dt_txt']
            }
        else:
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao consultar API: {e}")
        return None
    except KeyError as e:
        print(f"❌ Erro ao processar resposta da API: {e}")
        return None


def decidir_irrigacao(previsao):
    """
    Decide se deve irrigar baseado na previsão de chuva
    
    Args:
        previsao (dict): Dados da previsão meteorológica
    
    Returns:
        bool: True para irrigar, False para suspender
    """
    if not previsao:
        print("⚠️  Sem dados meteorológicos, mantendo irrigação normal")
        return True
    
    prob_chuva = previsao['probabilidade']
    
    # Lógica de decisão
    if prob_chuva >= 70:
        print(f"🌧️  ALTA probabilidade de chuva ({prob_chuva:.1f}%)")
        print(f"   📅 Previsto para: {previsao['horario_previsto']}")
        print(f"   ☔ Descrição: {previsao['descricao']}")
        print(f"   💧 DECISÃO: SUSPENDER irrigação (economia de água)")
        return False
    
    elif prob_chuva >= 40:
        print(f"🌦️  MÉDIA probabilidade de chuva ({prob_chuva:.1f}%)")
        print(f"   📅 Previsto para: {previsao['horario_previsto']}")
        print(f"   ⚠️  DECISÃO: REDUZIR irrigação em 50%")
        return True  # Poderia implementar irrigação parcial
    
    else:
        print(f"☀️  BAIXA probabilidade de chuva ({prob_chuva:.1f}%)")
        print(f"   🌡️  Temperatura: {previsao['temperatura']:.1f}°C")
        print(f"   ✅ DECISÃO: MANTER irrigação normal")
        return True


def enviar_comando_esp32(irrigar):
    """
    Envia comando para ESP32 via Serial (simulado)
    
    Args:
        irrigar (bool): True = ligar irrigação, False = desligar
    
    Nota: Para implementação real, use pyserial:
        import serial
        ser = serial.Serial('COM3', 115200)  # Porta do ESP32
        comando = 'IRRIGAR_ON' if irrigar else 'IRRIGAR_OFF'
        ser.write(comando.encode())
    """
    comando = "IRRIGAR_ON" if irrigar else "IRRIGAR_OFF"
    
    print("\n" + "="*60)
    print("📡 ENVIANDO COMANDO PARA ESP32 (Serial)")
    print("="*60)
    print(f"   Porta: COM3 (exemplo)")
    print(f"   Baud: 115200")
    print(f"   Comando: {comando}")
    print("="*60)
    
    # Simulação de envio
    print(f"\n✅ Comando '{comando}' enviado com sucesso!")
    print("   (Para implementação real, instale: pip install pyserial)")


def salvar_log_decisao(previsao, irrigar):
    """
    Salva log da decisão em arquivo JSON
    
    Args:
        previsao (dict): Dados meteorológicos
        irrigar (bool): Decisão tomada
    """
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'previsao': previsao,
        'decisao': 'IRRIGAR' if irrigar else 'SUSPENDER',
        'motivo': 'Previsão de chuva' if not irrigar else 'Sem chuva prevista'
    }
    
    try:
        # Tentar ler log existente
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except FileNotFoundError:
            logs = []
        
        # Adicionar nova entrada
        logs.append(log_entry)
        
        # Salvar atualizado
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
        
        print(f"\n📝 Log salvo em '{LOG_FILE}'")
        
    except Exception as e:
        print(f"⚠️  Erro ao salvar log: {e}")


# ============================================================================
# MENU E DESCRITIVOS
# ============================================================================

def mostrar_descritivo(opcao: str):
    """Imprime um descritivo acima dos dados esperados para cada opção do menu."""
    print("\n" + "=" * 60)
    if opcao == 'api':
        print("📘 DESCRITIVO - Modo Real (API OpenWeather)")
        print("- Requisitos: Internet ativa e API_KEY válida no script")
        print("- Parâmetros usados: Cidade (CIDADE), País (PAIS), unidades em Celsius (metric)")
        print("- Dados esperados da API (próximas 24h):")
        print("  • probabilidade: 0–100% (campo pop x 100)")
        print("  • descricao: condição do tempo (pt_br)")
        print("  • temperatura: °C no horário de maior probabilidade")
        print("  • horario_previsto: timestamp da previsão (dt_txt)")
        print("- Saídas do sistema:")
        print("  • Decisão: SUSPENDER / REDUZIR / MANTER irrigação")
        print(f"  • Log: registro salvo em '{LOG_FILE}'")
    elif opcao == 'demo':
        print("📘 DESCRITIVO - Modo Demonstração (Dados Simulados)")
        print("- Não usa internet nem API_KEY")
        print("- Dados simulados exibidos:")
        print("  • probabilidade: % chuva (ex.: 75.0)")
        print("  • descricao: texto amigável (ex.: 'chuva moderada')")
        print("  • temperatura: °C (ex.: 24.5)")
        print("  • horario_previsto: data e hora exemplo")
        print("- Saídas do sistema:")
        print("  • Decisão, Comando Serial simulado e log de decisão")
    elif opcao == 'logs':
        print("📘 DESCRITIVO - Visualizar Logs")
        print(f"- Origem: arquivo '{LOG_FILE}' no diretório atual")
        print("- Campos listados por registro:")
        print("  • timestamp: data/hora da decisão")
        print("  • decisao: IRRIGAR ou SUSPENDER")
        print("  • motivo: justificativa resumida")
        print("  • previsao: dicionário com probabilidade/descricao/temperatura/horario")
    print("=" * 60 + "\n")


def visualizar_logs(max_itens: int = 10):
    """Mostra os últimos registros de decisão salvos no arquivo de log."""
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            logs = json.load(f)
    except FileNotFoundError:
        print(f"⚠️  Arquivo de log '{LOG_FILE}' não encontrado.")
        return
    except json.JSONDecodeError:
        print(f"⚠️  Não foi possível ler '{LOG_FILE}' (JSON inválido).")
        return

    print(f"📄 Exibindo até {max_itens} registros mais recentes do log:\n")
    for entry in logs[-max_itens:]:
        print(f"- timestamp: {entry.get('timestamp')}")
        print(f"  decisao:   {entry.get('decisao')}")
        print(f"  motivo:    {entry.get('motivo')}")
        prev = entry.get('previsao') or {}
        print("  previsao:")
        print(f"    • probabilidade: {prev.get('probabilidade')}")
        print(f"    • descricao:     {prev.get('descricao')}")
        print(f"    • temperatura:   {prev.get('temperatura')}")
        print(f"    • horario:       {prev.get('horario_previsto')}\n")


def print_menu():
    print("\n" + "=" * 60)
    print("🌾 FarmTech Solutions - Integração API Meteorológica (Menu)")
    print("=" * 60)
    print("1) Modo Real (API OpenWeather)")
    print("2) Modo Demonstração (dados simulados)")
    print("3) Visualizar logs de decisões")
    print("4) Sair")
    print("=" * 60)


def executar_modo_api():
    mostrar_descritivo('api')
    if API_KEY == "SUA_CHAVE_AQUI":
        print("⚠️  API_KEY não configurada. Configure antes de usar o modo real.")
        return
    print("🌐 Consultando API OpenWeather...\n")
    previsao = obter_previsao_chuva()
    if previsao:
        print("✅ Dados meteorológicos obtidos com sucesso!\n")
        irrigar = decidir_irrigacao(previsao)
        enviar_comando_esp32(irrigar)
        salvar_log_decisao(previsao, irrigar)
    else:
        print("❌ Falha ao obter previsão. Mantendo irrigação padrão.")


def executar_modo_demo():
    mostrar_descritivo('demo')
    previsao_demo = {
        'probabilidade': 75.0,
        'descricao': 'chuva moderada',
        'temperatura': 24.5,
        'horario_previsto': '2025-10-12 15:00:00'
    }
    print("📊 DADOS SIMULADOS (exemplo):")
    irrigar = decidir_irrigacao(previsao_demo)
    enviar_comando_esp32(irrigar)
    salvar_log_decisao(previsao_demo, irrigar)


def executar_visualizar_logs():
    mostrar_descritivo('logs')
    visualizar_logs()


# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

def main():
    """Função principal do sistema"""
    global CIDADE, PAIS

    print("\n" + "="*60)
    print("🌾 FarmTech Solutions - Sistema de Irrigação Inteligente")
    print("   Opcional 1: Integração com API Meteorológica")
    print("="*60)
    print(f"📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"📍 Localização: {CIDADE}, {PAIS}")
    print("="*60 + "\n")

    # Suporte a argumentos de linha de comando (modo, cidade, país)
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--mode', choices=['api', 'demo', 'logs'], help='Seleciona o modo de execução')
    parser.add_argument('--city', help='Sobrescreve a cidade do script')
    parser.add_argument('--country', help='Sobrescreve o país do script (ex.: BR)')
    try:
        args, _ = parser.parse_known_args()
    except SystemExit:
        # Em ambientes sem CLI, ignore erros de parser
        args = argparse.Namespace(mode=None, city=None, country=None)

    if args.city:
        CIDADE = args.city
    if args.country:
        PAIS = args.country

    def exec_mode(mode: str):
        if mode == 'api':
            executar_modo_api()
        elif mode == 'demo':
            executar_modo_demo()
        elif mode == 'logs':
            executar_visualizar_logs()

    if args.mode:
        # Execução direta por argumento
        exec_mode(args.mode)
    elif sys.stdin.isatty():
        # Modo interativo com menu
        while True:
            print_menu()
            escolha = input("Selecione uma opção (1-4): ").strip()
            if escolha == '1':
                exec_mode('api')
            elif escolha == '2':
                exec_mode('demo')
            elif escolha == '3':
                exec_mode('logs')
            elif escolha == '4':
                break
            else:
                print("Opção inválida. Tente novamente.")
    else:
        # Fallback não interativo: comportamento original
        if API_KEY == "SUA_CHAVE_AQUI":
            executar_modo_demo()
        else:
            executar_modo_api()

    print("\n" + "="*60)
    print("✅ Processo concluído!")
    print("="*60 + "\n")


# ============================================================================
# EXECUÇÃO
# ============================================================================

if __name__ == "__main__":
    main()


# ============================================================================
# INTEGRAÇÃO COM ESP32 (Código C++ correspondente)
# ============================================================================

"""
Para receber comandos no ESP32, adicione no FarmTech.ino:

void setup() {
    Serial.begin(115200);
    // ... resto do setup
}

void loop() {
    // Verificar comandos da API Python
    if (Serial.available() > 0) {
        String comando = Serial.readStringUntil('\n');
        comando.trim();
        
        if (comando == "IRRIGAR_OFF") {
            // Forçar desligamento da irrigação
            digitalWrite(RELE_PIN, LOW);
            releLigado = false;
            Serial.println("✅ Irrigação SUSPENSA por previsão de chuva");
        }
        else if (comando == "IRRIGAR_ON") {
            // Permitir irrigação normal
            Serial.println("✅ Irrigação liberada (sem chuva prevista)");
        }
    }
    
    // ... resto do loop
}
"""

# ============================================================================
# BENEFÍCIOS DA INTEGRAÇÃO
# ============================================================================

"""
✅ ECONOMIA DE ÁGUA
   - Suspende irrigação antes da chuva
   - Reduz desperdício de recursos hídricos
   - Diminui custos operacionais

✅ SUSTENTABILIDADE
   - Uso inteligente de recursos naturais
   - Redução da pegada hídrica
   - Alinhamento com práticas ESG

✅ AUTOMAÇÃO
   - Decisão baseada em dados reais
   - Sem necessidade de intervenção manual
   - Integração com sistema existente

✅ ESCALABILIDADE
   - Fácil adaptação para múltiplas fazendas
   - Integração com outros sensores
   - Base para Machine Learning futuro
"""
