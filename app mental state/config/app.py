import streamlit as st
import pandas as pd
import numpy as np
import joblib
import re
import os
import matplotlib.pyplot as plt

# Configuração Visual
st.set_page_config(page_title="Synapsee - EEG Analyzer", layout="wide")
st.title("🧠 Monitor de Estado Mental e Engajamento")

@st.cache_resource
def load_assets():
    try:
        model = joblib.load('modelo_eeg_mlp.pkl')
        scaler = joblib.load('scaler_mlp.pkl')
        params = joblib.load('engagement_params.pkl')
        return model, scaler, params
    except Exception as e:
        st.error(f"Erro ao carregar modelos: {e}")
        return None, None, None

def aggregate_bands(df_raw):
    # Lógica de Agregação de Bandas (AUC / Soma)
    freq_bands = {'delta': (0.5, 4.0), 'theta': (4.0, 8.0), 'alpha': (8.0, 13.0), 'beta': (13.0, 30.0), 'gamma': (30.0, 100.0)}
    
    def parse_col(col):
        m = re.match(r'^freq_(\d+)_(\d+)$', col)
        return (float(m.group(1))/10.0, int(m.group(2))) if m else (None, None)

    band_df = pd.DataFrame(index=df_raw.index)
    all_freqs = [c for c in df_raw.columns if c.startswith('freq_')]

    for band, (f_min, f_max) in freq_bands.items():
        cols = [c for c in all_freqs if f_min < parse_col(c)[0] <= f_max]
        band_df[band] = df_raw[cols].sum(axis=1) if cols else 0.0
    return band_df

model, scaler, params = load_assets()

if model is None:
    st.error("⚠️ Arquivos do modelo não encontrados! Execute a célula de salvamento no Colab.")
else:
    uploaded_file = st.file_uploader("Upload do CSV (mental-state)", type="csv")

    if uploaded_file:
        df_input = pd.read_csv(uploaded_file)
        
        # 1. PREDICÃO
        X_to_pred = df_input[params['selected_features']]
        X_sc = scaler.transform(X_to_pred)
        preds = model.predict(X_sc)
        df_input['Label_Predito'] = preds

        # 2. CÁLCULO DAS BANDAS
        band_df = aggregate_bands(df_input)

        # 3. CÁLCULO DO SCORE (Alpha sensitivity / Boost)
        raw_ratio = band_df['beta'] / (band_df['alpha'])
        weighted_eng = raw_ratio * (1 + df_input['Label_Predito'])
        min_e, max_e = params['min_eng'], params['max_eng']
        norm_score = 100 * (weighted_eng - min_e) / (max_e - min_e)
        df_input['Engajamento_Raw'] = norm_score

        # 4. MÉDIA MÓVEL PARA SUAVIZAÇÃO
        # Janela de 5 pontos para reduzir ruído visual
        df_input['Engajamento_Suave'] = df_input['Engajamento_Raw'].rolling(window=20, min_periods=1).mean()

        # Dashboard
        label_map = {0.0: "Relaxado 😌", 1.0: "Neutro 😐", 2.0: "Focado 🚀"}
        df_input['Estado'] = df_input['Label_Predito'].map(label_map)

        c1, c2 = st.columns(2)
        with c1:
            estado_dominante = df_input['Estado'].value_counts().idxmax()
            st.metric("Estado Dominante", estado_dominante)
        with c2:
            st.metric("Engajamento Médio", f"{df_input['Engajamento_Suave'].mean():.1f}")

        st.subheader("Nível de Engajamento ao Longo do Tempo")
        # Exibindo os dois no mesmo gráfico para referência
        chart_data = df_input[['Engajamento_Raw', 'Engajamento_Suave']].rename(columns={
            'Engajamento_Raw': 'Engajamento',
            'Engajamento_Suave': 'Média Móvel'
        })
        st.line_chart(chart_data)

        st.write(f"### Tabela de Resultados ({len(df_input)} registros)")
        st.dataframe(df_input[['Estado', 'Engajamento_Suave']])
