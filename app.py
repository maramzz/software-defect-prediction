
import streamlit as st
import pandas as pd
import joblib

# ==========================================
# 1. CONFIGURATION DE LA PAGE
# ==========================================

st.set_page_config(
    page_title="Détection des défauts logiciels",
    page_icon="🔍",
    layout="wide"
)

# ==========================================
# 2. CHARGEMENT DU MODELE
# ==========================================

@st.cache_resource
def load_model():
    return joblib.load("model.joblib")

model = load_model()

# ==========================================
# 3. VARIABLES DU MODELE
# ==========================================

FEATURES = [
    'loc', 'v(g)', 'ev(g)', 'iv(g)', 'n', 'v', 'l', 'd',
    'i', 'e', 'b', 't', 'lOCode', 'lOComment', 'lOBlank',
    'locCodeAndComment', 'uniq_Op', 'uniq_Opnd',
    'total_Op', 'total_Opnd', 'branchCount'
]

# ==========================================
# 4. EXEMPLES REELS DU DATASET JM1
# ==========================================

# Exemple 1 : module non défectueux (classe réelle = false)

EXAMPLE_NON_DEFECTUEUX = {
    'loc': 31.0,
    'v(g)': 9.0,
    'ev(g)': 6.0,
    'iv(g)': 3.0,
    'n': 120.0,
    'v': 610.5,
    'l': 0.04,
    'd': 25.88,
    'i': 23.59,
    'e': 15796.57,
    'b': 0.2,
    't': 877.59,
    'lOCode': 23.0,
    'lOComment': 1.0,
    'lOBlank': 5.0,
    'locCodeAndComment': 0.0,
    'uniq_Op': 18.0,
    'uniq_Opnd': 16.0,
    'total_Op': 74.0,
    'total_Opnd': 46.0,
    'branchCount': 17.0
}

# Exemple 2 : module défectueux (classe réelle = true)

EXAMPLE_DEFECTUEUX = {
    'loc': 39.0,
    'v(g)': 6.0,
    'ev(g)': 1.0,
    'iv(g)': 5.0,
    'n': 138.0,
    'v': 762.25,
    'l': 0.05,
    'd': 20.89,
    'i': 36.48,
    'e': 15925.61,
    'b': 0.25,
    't': 884.76,
    'lOCode': 35.0,
    'lOComment': 0.0,
    'lOBlank': 2.0,
    'locCodeAndComment': 0.0,
    'uniq_Op': 18.0,
    'uniq_Opnd': 28.0,
    'total_Op': 73.0,
    'total_Opnd': 65.0,
    'branchCount': 11.0
}

# ==========================================
# 5. TITRE ET DESCRIPTION
# ==========================================

st.title("🔍 Détection des défauts logiciels")

st.write(
    "Cette application utilise un modèle de Machine Learning "
    "pour prédire si un module logiciel contient des défauts."
)

st.divider()

st.subheader("Caractéristiques du module logiciel")

st.write(
    "Vous pouvez saisir les caractéristiques manuellement "
    "ou charger un exemple réel du dataset JM1."
)

# ==========================================
# 6. BOUTONS POUR CHARGER LES EXEMPLES
# ==========================================

col_example1, col_example2 = st.columns(2)

with col_example1:
    if st.button("📂 Charger un exemple non défectueux"):
        for feature in FEATURES:
            st.session_state[feature] = EXAMPLE_NON_DEFECTUEUX[feature]

with col_example2:
    if st.button("⚠️ Charger un exemple défectueux"):
        for feature in FEATURES:
            st.session_state[feature] = EXAMPLE_DEFECTUEUX[feature]

st.divider()

# ==========================================
# 7. FORMULAIRE DE SAISIE
# ==========================================

with st.form("prediction_form"):

    input_values = {}

    col1, col2 = st.columns(2)

    for index, feature in enumerate(FEATURES):

        with col1 if index % 2 == 0 else col2:

            input_values[feature] = st.number_input(
                feature,
                value=0.0,
                format="%.4f",
                key=feature
            )

    submitted = st.form_submit_button(
        "🔍 Analyser le module",
        use_container_width=True
    )

# ==========================================
# 8. PREDICTION
# ==========================================

if submitted:

    # Conversion des valeurs en DataFrame
    input_df = pd.DataFrame(
        [input_values],
        columns=FEATURES
    )

    # Prediction du modele
    prediction = model.predict(input_df)[0]

    st.divider()
    st.subheader("Résultat de la prédiction")

    if str(prediction).lower() == "true":

        st.error("⚠️ Le module est prédit comme DÉFECTUEUX.")

    else:

        st.success("✅ Le module est prédit comme NON DÉFECTUEUX.")

    # ======================================
    # 9. PROBABILITE DE DEFAUT
    # ======================================

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(input_df)[0]
        classes = list(model.classes_)

        if "true" in classes:

            defect_probability = probabilities[
                classes.index("true")
            ]

            st.write(
                f"Probabilité estimée de défaut : "
                f"**{defect_probability * 100:.2f}%**"
            )

# ==========================================
# 10. COMPARAISON DES DEUX EXEMPLES
# ==========================================

st.divider()
st.subheader("Comparaison des exemples testés")

st.write(
    "Comparaison entre les classes réelles et les prédictions "
    "obtenues avec le modèle."
)

# Prédictions des deux exemples
example1_df = pd.DataFrame(
    [EXAMPLE_NON_DEFECTUEUX],
    columns=FEATURES
)

example2_df = pd.DataFrame(
    [EXAMPLE_DEFECTUEUX],
    columns=FEATURES
)

prediction1 = str(model.predict(example1_df)[0]).lower()
prediction2 = str(model.predict(example2_df)[0]).lower()

# Création du tableau comparatif
comparison = pd.DataFrame({
    "Exemple": [
        "Exemple 1",
        "Exemple 2"
    ],
    "Classe réelle": [
        "Non défectueux (false)",
        "Défectueux (true)"
    ],
    "Classe prédite": [
        "Défectueux" if prediction1 == "true" else "Non défectueux",
        "Défectueux" if prediction2 == "true" else "Non défectueux"
    ],
    "Résultat": [
        "Correcte" if prediction1 == "false" else "Incorrecte",
        "Correcte" if prediction2 == "true" else "Incorrecte"
    ]
})

st.dataframe(
    comparison,
    use_container_width=True,
    hide_index=True
)

# Interprétation
if prediction1 == "false":
    st.success("Exemple 1 : le module non défectueux est correctement classé.")
else:
    st.warning("Exemple 1 : le module non défectueux est mal classé.")

if prediction2 == "false":
    st.error(
        "Exemple 2 : le défaut n'a pas été détecté. "
        "Il s'agit d'un faux négatif (False Negative)."
    )
else:
    st.success("Exemple 2 : le défaut a été correctement détecté.")
