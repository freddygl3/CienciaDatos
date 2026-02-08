
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Assuming 'metrics_df' is already created from the previous code block (calc_failed_stats logic)
# which contains 'label', 'impacto_tiempo_fallo', 'indice_bloqueo' and now we need 'chapter' back.

try:
    # --- Reconstrucción rápida de metrics_df con 'chapter' ---
    # (Si ya ejecutaste la celda anterior en el notebook, esto no sería necesario, 
    # pero lo incluyo para que este bloque sea independiente y funcional)
    
    # 1. Recuperar 'chapter' en el label
    metrics_df['chapter'] = metrics_df['label'].apply(lambda x: int(x.split('-')[0].replace('C', '')))
    
    # --- GRÁFICOS POR CAPÍTULO ---
    chapters = sorted(metrics_df['chapter'].unique())
    
    for cap in chapters:
        # Filtrar datos del capítulo
        cap_data = metrics_df[metrics_df['chapter'] == cap].copy()
        
        # Ordenar por índice de bloqueo para mejor visualización
        cap_data = cap_data.sort_values('indice_bloqueo', ascending=False)
        
        # Top 15 para no saturar el gráfico (opcional, ajusta según necesidad)
        cap_data_plot = cap_data.head(15) 
        
        # Configuración del plot dual
        fig, ax1 = plt.subplots(figsize=(14, 7))
        
        title = f"Análisis de Bloqueo y Tiempo - Capítulo {cap} (Top 15 Problemáticos)"
        ax1.set_title(title, fontsize=16, pad=20)
        
        # Eje X
        x = range(len(cap_data_plot))
        labels = cap_data_plot['label']
        
        # Gráfico de Barras: Índice de Bloqueo (Eje Y1 - Izquierdo)
        bars = ax1.bar(x, cap_data_plot['indice_bloqueo'], color='#e74c3c', startAt=0, alpha=0.7, label='Índice de Bloqueo (0-100)')
        ax1.set_xlabel('Artefacto', fontsize=12)
        ax1.set_ylabel('Índice de Bloqueo (Score)', fontsize=12, color='#c0392b')
        ax1.tick_params(axis='y', labelcolor='#c0392b')
        ax1.set_ylim(0, 100) # Escala fija para el índice
        ax1.set_xticks(x)
        ax1.set_xticklabels(labels, rotation=45, ha='right')
        
        # Eje Y2 - Derecho: Impacto de Tiempo (Línea)
        ax2 = ax1.twinx()
        line = ax2.plot(x, cap_data_plot['impacto_tiempo_fallo'], color='#2c3e50', marker='o', linewidth=2, linestyle='-', label='Impacto Tiempo Fallo (min)')
        ax2.set_ylabel('Impacto Tiempo (Minutos perdidos/usuario)', fontsize=12, color='#2c3e50')
        ax2.tick_params(axis='y', labelcolor='#2c3e50')
        ax2.set_ylim(0, cap_data_plot['impacto_tiempo_fallo'].max() * 1.2) # Margen superior
        
        # Leyenda combinada
        # lines_1, labels_1 = ax1.get_legend_handles_labels()
        # lines_2, labels_2 = ax2.get_legend_handles_labels()
        # ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')
        
        # Grid y Layout
        ax1.grid(axis='y', linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

except Exception as e:
    print(f"Error generando gráficos: {e}")
    # Fallback si metrics_df no existe en el contexto inmediato (para pruebas)
    print("Asegúrate de haber ejecutado la celda de cálculo de métricas (metrics_df) antes.")
