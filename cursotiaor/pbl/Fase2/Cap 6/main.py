"""
FarmTech Solutions - Sistema de Gestão Agrícola
Aplicação Principal com Menu Interativo

Autores: Grupo 59 - FIAP Fase 2
Data: Outubro 2025
"""

import json
import os
from datetime import datetime
from cultivo_manager import CultivoManager
from sensor_monitor import SensorMonitor
from irrigacao_controller import IrrigacaoController
from estoque_manager import EstoqueManager
from database import DatabaseOracle
from file_utils import FileUtils


class FarmTechApp:
    """Classe principal da aplicação FarmTech Solutions"""
    
    def __init__(self):
        """Inicializa os gerenciadores e configurações"""
        self.cultivo_mgr = CultivoManager()
        self.sensor_mon = SensorMonitor()
        self.irrigacao_ctrl = IrrigacaoController()
        self.estoque_mgr = EstoqueManager()
        self.database = DatabaseOracle()
        self.file_utils = FileUtils()
        
        # Garante que diretórios existam
        self._criar_diretorios()
        
        # Carrega dados iniciais
        self._carregar_dados_iniciais()
    
    def _criar_diretorios(self):
        """Cria estrutura de diretórios necessária"""
        diretorios = ['data', 'logs', 'sql', 'docs']
        for diretorio in diretorios:
            if not os.path.exists(diretorio):
                os.makedirs(diretorio)
                print(f"✅ Diretório '{diretorio}/' criado")
    
    def _carregar_dados_iniciais(self):
        """Carrega dados dos arquivos JSON"""
        try:
            self.cultivo_mgr.carregar_json()
            self.sensor_mon.carregar_json()
            self.irrigacao_ctrl.carregar_json()
            self.estoque_mgr.carregar_json()
            print("✅ Dados carregados com sucesso\n")
        except FileNotFoundError:
            print("⚠️  Arquivos JSON não encontrados. Iniciando com dados vazios.\n")
    
    def exibir_banner(self):
        """Exibe banner de boas-vindas"""
        print("\n" + "="*60)
        print("🌾 FarmTech Solutions - Sistema de Gestão Agrícola 🌾".center(60))
        print("="*60)
        print("Tecnologia Python para Agricultura de Precisão".center(60))
        print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}".center(60))
        print("="*60 + "\n")
    
    def exibir_menu_principal(self):
        """Exibe menu principal de opções"""
        print("\n" + "─"*60)
        print("📋 MENU PRINCIPAL")
        print("─"*60)
        print("1️⃣  - Cadastrar Cultivo")
        print("2️⃣  - Listar Cultivos")
        print("3️⃣  - Monitorar Sensores (Simular Leitura)")
        print("4️⃣  - Verificar Necessidade de Irrigação")
        print("5️⃣  - Histórico de Irrigações")
        print("6️⃣  - Gerenciar Estoque de Insumos")
        print("7️⃣  - Relatórios e Análises")
        print("8️⃣  - Exportar Dados para JSON")
        print("9️⃣  - Sincronizar com Oracle Database")
        print("0️⃣  - Sair")
        print("─"*60)
    
    def cadastrar_cultivo(self):
        """Menu para cadastrar novo cultivo"""
        print("\n" + "="*60)
        print("🌱 CADASTRO DE CULTIVO")
        print("="*60)
        
        try:
            nome = input("\n📝 Nome do cultivo: ").strip()
            if not nome:
                print("❌ Nome não pode ser vazio!")
                return
            
            print("\n📂 Tipos disponíveis:")
            print("   1 - BANANA (K crítico: 20 g/m²)")
            print("   2 - MILHO (N crítico: 12 g/m²)")
            print("   3 - OUTRO")
            tipo_opcao = input("Escolha o tipo: ").strip()
            
            tipos_map = {'1': 'BANANA', '2': 'MILHO', '3': 'OUTRO'}
            cultura_tipo = tipos_map.get(tipo_opcao, 'OUTRO')
            
            area = float(input("\n📏 Área (hectares): "))
            if area <= 0:
                print("❌ Área deve ser maior que zero!")
                return
            
            data_plantio = input("\n📅 Data de plantio (YYYY-MM-DD): ").strip()
            
            # NPK requisitos
            print("\n🧪 Requisitos de NPK (g/m²):")
            nitrogenio = float(input("   Nitrogênio (N): "))
            fosforo = float(input("   Fósforo (P): "))
            potassio = float(input("   Potássio (K): "))
            
            ph_ideal = float(input("\n🧪 pH ideal do solo: "))
            umidade_ideal = float(input("💧 Umidade ideal do solo (%): "))
            
            # Cria cultivo
            cultivo_id = self.cultivo_mgr.adicionar_cultivo(
                nome=nome,
                cultura_tipo=cultura_tipo,
                area_hectares=area,
                data_plantio=data_plantio,
                npk_requisitos={'nitrogenio': nitrogenio, 'fosforo': fosforo, 'potassio': potassio},
                ph_ideal=ph_ideal,
                umidade_ideal=umidade_ideal
            )
            
            print(f"\n✅ Cultivo '{nome}' cadastrado com sucesso! ID: {cultivo_id}")
            
        except ValueError as e:
            print(f"❌ Erro de validação: {e}")
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
    
    def listar_cultivos(self):
        """Exibe lista de todos os cultivos"""
        print("\n" + "="*60)
        print("📋 CULTIVOS CADASTRADOS")
        print("="*60)
        
        cultivos = self.cultivo_mgr.listar_cultivos()
        
        if not cultivos:
            print("\n⚠️  Nenhum cultivo cadastrado ainda.")
            return
        
        for cultivo in cultivos:
            print(f"\n🌱 ID: {cultivo['id']} | {cultivo['nome']}")
            print(f"   Tipo: {cultivo['cultura_tipo']}")
            print(f"   Área: {cultivo['area_hectares']} hectares")
            print(f"   Plantio: {cultivo['data_plantio']}")
            print(f"   NPK: N={cultivo['npk_requisitos']['nitrogenio']}g/m² | "
                  f"P={cultivo['npk_requisitos']['fosforo']}g/m² | "
                  f"K={cultivo['npk_requisitos']['potassio']}g/m²")
            print(f"   pH ideal: {cultivo['ph_ideal']} | Umidade ideal: {cultivo['umidade_ideal']}%")
    
    def simular_leitura_sensores(self):
        """Simula leitura de sensores para um cultivo"""
        print("\n" + "="*60)
        print("📊 MONITORAMENTO DE SENSORES")
        print("="*60)
        
        cultivos = self.cultivo_mgr.listar_cultivos()
        if not cultivos:
            print("\n⚠️  Cadastre um cultivo primeiro!")
            return
        
        print("\n📋 Cultivos disponíveis:")
        for c in cultivos:
            print(f"   {c['id']} - {c['nome']}")
        
        try:
            cultivo_id = int(input("\n🔢 ID do cultivo para monitorar: "))
            
            print("\n🌡️  Insira os valores dos sensores:")
            temperatura = float(input("   Temperatura (°C): "))
            umidade_ar = float(input("   Umidade do ar (%): "))
            ph = float(input("   pH do solo: "))
            
            print("\n🧪 Status dos nutrientes (NPK):")
            n_ok = input("   Nitrogênio adequado? (s/n): ").lower() == 's'
            p_ok = input("   Fósforo adequado? (s/n): ").lower() == 's'
            k_ok = input("   Potássio adequado? (s/n): ").lower() == 's'
            
            # Registra leitura
            leitura_id = self.sensor_mon.adicionar_leitura(
                cultivo_id=cultivo_id,
                temperatura=temperatura,
                umidade_ar=umidade_ar,
                ph=ph,
                npk_ok={'N': n_ok, 'P': p_ok, 'K': k_ok}
            )
            
            # Exibe resultado
            leitura = self.sensor_mon.obter_leitura(leitura_id)
            print(f"\n✅ Leitura registrada com sucesso! ID: {leitura_id}")
            print(f"\n📊 RESUMO DA LEITURA:")
            print(f"   🌡️  Temperatura: {leitura['temperatura']}°C")
            print(f"   💧 Umidade do ar: {leitura['umidade_ar']}%")
            print(f"   💦 Umidade do solo: {leitura['umidade_solo']}% (calculada)")
            print(f"   🧪 pH: {leitura['ph']}")
            print(f"   🧪 NPK: N={'✅' if n_ok else '❌'} | P={'✅' if p_ok else '❌'} | K={'✅' if k_ok else '❌'}")
            
        except ValueError as e:
            print(f"❌ Erro: {e}")
    
    def verificar_irrigacao(self):
        """Verifica necessidade de irrigação para um cultivo"""
        print("\n" + "="*60)
        print("💧 VERIFICAÇÃO DE IRRIGAÇÃO")
        print("="*60)
        
        cultivos = self.cultivo_mgr.listar_cultivos()
        if not cultivos:
            print("\n⚠️  Cadastre um cultivo primeiro!")
            return
        
        print("\n📋 Cultivos disponíveis:")
        for c in cultivos:
            print(f"   {c['id']} - {c['nome']}")
        
        try:
            cultivo_id = int(input("\n🔢 ID do cultivo: "))
            
            # Busca última leitura
            leitura = self.sensor_mon.obter_ultima_leitura(cultivo_id)
            if not leitura:
                print(f"❌ Nenhuma leitura encontrada para cultivo {cultivo_id}")
                return
            
            cultivo = self.cultivo_mgr.obter_cultivo(cultivo_id)
            
            # Decide irrigação
            resultado = self.irrigacao_ctrl.decidir_irrigacao(cultivo, leitura)
            
            print(f"\n📊 ANÁLISE DE IRRIGAÇÃO:")
            print(f"   Cultivo: {cultivo['nome']}")
            print(f"   Timestamp: {leitura['timestamp']}")
            print(f"   Umidade solo: {leitura['umidade_solo']}%")
            print(f"   Temperatura: {leitura['temperatura']}°C")
            print(f"   pH: {leitura['ph']}")
            
            if resultado['deve_irrigar']:
                print(f"\n💧💧💧 IRRIGAÇÃO NECESSÁRIA")
                print(f"   Motivo: {resultado['motivo']}")
                
                # Registra irrigação
                self.irrigacao_ctrl.registrar_irrigacao(
                    cultivo_id=cultivo_id,
                    leitura_id=leitura['id'],
                    acionado=True,
                    motivo=resultado['motivo']
                )
                print("   ✅ Irrigação registrada no histórico")
            else:
                print(f"\n⏸️⏸️⏸️ IRRIGAÇÃO DESNECESSÁRIA")
                print(f"   Motivo: {resultado['motivo']}")
                
                # Registra decisão de não irrigar
                self.irrigacao_ctrl.registrar_irrigacao(
                    cultivo_id=cultivo_id,
                    leitura_id=leitura['id'],
                    acionado=False,
                    motivo=resultado['motivo']
                )
        
        except ValueError as e:
            print(f"❌ Erro: {e}")
    
    def exibir_historico_irrigacoes(self):
        """Exibe histórico de irrigações"""
        print("\n" + "="*60)
        print("📜 HISTÓRICO DE IRRIGAÇÕES")
        print("="*60)
        
        cultivos = self.cultivo_mgr.listar_cultivos()
        if not cultivos:
            print("\n⚠️  Cadastre um cultivo primeiro!")
            return
        
        print("\n📋 Cultivos disponíveis:")
        for c in cultivos:
            print(f"   {c['id']} - {c['nome']}")
        print("   0 - Todos")
        
        try:
            cultivo_id = int(input("\n🔢 ID do cultivo (0 para todos): "))
            
            if cultivo_id == 0:
                irrigacoes = self.irrigacao_ctrl.listar_irrigacoes()
            else:
                irrigacoes = self.irrigacao_ctrl.obter_irrigacoes_cultivo(cultivo_id)
            
            if not irrigacoes:
                print("\n⚠️  Nenhuma irrigação registrada ainda.")
                return
            
            print(f"\n📊 Total de registros: {len(irrigacoes)}")
            
            for irr in irrigacoes[-10:]:  # Últimas 10
                status = "💧 LIGADA" if irr['acionado'] else "⏸️  DESLIGADA"
                print(f"\n{status} | {irr['timestamp']}")
                print(f"   Cultivo ID: {irr['cultivo_id']}")
                print(f"   Motivo: {irr['motivo']}")
        
        except ValueError as e:
            print(f"❌ Erro: {e}")
    
    def gerenciar_estoque(self):
        """Menu de gerenciamento de estoque"""
        print("\n" + "="*60)
        print("📦 GERENCIAMENTO DE ESTOQUE")
        print("="*60)
        print("\n1 - Adicionar produto")
        print("2 - Listar estoque")
        print("3 - Registrar aplicação")
        print("4 - Verificar alertas")
        print("0 - Voltar")
        
        opcao = input("\nEscolha: ").strip()
        
        if opcao == '1':
            self._adicionar_produto_estoque()
        elif opcao == '2':
            self._listar_estoque()
        elif opcao == '3':
            self._registrar_aplicacao()
        elif opcao == '4':
            self._verificar_alertas_estoque()
    
    def _adicionar_produto_estoque(self):
        """Adiciona produto ao estoque"""
        try:
            produto = input("\n📝 Nome do produto: ").strip()
            print("\n📂 Tipo: 1-Fertilizante | 2-Defensivo | 3-Sementes | 4-Outro")
            tipo_opcao = input("Escolha: ").strip()
            tipos = {'1': 'fertilizante', '2': 'defensivo', '3': 'sementes', '4': 'outro'}
            tipo = tipos.get(tipo_opcao, 'outro')
            
            quantidade = float(input("\n⚖️  Quantidade (kg ou L): "))
            data_compra = input("📅 Data de compra (YYYY-MM-DD): ").strip()
            validade = input("📅 Validade (YYYY-MM-DD): ").strip()
            
            self.estoque_mgr.adicionar_produto(produto, tipo, quantidade, data_compra, validade)
            print(f"\n✅ Produto '{produto}' adicionado ao estoque!")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def _listar_estoque(self):
        """Lista produtos em estoque"""
        produtos = self.estoque_mgr.listar_estoque()
        
        if not produtos:
            print("\n⚠️  Estoque vazio.")
            return
        
        print(f"\n📦 ESTOQUE ATUAL ({len(produtos)} produtos)")
        for prod in produtos:
            print(f"\n📦 {prod['produto']}")
            print(f"   Tipo: {prod['tipo']}")
            print(f"   Quantidade: {prod['quantidade_kg']:.2f} kg/L")
            print(f"   Compra: {prod['data_compra']} | Validade: {prod['validade']}")
    
    def _registrar_aplicacao(self):
        """Registra aplicação de produto"""
        try:
            produtos = self.estoque_mgr.listar_estoque()
            if not produtos:
                print("\n⚠️  Estoque vazio.")
                return
            
            print("\n📦 Produtos disponíveis:")
            for i, p in enumerate(produtos):
                print(f"   {i} - {p['produto']} ({p['quantidade_kg']:.2f} kg/L)")
            
            idx = int(input("\n🔢 Índice do produto: "))
            quantidade = float(input("⚖️  Quantidade aplicada (kg ou L): "))
            
            self.estoque_mgr.registrar_aplicacao(idx, quantidade)
            print(f"\n✅ Aplicação registrada! Novo saldo: {produtos[idx]['quantidade_kg']:.2f} kg/L")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def _verificar_alertas_estoque(self):
        """Verifica alertas de estoque"""
        alertas = self.estoque_mgr.verificar_alertas()
        
        if not alertas:
            print("\n✅ Sem alertas no momento.")
            return
        
        print(f"\n⚠️  {len(alertas)} ALERTA(S) DETECTADO(S):")
        for alerta in alertas:
            print(f"   ⚠️  {alerta}")
    
    def gerar_relatorios(self):
        """Gera relatórios e análises"""
        print("\n" + "="*60)
        print("📊 RELATÓRIOS E ANÁLISES")
        print("="*60)
        print("\n1 - Relatório geral de cultivos")
        print("2 - Análise de irrigações")
        print("3 - Estatísticas de sensores")
        print("0 - Voltar")
        
        opcao = input("\nEscolha: ").strip()
        
        if opcao == '1':
            self._relatorio_cultivos()
        elif opcao == '2':
            self._analise_irrigacoes()
        elif opcao == '3':
            self._estatisticas_sensores()
    
    def _relatorio_cultivos(self):
        """Gera relatório geral de cultivos"""
        cultivos = self.cultivo_mgr.listar_cultivos()
        
        if not cultivos:
            print("\n⚠️  Nenhum cultivo cadastrado.")
            return
        
        print(f"\n╔{'═'*58}╗")
        print(f"║{'RELATÓRIO GERAL DE CULTIVOS'.center(58)}║")
        print(f"╠{'═'*58}╣")
        print(f"║ Total de cultivos: {len(cultivos):<43}║")
        
        area_total = sum(c['area_hectares'] for c in cultivos)
        print(f"║ Área total: {area_total:.2f} hectares{' '*(43-len(f'{area_total:.2f} hectares'))}║")
        print(f"╚{'═'*58}╝")
    
    def _analise_irrigacoes(self):
        """Analisa histórico de irrigações"""
        irrigacoes = self.irrigacao_ctrl.listar_irrigacoes()
        
        if not irrigacoes:
            print("\n⚠️  Nenhuma irrigação registrada.")
            return
        
        total = len(irrigacoes)
        acionadas = sum(1 for i in irrigacoes if i['acionado'])
        
        print(f"\n╔{'═'*58}╗")
        print(f"║{'ANÁLISE DE IRRIGAÇÕES'.center(58)}║")
        print(f"╠{'═'*58}╣")
        print(f"║ Total de verificações: {total:<40}║")
        print(f"║ Irrigações acionadas: {acionadas:<41}║")
        print(f"║ Irrigações evitadas: {total - acionadas:<42}║")
        taxa = (acionadas / total * 100) if total > 0 else 0
        print(f"║ Taxa de acionamento: {taxa:.1f}%{' '*(41-len(f'{taxa:.1f}%'))}║")
        print(f"╚{'═'*58}╝")
    
    def _estatisticas_sensores(self):
        """Gera estatísticas das leituras de sensores"""
        leituras = self.sensor_mon.listar_leituras()
        
        if not leituras:
            print("\n⚠️  Nenhuma leitura registrada.")
            return
        
        import statistics
        
        temperaturas = [l['temperatura'] for l in leituras]
        umidades = [l['umidade_solo'] for l in leituras]
        phs = [l['ph'] for l in leituras]
        
        print(f"\n╔{'═'*58}╗")
        print(f"║{'ESTATÍSTICAS DE SENSORES'.center(58)}║")
        print(f"╠{'═'*58}╣")
        print(f"║ Total de leituras: {len(leituras):<42}║")
        print(f"║ Temperatura média: {statistics.mean(temperaturas):.1f}°C ±{statistics.stdev(temperaturas) if len(temperaturas) > 1 else 0:.1f}{' '*29}║")
        print(f"║ Umidade média: {statistics.mean(umidades):.1f}% (min: {min(umidades):.1f}%, max: {max(umidades):.1f}%){' '*10}║")
        print(f"║ pH médio: {statistics.mean(phs):.2f}{' '*46}║")
        print(f"╚{'═'*58}╝")
    
    def exportar_json(self):
        """Exporta todos os dados para JSON"""
        print("\n" + "="*60)
        print("💾 EXPORTAR DADOS PARA JSON")
        print("="*60)
        
        try:
            self.cultivo_mgr.salvar_json()
            self.sensor_mon.salvar_json()
            self.irrigacao_ctrl.salvar_json()
            self.estoque_mgr.salvar_json()
            
            print("\n✅ Todos os dados exportados com sucesso!")
            print("   📁 data/cultivos.json")
            print("   📁 data/sensores.json")
            print("   📁 data/irrigacoes.json")
            print("   📁 data/estoque.json")
            
        except Exception as e:
            print(f"❌ Erro ao exportar: {e}")
    
    def sincronizar_oracle(self):
        """Sincroniza dados com Oracle Database"""
        print("\n" + "="*60)
        print("🔄 SINCRONIZAR COM ORACLE DATABASE")
        print("="*60)
        
        print("\n⚠️  Esta funcionalidade requer:")
        print("   1. Oracle Database instalado e configurado")
        print("   2. Biblioteca cx_Oracle instalada")
        print("   3. Credenciais em database.py")
        
        confirma = input("\nDeseja continuar? (s/n): ").lower()
        
        if confirma == 's':
            try:
                # Tenta conectar
                if not self.database.conectar():
                    print("❌ Falha na conexão. Verifique configurações.")
                    return
                
                # Sincroniza cultivos
                cultivos = self.cultivo_mgr.listar_cultivos()
                for cultivo in cultivos:
                    self.database.inserir_cultivo(cultivo)
                
                print(f"\n✅ {len(cultivos)} cultivos sincronizados!")
                
                self.database.desconectar()
                
            except Exception as e:
                print(f"❌ Erro na sincronização: {e}")
        else:
            print("\n⏸️  Sincronização cancelada.")
    
    def executar(self):
        """Loop principal da aplicação"""
        self.exibir_banner()
        
        while True:
            self.exibir_menu_principal()
            
            try:
                opcao = input("\n🔢 Escolha uma opção: ").strip()
                
                if opcao == '1':
                    self.cadastrar_cultivo()
                elif opcao == '2':
                    self.listar_cultivos()
                elif opcao == '3':
                    self.simular_leitura_sensores()
                elif opcao == '4':
                    self.verificar_irrigacao()
                elif opcao == '5':
                    self.exibir_historico_irrigacoes()
                elif opcao == '6':
                    self.gerenciar_estoque()
                elif opcao == '7':
                    self.gerar_relatorios()
                elif opcao == '8':
                    self.exportar_json()
                elif opcao == '9':
                    self.sincronizar_oracle()
                elif opcao == '0':
                    print("\n👋 Encerrando FarmTech Solutions...")
                    print("✅ Dados salvos automaticamente.")
                    print("🌾 Até logo!\n")
                    break
                else:
                    print("\n❌ Opção inválida! Tente novamente.")
                
                input("\n⏎ Pressione ENTER para continuar...")
                
            except KeyboardInterrupt:
                print("\n\n⚠️  Interrupção detectada. Salvando dados...")
                self.exportar_json()
                print("👋 Até logo!\n")
                break
            except Exception as e:
                print(f"\n❌ Erro inesperado: {e}")
                input("\n⏎ Pressione ENTER para continuar...")


def main():
    """Função principal"""
    app = FarmTechApp()
    app.executar()


if __name__ == "__main__":
    main()
