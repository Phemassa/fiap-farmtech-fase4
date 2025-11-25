"""
FarmTech Solutions - Treinamento de Modelos ML
==============================================
Pipeline completo de treinamento para previsão de irrigação
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import json
from pathlib import Path
from datetime import datetime

class FarmTechModelTrainer:
    """
    Classe para treinamento de modelos de Machine Learning
    para previsão de volume de irrigação e rendimento de culturas
    """
    
    def __init__(self, data_path='sensor_data_banana.csv'):
        """
        Inicializa o trainer
        
        Args:
            data_path: Caminho para o arquivo CSV com dados de treinamento
        """
        self.data_path = data_path
        self.models = {}
        self.metrics = {}
        self.feature_importance = {}
        
    def load_data(self):
        """Carrega e prepara os dados"""
        print(f"📁 Carregando dados de {self.data_path}...")
        
        # Carregar CSV
        self.df = pd.read_csv(self.data_path)
        
        # Converter booleanos
        bool_cols = ['nitrogenio_ok', 'fosforo_ok', 'potassio_ok']
        for col in bool_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(int)
        
        print(f"✅ Carregados {len(self.df)} registros")
        print(f"📊 Colunas: {list(self.df.columns)}")
        
        return self.df
    
    def prepare_features(self, target='volume_irrigacao'):
        """
        Prepara features e target para treinamento
        
        Args:
            target: Nome da coluna target ('volume_irrigacao' ou 'rendimento_estimado')
        """
        print(f"\n🔧 Preparando features para target: {target}")
        
        # Definir features
        feature_cols = [
            'temperatura',
            'umidade_solo',
            'ph_solo',
            'nitrogenio_ok',
            'fosforo_ok',
            'potassio_ok'
        ]
        
        # Adicionar cultura como one-hot encoding se existir
        if 'cultura' in self.df.columns:
            self.df['cultura_banana'] = (self.df['cultura'] == 'banana').astype(int)
            self.df['cultura_milho'] = (self.df['cultura'] == 'milho').astype(int)
            feature_cols.extend(['cultura_banana', 'cultura_milho'])
        
        # Verificar se todas as features existem
        missing_cols = [col for col in feature_cols if col not in self.df.columns]
        if missing_cols:
            print(f"⚠️ Colunas faltando: {missing_cols}")
            feature_cols = [col for col in feature_cols if col in self.df.columns]
        
        # Verificar se target existe
        if target not in self.df.columns:
            raise ValueError(f"❌ Coluna target '{target}' não encontrada no dataset")
        
        # Remover linhas com valores nulos
        df_clean = self.df[feature_cols + [target]].dropna()
        
        print(f"✅ Features selecionadas: {feature_cols}")
        print(f"📊 Dataset limpo: {len(df_clean)} registros (removidos {len(self.df) - len(df_clean)} nulos)")
        
        # Separar X e y
        X = df_clean[feature_cols]
        y = df_clean[target]
        
        return X, y, feature_cols
    
    def train_models(self, X, y, target_name='volume_irrigacao'):
        """
        Treina múltiplos modelos e compara performance
        
        Args:
            X: Features
            y: Target
            target_name: Nome do target para salvar modelos
        """
        print(f"\n🤖 Treinando modelos para {target_name}...")
        
        # Split train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print(f"📊 Train: {len(X_train)} | Test: {len(X_test)}")
        
        # Definir modelos
        models_to_train = {
            'linear_regression': LinearRegression(),
            'random_forest': RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            ),
            'gradient_boosting': GradientBoostingRegressor(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=42
            )
        }
        
        results = {}
        
        # Treinar cada modelo
        for model_name, model in models_to_train.items():
            print(f"\n🔄 Treinando {model_name}...")
            
            # Treinar
            model.fit(X_train, y_train)
            
            # Fazer previsões
            y_pred_train = model.predict(X_train)
            y_pred_test = model.predict(X_test)
            
            # Calcular métricas
            metrics = {
                'train': {
                    'mae': mean_absolute_error(y_train, y_pred_train),
                    'mse': mean_squared_error(y_train, y_pred_train),
                    'rmse': np.sqrt(mean_squared_error(y_train, y_pred_train)),
                    'r2': r2_score(y_train, y_pred_train)
                },
                'test': {
                    'mae': mean_absolute_error(y_test, y_pred_test),
                    'mse': mean_squared_error(y_test, y_pred_test),
                    'rmse': np.sqrt(mean_squared_error(y_test, y_pred_test)),
                    'r2': r2_score(y_test, y_pred_test)
                }
            }
            
            # Cross-validation
            cv_scores = cross_val_score(
                model, X_train, y_train, 
                cv=5, scoring='r2', n_jobs=-1
            )
            metrics['cv_r2_mean'] = cv_scores.mean()
            metrics['cv_r2_std'] = cv_scores.std()
            
            # Salvar
            results[model_name] = {
                'model': model,
                'metrics': metrics
            }
            
            # Imprimir resultados
            print(f"  📊 Train R²: {metrics['train']['r2']:.4f}")
            print(f"  📊 Test R²: {metrics['test']['r2']:.4f}")
            print(f"  📊 CV R²: {metrics['cv_r2_mean']:.4f} ± {metrics['cv_r2_std']:.4f}")
            print(f"  📊 Test MAE: {metrics['test']['mae']:.4f}")
            print(f"  📊 Test RMSE: {metrics['test']['rmse']:.4f}")
        
        # Selecionar melhor modelo baseado em R² de teste
        best_model_name = max(
            results.keys(), 
            key=lambda k: results[k]['metrics']['test']['r2']
        )
        
        print(f"\n🏆 Melhor modelo: {best_model_name}")
        print(f"   R² Test: {results[best_model_name]['metrics']['test']['r2']:.4f}")
        
        # Salvar melhor modelo
        self.models[target_name] = results[best_model_name]['model']
        self.metrics[target_name] = results[best_model_name]['metrics']
        
        # Feature importance (se disponível)
        if hasattr(results[best_model_name]['model'], 'feature_importances_'):
            importance = results[best_model_name]['model'].feature_importances_
            self.feature_importance[target_name] = dict(zip(X.columns, importance))
            
            print(f"\n📊 Feature Importance:")
            for feat, imp in sorted(
                self.feature_importance[target_name].items(), 
                key=lambda x: x[1], 
                reverse=True
            ):
                print(f"   {feat}: {imp:.4f}")
        
        return results, best_model_name
    
    def save_models(self, output_dir='models'):
        """Salva modelos treinados e métricas"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        print(f"\n💾 Salvando modelos em {output_dir}...")
        
        for target_name, model in self.models.items():
            # Salvar modelo
            model_file = output_path / f"{target_name}_model.pkl"
            joblib.dump(model, model_file)
            print(f"✅ Modelo salvo: {model_file}")
            
            # Salvar métricas
            metrics_file = output_path / f"{target_name}_metrics.json"
            with open(metrics_file, 'w') as f:
                json.dump(self.metrics[target_name], f, indent=2)
            print(f"✅ Métricas salvas: {metrics_file}")
            
            # Salvar feature importance
            if target_name in self.feature_importance:
                importance_file = output_path / f"{target_name}_feature_importance.json"
                with open(importance_file, 'w') as f:
                    json.dump(self.feature_importance[target_name], f, indent=2)
                print(f"✅ Feature importance salva: {importance_file}")
        
        # Salvar metadados
        metadata = {
            'training_date': datetime.now().isoformat(),
            'data_source': self.data_path,
            'n_samples': len(self.df),
            'models': list(self.models.keys()),
            'best_metrics': {
                target: {
                    'test_r2': self.metrics[target]['test']['r2'],
                    'test_mae': self.metrics[target]['test']['mae'],
                    'test_rmse': self.metrics[target]['test']['rmse']
                }
                for target in self.models.keys()
            }
        }
        
        metadata_file = output_path / 'training_metadata.json'
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"✅ Metadados salvos: {metadata_file}")
        
        print(f"\n🎉 Treinamento concluído com sucesso!")
        
    def train_all(self):
        """Pipeline completo de treinamento"""
        print("=" * 60)
        print("🌾 FarmTech Solutions - Treinamento de Modelos ML")
        print("=" * 60)
        
        # Carregar dados
        self.load_data()
        
        # Treinar modelo de volume de irrigação
        if 'volume_irrigacao' in self.df.columns:
            X, y, features = self.prepare_features('volume_irrigacao')
            self.train_models(X, y, 'volume_irrigacao')
        
        # Treinar modelo de rendimento
        if 'rendimento_estimado' in self.df.columns:
            X, y, features = self.prepare_features('rendimento_estimado')
            self.train_models(X, y, 'rendimento_estimado')
        
        # Salvar modelos
        self.save_models()
        
        print("\n" + "=" * 60)
        print("✅ Pipeline de treinamento finalizado!")
        print("=" * 60)


def main():
    """Função principal"""
    import sys
    
    # Verificar argumentos
    if len(sys.argv) > 1:
        data_file = sys.argv[1]
    else:
        # Tentar banana primeiro, depois milho
        if Path('sensor_data_banana.csv').exists():
            data_file = 'sensor_data_banana.csv'
        elif Path('sensor_data_milho.csv').exists():
            data_file = 'sensor_data_milho.csv'
        else:
            print("❌ Erro: Nenhum arquivo de dados encontrado!")
            print("Execute primeiro: python generate_sensor_data.py")
            sys.exit(1)
    
    # Treinar modelos
    trainer = FarmTechModelTrainer(data_file)
    trainer.train_all()
    
    # Treinar também para outra cultura se existir
    other_culture = 'sensor_data_milho.csv' if 'banana' in data_file else 'sensor_data_banana.csv'
    if Path(other_culture).exists():
        print(f"\n🔄 Treinando também para {other_culture}...")
        trainer2 = FarmTechModelTrainer(other_culture)
        trainer2.train_all()


if __name__ == "__main__":
    main()