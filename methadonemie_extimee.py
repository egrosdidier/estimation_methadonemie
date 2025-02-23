import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def estimate_methadonemie(dose, delay, days_consecutive, weight, half_life=36):
    """
    Estime la méthadonémie en fonction de la posologie, du délai depuis la dernière prise, du nombre de jours consécutifs et du poids du patient.
    """
    volume_distribution = 4  # L/kg, valeur clinique moyenne
    
    # Ajustement du facteur d'accumulation pour éviter la surestimation
    if days_consecutive <= 14:
        accumulation_factor = 1 / (1 - np.exp(-0.693 * days_consecutive / half_life))
    else:
        accumulation_factor = 3.5  # Facteur d'équilibre basé sur la clinique pour éviter une surestimation
    
    # Calcul de la concentration attendue
    clearance = (0.693 / half_life) * (volume_distribution * weight)
    concentration = (dose * accumulation_factor / (volume_distribution * weight)) * np.exp(-0.693 * delay / half_life)
    
    return max(min(concentration * 1000, 1200), 0)  # Conversion en ng/mL et limitation à 1200 ng/mL max

# Interface Streamlit
st.title("Estimation de la Méthadonémie")

dose = st.number_input("Dose quotidienne de méthadone (mg)", min_value=1, max_value=500, value=60)
delay = st.number_input("Délai depuis la dernière prise (h)", min_value=1, max_value=48, value=12)
days_consecutive = st.number_input("Nombre de jours consécutifs de prise", min_value=1, max_value=30, value=7)
weight = st.number_input("Poids du patient (kg)", min_value=30, max_value=150, value=70)

if st.button("Estimer"):
    estimated_methadonemie = estimate_methadonemie(dose, delay, days_consecutive, weight)
    st.write(f"**Méthadonémie estimée**: {estimated_methadonemie:.2f} ng/mL")
    
    # Tracer la courbe d'évolution
    time = np.linspace(0, 48, 100)
    concentrations = [estimate_methadonemie(dose, t, days_consecutive, weight) for t in time]
    
    fig, ax = plt.subplots()
    ax.plot(time, concentrations, label="Évolution de la Méthadonémie", color='blue')
    ax.axhline(100, color='green', linestyle='--', label='Seuil bas (100 ng/mL)')
    ax.axhline(400, color='red', linestyle='--', label='Zone thérapeutique (400 ng/mL)')
    ax.set_ylim(0, 1200)  # Augmenter la limite supérieure à 1200 ng/mL
    ax.axvline(delay, color='purple', linestyle='--', label='Moment du prélèvement')
    ax.set_xlabel("Temps depuis la dernière prise (h)")
    ax.set_ylabel("Méthadonémie (ng/mL)")
    ax.set_title("Estimation de la Méthadonémie en fonction du temps")
    ax.legend()
    st.pyplot(fig)
