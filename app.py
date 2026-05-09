# app.py
import streamlit as st
from logic.sequence_processor import analyze_sequence

st.set_page_config(
    page_title="Genetic Sequence Analyzer",
    page_icon="🧬",
    layout="centered"
)

st.title("🧬 Genetic Sequence Analyzer")
st.markdown("Analyze DNA or RNA sequences using the **Central Dogma** of molecular biology.")
st.divider()

# --- Input ---
sequence_input = st.text_area(
    "Paste your Nucleotide Sequence below (A, T, C, G for DNA / A, U, C, G for RNA):",
    height=150,
    placeholder="e.g. ATGCTTACG"
)

col1, col2 = st.columns(2)
analyze_btn = col1.button("🔍 Analyze")
clear_btn = col2.button("🗑️ Clear")

if clear_btn:
    st.rerun()

st.divider()

# --- Analysis ---
if analyze_btn:
    if not sequence_input.strip():
        st.warning("⚠️ Please enter a nucleotide sequence first.")
    else:
        try:
            result = analyze_sequence(sequence_input)

            st.subheader("📊 Analysis Results")

            # Sequence Type
            st.info(f"**Sequence Type:** {result['type']}")

            # Strands
            st.markdown("### 🔗 Strand Information")
            st.markdown(f"**Input Sequence:** `{result['sequence']}`")
            st.markdown(f"**{'mRNA' if result['type'] == 'DNA' else 'DNA Template'} (Transcribed):** `{result['transcribed']}`")
            st.markdown(f"**Complement:** `{result['complement']}`")
            st.markdown(f"**Reverse Complement:** `{result['reverse_complement']}`")

            # mRNA
            st.markdown("### 🧪 mRNA Strand")
            st.markdown(f"`{result['mrna']}`")

            # Protein
            st.markdown("### 🔬 Protein Sequence")
            if result['protein_1letter']:
                st.success(f"**1-Letter Code:** {result['protein_1letter']}")
                st.success(f"**3-Letter Code:** {result['protein_3letter']}")
            else:
                st.warning("No protein sequence produced — sequence may be too short or missing a start codon.")

        except ValueError as e:
            st.error(f"❌ Error: {e}")