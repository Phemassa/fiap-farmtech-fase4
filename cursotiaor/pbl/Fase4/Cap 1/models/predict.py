"""
FarmTech Solutions - Sistema de Previsão ML
==========================================
Carrega modelos treinados e faz previsões
"""

import joblib
import json
import numpy as np
from pathlib import Path

class FarmTechPredictor:
    """
    Classe para fazer previsões usando modelos treinados
    """
    
    def __init__(self, models_dir='models'):
        """
        Inicializa o predictor
        
        Args:
            models_dir: Diretório com modelos treinados
        """
        self.models_dir = Path(models_dir)
        self.models = {}
        self.metrics = {}
        self.feature_importance = {}
        
    def load_models(self):
        """Carrega todos os modelos disponíveis"""
        print(f"📁 Carregando modelos de {self.models_dir}...")
        
        # Procurar por arquivos .pkl
        model_files = list(self.models_dir.glob('*_model.pkl'))
        
        if not model_files:
            print("⚠️ Nenhum modelo encontrado. Execute o treinamento primeiro:")
            print("   python models/train_models.py")
            return False
        
        for model_file in model_files:
            target_name = model_file.stem.replace('_model', '')
            
            # Carregar modelo
            self.models[target_name] = joblib.load(model_file)
            print(f"✅ Modelo carregado: {target_name}")
            
            # Carregar métricas
            metrics_file = model_file.parent / f"{target_name}_metrics.json"
            if metrics_file.exists():
                with open(metrics_file) as f:
                    self.metrics[target_name] = json.load(f)
            
            # Carregar feature importance
            importance_file = model_file.parent / f"{target_name}_feature_importance.json"
            if importance_file.exists():
                with open(importance_file) as f:
                    self.feature_importance[target_name] = json.load(f)
        
        print(f"🎉 {len(self.models)} modelos carregados com sucesso!")
        return True
    
    def prepare_input(self, temperatura, umidade_solo, ph_solo,
                     nitrogenio_ok, fosforo_ok, potassio_ok,
                     cultura='banana'):
        """
        Prepara input para previsão
        
        Args:
            temperatura: Temperatura em °C
            umidade_solo: Umidade do solo em %
            ph_solo: pH do solo
            nitrogenio_ok: Se nitrogênio está adequado (bool)
            fosforo_ok: Se fósforo está adequado (bool)
            potassio_ok: Se potássio está adequado (bool)
            cultura: 'banana' ou 'milho'
        
        Returns:
            Array numpy com features preparadas
        """
        # Converter booleanos para int
        n_ok = 1 if nitrogenio_ok else 0
        p_ok = 1 if fosforo_ok else 0
        k_ok = 1 if potassio_ok else 0
        
        # One-hot encoding da cultura
        cultura_banana = 1 if cultura == 'banana' else 0
        cultura_milho = 1 if cultura == 'milho' else 0
        
        # Criar array de features
        features = np.array([
            temperatura,
            umidade_solo,
            ph_solo,
            n_ok,
            p_ok,
            k_ok,
            cultura_banana,
            cultura_milho
        ]).reshape(1, -1)
        
        return features
    
    def predict_volume_irrigacao(self, temperatura, umidade_solo, ph_solo,
                                 nitrogenio_ok, fosforo_ok, potassio_ok,
                                 cultura='banana'):
        """
        Prevê volume de irrigação necessário
        
        Returns:
            dict com previsão e métricas
        """
        if 'volume_irrigacao' not in self.models:
            print("❌ Modelo de volume de irrigação não encontrado")
            return None
        
        # Preparar input
        X = self.prepare_input(
            temperatura, umidade_solo, ph_solo,
            nitrogenio_ok, fosforo_ok, potassio_ok,
            cultura
        )
        
        # Fazer previsão
        volume = self.models['volume_irrigacao'].predict(X)[0]
        
        # Garantir que volume não seja negativo
        volume = max(0, volume)
        
        result = {
            'volume_litros': round(volume, 2),
            'model_metrics': self.metrics.get('volume_irrigacao', {}),
            'confidence': self._calculate_confidence(volume, 'volume_irrigacao')
        }
        
        return result
    
    def predict_rendimento(self, temperatura, umidade_solo, ph_solo,
                          nitrogenio_ok, fosforo_ok, potassio_ok,
                          cultura='banana'):
        """
        Prevê rendimento da cultura
        
        Returns:
            dict com previsão e métricas
        """
        if 'rendimento_estimado' not in self.models:
            print("❌ Modelo de rendimento não encontrado")
            return None
        
        # Preparar input
        X = self.prepare_input(
            temperatura, umidade_solo, ph_solo,
            nitrogenio_ok, fosforo_ok, potassio_ok,
            cultura
        )
        
        # Fazer previsão
        rendimento = self.models['rendimento_estimado'].predict(X)[0]
        
        result = {
            'rendimento_kg_ha': round(rendimento, 2),
            'model_metrics': self.metrics.get('rendimento_estimado', {}),
            'confidence': self._calculate_confidence(rendimento, 'rendimento_estimado')
        }
        
        return result
    
    def predict_all(self, temperatura, umidade_solo, ph_solo,
                   nitrogenio_ok, fosforo_ok, potassio_ok,
                   cultura='banana'):
        """
        Faz todas as previsões disponíveis
        
        Returns:
            dict com todas as previsões
        """
        results = {
            'inputs': {
                'temperatura': temperatura,
                'umidade_solo': umidade_solo,
                'ph_solo': ph_solo,
                'nitrogenio_ok': nitrogenio_ok,
                'fosforo_ok': fosforo_ok,
                'potassio_ok': potassio_ok,
                'cultura': cultura
            },
            'predictions': {}
        }
        
        # Volume de irrigação
        vol_pred = self.predict_volume_irrigacao(
            temperatura, umidade_solo, ph_solo,
            nitrogenio_ok, fosforo_ok, potassio_ok,
            cultura
        )
        if vol_pred:
            results['predictions']['volume_irrigacao'] = vol_pred
        
        # Rendimento
        rend_pred = self.predict_rendimento(
            temperatura, umidade_solo, ph_solo,
            nitrogenio_ok, fosforo_ok, potassio_ok,
            cultura
        )
        if rend_pred:
            results['predictions']['rendimento'] = rend_pred
        
        # Calcular dosagens NPK recomendadas
        results['predictions']['dosagens_npk'] = self._calculate_npk_dosages(
            nitrogenio_ok, fosforo_ok, potassio_ok, cultura
        )
        
        return results
    
    def _calculate_confidence(self, prediction, model_name):
        """Calcula nível de confiança da previsão"""
        if model_name not in self.metrics:
            return 0.5
        
        # Usar R² como proxy de confiança
        r2 = self.metrics[model_name].get('test', {}).get('r2', 0.5)
        
        # Converter para percentual 0-100
        confidence = max(0, min(100, r2 * 100))
        
        return round(confidence, 1)
    
    def _calculate_npk_dosages(self, n_ok, p_ok, k_ok, cultura):
        """Calcula dosagens NPK recomendadas"""
        # Valores de referência (g/m²) - baseados em EMBRAPA
        if cultura == 'banana':
            n_target = 15
            p_target = 10
            k_target = 20
        else:  # milho
            n_target = 12
            p_target = 8
            k_target = 10
        
        dosagens = {
            'nitrogenio_g_m2': 0 if n_ok else n_target,
            'fosforo_g_m2': 0 if p_ok else p_target,
            'potassio_g_m2': 0 if k_ok else k_target,
            'total_g_m2': 0
        }
        
        dosagens['total_g_m2'] = (
            dosagens['nitrogenio_g_m2'] +
            dosagens['fosforo_g_m2'] +
            dosagens['potassio_g_m2']
        )
        
        return dosagens
    
    def get_model_info(self):
        """Retorna informações sobre os modelos carregados"""
        info = {
            'models_loaded': list(self.models.keys()),
            'model_details': {}
        }
        
        for model_name, model in self.models.items():
            details = {
                'type': type(model).__name__,
                'metrics': self.metrics.get(model_name, {})
            }
            
            # Feature importance se disponível
            if model_name in self.feature_importance:
                details['feature_importance'] = self.feature_importance[model_name]
            
            info['model_details'][model_name] = details
        
        return info


def demo():
    """Demonstração de uso"""
    print("=" * 60)
    print("🌾 FarmTech Solutions - Demo de Previsão ML")
    print("=" * 60)
    
    # Inicializar predictor
    predictor = FarmTechPredictor('models')
    
    # Carregar modelos
    if not predictor.load_models():
        return
    
    print("\n" + "=" * 60)
    print("📊 Informações dos Modelos:")
    print("=" * 60)
    
    info = predictor.get_model_info()
    for model_name, details in info['model_details'].items():
        print(f"\n🤖 {model_name}:")
        print(f"   Tipo: {details['type']}")
        if 'test' in details['metrics']:
            print(f"   R²: {details['metrics']['test']['r2']:.4f}")
            print(f"   MAE: {details['metrics']['test']['mae']:.4f}")
    
    # Exemplo de previsão
    print("\n" + "=" * 60)
    print("🔮 Exemplo de Previsão:")
    print("=" * 60)
    
    print("\n📝 Cenário: Solo seco, NPK insuficiente")
    print("   Temperatura: 28°C")
    print("   Umidade: 35%")
    print("   pH: 6.5")
    print("   NPK: N=Sim, P=Não, K=Não")
    print("   Cultura: Banana")
    
    results = predictor.predict_all(
        temperatura=28,
        umidade_solo=35,
        ph_solo=6.5,
        nitrogenio_ok=True,
        fosforo_ok=False,
        potassio_ok=False,
        cultura='banana'
    )
    
    print("\n📊 Resultados:")
    if 'volume_irrigacao' in results['predictions']:
        vol = results['predictions']['volume_irrigacao']
        print(f"\n💧 Volume de Irrigação: {vol['volume_litros']} L/m²")
        print(f"   Confiança: {vol['confidence']}%")
    
    if 'rendimento' in results['predictions']:
        rend = results['predictions']['rendimento']
        print(f"\n🌾 Rendimento Estimado: {rend['rendimento_kg_ha']:,.0f} kg/ha")
        print(f"   Confiança: {rend['confidence']}%")
    
    if 'dosagens_npk' in results['predictions']:
        npk = results['predictions']['dosagens_npk']
        print(f"\n🧪 Dosagens NPK Recomendadas:")
        print(f"   Nitrogênio: {npk['nitrogenio_g_m2']} g/m²")
        print(f"   Fósforo: {npk['fosforo_g_m2']} g/m²")
        print(f"   Potássio: {npk['potassio_g_m2']} g/m²")
        print(f"   Total: {npk['total_g_m2']} g/m²")
    
    print("\n" + "=" * 60)
    print("✅ Demo concluída!")
    print("=" * 60)


if __name__ == "__main__":
    demo()