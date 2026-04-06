## 🟢 O Que Funcionou (Sucessos e Validações)

### 1. Inteligência de Dados e Curadoria de Features

- **Aproveitamento do Dataset:** A percepção precoce de que o `mental-state.csv` já continha um pré-processamento avançado permitiu focar na interpretação neurofisiológica em vez de limpeza básica.
    
- **Enriquecimento Científico:** A adição das bandas de frequência clássicas ($\alpha, \beta, \theta$) e o uso de **Boxplots** validaram que o modelo estava seguindo padrões biológicos reais, e não apenas ruído estatístico.
    
- **Seleção Estratégica:** A redução drástica de **988 para 50 features** (via _Feature Importance_ do Random Forest) foi um divisor de águas. Isso eliminou o _overfitting_, acelerou a inferência para milissegundos e manteve a relevância técnica (focando em _Eigenvalues_ e potências de banda).
    

### 2. Excelência em Modelagem

- **Robustez dos Algoritmos:** A transição de modelos simples para um **XGBoost** e uma **MLP (Rede Neural)** otimizada com _Batch Normalization_ e _Dropout_ elevou a acurácia de ~85% para **acima de 0.96**.
    
- **Otimização de Hiperparâmetros:** O uso de _GridSearchCV_ garantiu que os modelos operassem em seu potencial máximo, resultando em classificações sólidas entre os três estados mentais.
    

### 3. Inovação no Score de Engajamento

- **Refinamento de Métricas:** A adaptação de índices clássicos da literatura para uma fórmula personalizada baseada em `(1 + label) * Beta / Alpha` resolveu o problema de sobreposição das classes, gerando uma métrica contínua, normalizada e visualmente clara no dashboard.
    

### 4. Entrega de Produto

- **Dashboard Streamlit:** A implementação da interface foi bem-sucedida, fechando o ciclo do projeto ao permitir que um usuário faça o upload de um CSV e receba diagnósticos imediatos.
    

---

## 🔴 O Que Deu Errado (Aprendizados e Desafios)

- **Replicação de Estruturas Externas:** No início, tentar aplicar arquiteturas de outros projetos sem considerar a especificidade das quase 1.000 features do dataset limitou a acurácia inicial entre 80% e 85%. O modelo precisava de uma "dieta" de dados (seleção de features) para performar melhor.
    
- **Sensibilidade da MLP:** A versão inicial da Rede Neural (MLP) sem escalonamento de dados e sem ajuste de hiperparâmetros falhou em convergir, provando que o EEG exige uma preparação de dados (como _StandardScaling_) rigorosa.
    
- **Gargalo de Treino:** O XGBoost, embora excelente na predição, apresentou o maior tempo de treinamento, o que exigiu paciência e hardware durante a fase de ajuste.
    
- **Sobreposição de Scores Clássicos:** Inicialmente, o uso estrito de fórmulas da literatura sem adaptação resultou em scores que não diferenciavam bem as três classes, exigindo a criação de uma lógica de normalização própria.
    

---

## 🚀 O Que Faria Diferente (Visão de Futuro)

Se houvesse mais tempo ou maior volume de dados, os próximos passos seriam:

1. **Otimização Avançada:** Substituir o _GridSearch_ por técnicas de **Otimização Bayesiana (Optuna)** para explorar espaços de parâmetros ainda maiores de forma mais inteligente.
    
2. **Engajamento Dinâmico:** Desenvolver um score que se ajuste ao _baseline_ individual de cada usuário, considerando que cada cérebro possui potências de banda diferentes em repouso.
    
3. **Complexidade de Features:** Explorar métricas de **Conectividade Funcional** (como coerência entre canais) e entropia para captar a complexidade do sinal que estatísticas lineares podem perder.
    
4. **Análise de Erro Detalhada:** Implementar uma validação cruzada estratificada repetida para investigar exatamente quais sinais causam a confusão entre, por exemplo, "Neutro" e "Relaxado".

Ingestão e Normalização de Hardware

- **Resampling Universal:** Implementação de uma etapa de reamostragem (ex: fixar todos em 250Hz) para lidar com diferentes taxas de amostragem de dispositivos distintos.
    
- **Mapeamento de Montagens:** Criação de um de-para de canais (Sistema 10-20) para garantir que, independentemente do número de eletrodos, as features espaciais (como a Matriz de Covariância) fossem calculadas sobre regiões cerebrais equivalentes.

Pipeline de Limpeza Automática (Artifact Removal)

- **Filtragem Adaptativa:** Aplicação de filtros Notch (para ruído de rede elétrica 50/60Hz) e Band-pass (0.5Hz - 50Hz) automáticos.
    
- **Decomposição por ICA (Independent Component Analysis):** Implementação de um módulo para identificar e remover automaticamente artefatos oculares (piscadas) e miográficos (tensões musculares), que frequentemente "sujam" as bandas Beta e Gamma.
    
Motor de Extração de Features (O "Coração" do Sistema)

Para replicar a estrutura do `mental-state.csv`, eu desenvolveria um módulo modular que calcularia:

- **Janelas Deslizantes (Sliding Windows):** Com _overlap_ configurável (ex: 50%) para manter a continuidade temporal.
    
- **Extração Multi-Domínio:** 

	- **Tempo:** Momentos estatísticos e análise de sub-janelas (quartos e metades).
    
    - **Frequência:** Welch's Method para estimativa de PSD (Power Spectral Density) mais estável que a FFT pura.
        
    - **Espacial:** Cálculo de conectividade funcional em tempo real.