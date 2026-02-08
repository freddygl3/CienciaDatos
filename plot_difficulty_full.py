
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

try:
    # --- RECONSTRUCCIÓN DEL DATAFRAME (Lógica consolidada para el script) ---
    # 1. Carga
    df = pd.read_csv("P20242_Inst_1_clean.csv")
    df['seconds'] = pd.to_numeric(df['seconds'], errors='coerce')
    df['minutes'] = df['seconds'] / 60
    df['label'] = ("C" + df['chapter'].astype(str) + "-P" + df['page'].astype(str) + "-" + df['artifact'].astype(str))

    # 2. Métricas
    total_users = df.groupby('label')['_idUser'].nunique().reset_index(name='total_usuarios')
    failures = df[df['validationArtifact'] == False].copy()
    failures_agg = failures.groupby('label').agg(
        total_fallos=('label', 'count'),
        tiempo_promedio_fallo=('minutes', 'mean')
    ).reset_index()
    
    metrics_df = pd.merge(total_users, failures_agg, on='label', how='left').fillna(0)
    metrics_df['tasa_fallo'] = metrics_df['total_fallos'] / metrics_df['total_usuarios']
    metrics_df['impacto_tiempo_fallo'] = metrics_df['tasa_fallo'] * metrics_df['tiempo_promedio_fallo']
    
    def min_max_scale(series):
        if series.max() == series.min(): return 0
        return (series - series.min()) / (series.max() - series.min())

    n_tasa = min_max_scale(metrics_df['tasa_fallo'])
    n_tiempo = min_max_scale(metrics_df['tiempo_promedio_fallo'])
    metrics_df['indice_bloqueo'] = (n_tasa * 0.5 + n_tiempo * 0.5) * 100
    
    # 3. Recuperar Capítulo
    metrics_df['chapter'] = metrics_df['label'].apply(lambda x: int(x.split('-')[0].replace('C', '')) )

    # --- PLOTTING ---
    chapters = sorted(metrics_df['chapter'].unique()) # Should be [0, 1]
    
    for cap in chapters:
        cap_data = metrics_df[metrics_df['chapter'] == cap].sort_values('indice_bloqueo', ascending=False).head(15)
        
        if cap_data.empty: continue

        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        # Eje Izquierdo (Barras - Índice)
        color_bar = '#e74c3c' # Rojo suave
        ax1.bar(cap_data['label'], cap_data['indice_bloqueo'], color=color_bar, alpha=0.6, label='Índice de Bloqueo (0-100)')
        ax1.set_xlabel('Artefacto', fontsize=12)
        ax1.set_ylabel('Índice de Bloqueo', color=color_bar, fontsize=12, fontweight='bold')
        ax1.tick_params(axis='y', labelcolor=color_bar)
        ax1.set_ylim(0, 100)
        ax1.set_xticklabels(cap_data['label'], rotation=45, ha='right')
        
        # Eje Derecho (Línea - Impacto Tiempo)
        ax2 = ax1.twinx()
        color_line = '#2c3e50' # Azul oscuro
        ax2.plot(cap_data['label'], cap_data['impacto_tiempo_fallo'], color=color_line, marker='o', linewidth=2, label='Impacto Tiempo (min)')
        ax2.set_ylabel('Impacto Tiempo (min perdidos/usuario)', color=color_line, fontsize=12, fontweight='bold')
        ax2.tick_params(axis='y', labelcolor=color_line)
        
        # Título y Grid
        plt.title(f'Capítulo {cap}: Top 15 Artefactos Críticos (Bloqueo vs. Tiempo)', fontsize=14, pad=15)
        ax1.grid(axis='y', linestyle=':', alpha=0.5)
        
        plt.tight_layout()
        plt.show()
        print(f"Gráfico para Capítulo {cap} generado correctamente.")

except Exception as e:
    print(f"Error: {e}")
