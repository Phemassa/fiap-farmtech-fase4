# FarmTech Solutions - Modelos de Machine Learning
## 🤖 Pipeline de Treinamento e Previsão

### 📋 Visão Geral

Sistema completo de Machine Learning para:
- **Previsão de Volume de Irrigação**: Baseado em condições climáticas e nutricionais
- **Estimativa de Rendimento**: Produtividade esperada por cultura
- **Recomendações NPK**: Dosagens personalizadas de fertilizantes

---

## 🚀 Guia Rápido

### 1. Gerar Dados de Treinamento
```bash
python generate_sensor_data.py
```
Isso cria:
- `sensor_data_banana.csv` (1000+ amostras)
- `sensor_data_milho.csv` (1000+ amostras)

### 2. Treinar Modelos
```bash
python models/train_models.py
```
Ou especificar arquivo:
```bash
python models/train_models.py sensor_data_banana.csv
```

### 3. Testar Previsões
```bash
python models/predict.py
```

---

## 📊 Arquitetura do Sistema

### Modelos Treinados

#### 1. **Linear Regression** (Baseline)
- Algoritmo: Regressão linear simples
- Uso: Modelo de referência para comparação
- Vantagens: Rápido, interpretável
- Desvantagens: Assume relações lineares

#### 2. **Random Forest** (Recomendado)
- Algoritmo: Ensemble de árvores de decisão
- Parâmetros: 100 estimadores, max_depth=10
- Vantagens: Captura não-linearidades, feature importance
- Desvantagens: Maior complexidade computacional

#### 3. **Gradient Boosting**
- Algoritmo: Boosting de árvores de decisão
- Parâmetros: 100 estimadores, learning_rate=0.1
- Vantagens: Alta acurácia, robustez
- Desvantagens: Sensível a overfitting

### Features Utilizadas

```python
features = [
    'temperatura',       # Temperatura em °C
    'umidade_solo',      # Umidade do solo em %
    'ph_solo',           # pH do solo
    'nitrogenio_ok',     # Nitrogênio adequado (0/1)
    'fosforo_ok',        # Fósforo adequado (0/1)
    'potassio_ok',       # Potássio adequado (0/1)
    'cultura_banana',    # One-hot: Cultura = banana
    'cultura_milho'      # One-hot: Cultura = milho
]
```

### Targets (Variáveis Alvo)

1. **volume_irrigacao**: Volume de água em L/m²
2. **rendimento_estimado**: Produtividade em kg/ha

---

## 📈 Métricas de Avaliação

### Métricas Calculadas

- **MAE (Mean Absolute Error)**: Erro médio absoluto
- **MSE (Mean Squared Error)**: Erro quadrático médio
- **RMSE (Root Mean Squared Error)**: Raiz do erro quadrático médio
- **R² (Coefficient of Determination)**: Coeficiente de determinação (0-1)
- **CV R²**: R² de validação cruzada (5-folds)

### Interpretação

| R² Score | Qualidade |
|----------|-----------|
| > 0.90   | Excelente |
| 0.80-0.90| Muito Bom |
| 0.70-0.80| Bom       |
| 0.60-0.70| Regular   |
| < 0.60   | Ruim      |

---

## 🔧 Uso Detalhado

### Classe `FarmTechModelTrainer`

```python
from models.train_models import FarmTechModelTrainer

# Inicializar
trainer = FarmTechModelTrainer('sensor_data_banana.csv')

# Carregar dados
trainer.load_data()

# Preparar features
X, y, feature_names = trainer.prepare_features('volume_irrigacao')

# Treinar modelos
results, best_model = trainer.train_models(X, y, 'volume_irrigacao')

# Salvar modelos
trainer.save_models('models')
```

### Classe `FarmTechPredictor`

```python
from models.predict import FarmTechPredictor

# Inicializar
predictor = FarmTechPredictor('models')

# Carregar modelos treinados
predictor.load_models()

# Fazer previsão
result = predictor.predict_all(
    temperatura=28.0,
    umidade_solo=45.0,
    ph_solo=6.5,
    nitrogenio_ok=True,
    fosforo_ok=False,
    potassio_ok=False,
    cultura='banana'
)

# Acessar resultados
volume = result['predictions']['volume_irrigacao']['volume_litros']
rendimento = result['predictions']['rendimento']['rendimento_kg_ha']
dosagens = result['predictions']['dosagens_npk']
```

---

## 📁 Arquivos Gerados

### Após Treinamento

```
models/
├── volume_irrigacao_model.pkl          # Modelo de volume
├── volume_irrigacao_metrics.json       # Métricas de performance
├── volume_irrigacao_feature_importance.json  # Importância features
├── rendimento_estimado_model.pkl       # Modelo de rendimento
├── rendimento_estimado_metrics.json
├── rendimento_estimado_feature_importance.json
└── training_metadata.json              # Metadados do treinamento
```

### Conteúdo dos Arquivos

#### `*_model.pkl`
Modelo treinado serializado com joblib. Pode ser carregado com:
```python
import joblib
model = joblib.load('models/volume_irrigacao_model.pkl')
```

#### `*_metrics.json`
```json
{
  "train": {
    "mae": 1.23,
    "mse": 2.45,
    "rmse": 1.56,
    "r2": 0.89
  },
  "test": {
    "mae": 1.45,
    "mse": 2.78,
    "rmse": 1.67,
    "r2": 0.87
  },
  "cv_r2_mean": 0.86,
  "cv_r2_std": 0.03
}
```

#### `*_feature_importance.json`
```json
{
  "umidade_solo": 0.45,
  "temperatura": 0.25,
  "ph_solo": 0.15,
  "potassio_ok": 0.08,
  "nitrogenio_ok": 0.04,
  "fosforo_ok": 0.02,
  "cultura_banana": 0.005,
  "cultura_milho": 0.005
}
```

---

## 🧪 Validação do Modelo

### Cross-Validation

Todos os modelos são avaliados com **5-fold cross-validation**:

```python
from sklearn.model_selection import cross_val_score

cv_scores = cross_val_score(
    model, X_train, y_train,
    cv=5, scoring='r2', n_jobs=-1
)

print(f"CV R²: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
```

### Train/Test Split

- **80% Training**: Treinar o modelo
- **20% Testing**: Avaliar performance

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

---

## 🎯 Casos de Uso

### 1. Previsão de Irrigação para Novos Dados

```python
predictor = FarmTechPredictor('models')
predictor.load_models()

# Cenário: Solo seco, temperatura alta
volume = predictor.predict_volume_irrigacao(
    temperatura=32,
    umidade_solo=30,
    ph_solo=6.5,
    nitrogenio_ok=True,
    fosforo_ok=True,
    potassio_ok=False,
    cultura='banana'
)

print(f"Volume recomendado: {volume['volume_litros']} L/m²")
print(f"Confiança: {volume['confidence']}%")
```

### 2. Estimativa de Rendimento

```python
rendimento = predictor.predict_rendimento(
    temperatura=25,
    umidade_solo=60,
    ph_solo=6.8,
    nitrogenio_ok=True,
    fosforo_ok=True,
    potassio_ok=True,
    cultura='milho'
)

print(f"Rendimento estimado: {rendimento['rendimento_kg_ha']:,.0f} kg/ha")
```

### 3. Análise de Feature Importance

```python
info = predictor.get_model_info()

importance = info['model_details']['volume_irrigacao']['feature_importance']

# Ordenar por importância
sorted_features = sorted(
    importance.items(), 
    key=lambda x: x[1], 
    reverse=True
)

print("Features mais importantes:")
for feat, imp in sorted_features:
    print(f"  {feat}: {imp:.4f}")
```

---

## 🔬 Experimentação

### Adicionar Novas Features

1. Editar `generate_sensor_data.py` para incluir novas colunas
2. Modificar `prepare_features()` em `train_models.py`
3. Retreinar modelos

Exemplo:
```python
# Adicionar velocidade do vento
feature_cols = [
    'temperatura',
    'umidade_solo',
    'ph_solo',
    'velocidade_vento',  # Nova feature
    'nitrogenio_ok',
    # ...
]
```

### Tunar Hiperparâmetros

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(
    RandomForestRegressor(),
    param_grid,
    cv=5,
    scoring='r2',
    n_jobs=-1
)

grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_
```

### Experimentar Novos Modelos

```python
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor

models_to_train = {
    'svm': SVR(kernel='rbf'),
    'neural_net': MLPRegressor(hidden_layers=(100, 50), max_iter=1000)
}
```

---

## 📊 Análise de Resultados

### Exemplo de Output do Treinamento

```
============================================================
🌾 FarmTech Solutions - Treinamento de Modelos ML
============================================================

📁 Carregando dados de sensor_data_banana.csv...
✅ Carregados 1200 registros
📊 Colunas: ['temperatura', 'umidade_solo', 'ph_solo', ...]

🔧 Preparando features para target: volume_irrigacao
✅ Features selecionadas: [8 features]
📊 Dataset limpo: 1200 registros

🤖 Treinando modelos para volume_irrigacao...
📊 Train: 960 | Test: 240

🔄 Treinando linear_regression...
  📊 Train R²: 0.8245
  📊 Test R²: 0.8123
  📊 CV R²: 0.8089 ± 0.0234
  📊 Test MAE: 1.456
  📊 Test RMSE: 1.897

🔄 Treinando random_forest...
  📊 Train R²: 0.9567
  📊 Test R²: 0.8892
  📊 CV R²: 0.8765 ± 0.0189
  📊 Test MAE: 1.234
  📊 Test RMSE: 1.678

🔄 Treinando gradient_boosting...
  📊 Train R²: 0.9234
  📊 Test R²: 0.8756
  📊 CV R²: 0.8654 ± 0.0212
  📊 Test MAE: 1.345
  📊 Test RMSE: 1.734

🏆 Melhor modelo: random_forest
   R² Test: 0.8892

📊 Feature Importance:
   umidade_solo: 0.4523
   temperatura: 0.2456
   ph_solo: 0.1234
   potassio_ok: 0.0789
   ...

💾 Salvando modelos em models...
✅ Modelo salvo: models/volume_irrigacao_model.pkl
✅ Métricas salvas: models/volume_irrigacao_metrics.json
✅ Feature importance salva: models/volume_irrigacao_feature_importance.json

🎉 Treinamento concluído com sucesso!
```

---

## ⚠️ Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'sklearn'"

**Solução**: Instalar scikit-learn
```bash
pip install scikit-learn==1.3.2
```

### Erro: "FileNotFoundError: sensor_data_banana.csv"

**Solução**: Gerar dados primeiro
```bash
python generate_sensor_data.py
```

### Modelo com R² baixo (< 0.60)

**Possíveis causas**:
1. Dados insuficientes (< 500 amostras)
2. Features não informativas
3. Modelo inadequado para o problema
4. Overfitting (R² train >> R² test)

**Soluções**:
- Gerar mais dados simulados
- Adicionar features relevantes
- Experimentar outros algoritmos
- Ajustar hiperparâmetros

### Overfitting Detectado

**Sintomas**: R² train > 0.95 e R² test < 0.70

**Soluções**:
```python
# Para Random Forest
RandomForestRegressor(
    max_depth=5,           # Reduzir profundidade
    min_samples_split=10,  # Aumentar mínimo de amostras
    min_samples_leaf=5     # Aumentar folhas mínimas
)

# Para Gradient Boosting
GradientBoostingRegressor(
    learning_rate=0.05,    # Reduzir taxa de aprendizado
    subsample=0.8,         # Usar subsample
    max_features='sqrt'    # Limitar features
)
```

---

## 📚 Referências Técnicas

### Scikit-Learn Documentation
- [Random Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html)
- [Gradient Boosting](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html)
- [Model Evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html)

### Papers & Artigos
- Breiman, L. (2001). Random Forests. Machine Learning.
- Friedman, J. H. (2001). Greedy Function Approximation: A Gradient Boosting Machine.

---

## 🎓 Pontuação FIAP

### PARTE 1: Coleta de Dados (✅ 100% Completo)
- Geração de dataset realístico
- Múltiplas culturas (banana, milho)
- 1000+ amostras por cultura
- Features relevantes (clima, solo, NPK)
- Targets definidos (volume, rendimento)

### PARTE 2: Análise e Modelagem (✅ 100% Completo)
- Treinamento de múltiplos modelos
- Validação cruzada (5-fold CV)
- Métricas completas (MAE, RMSE, R²)
- Feature importance analysis
- Seleção automática do melhor modelo
- Persistência de modelos treinados

---

## 👥 Autores

**FarmTech Solutions - Grupo 19**  
FIAP - Pós-Tech: Agronegócio e IA  
Fase 2 - Cap 1 - Janeiro 2025

---

**Última atualização**: Janeiro 2025