"""
Customer Support Ticket Classification & Duplicate Detection
Streamlit Application - NLP vs Deep Learning Comparison
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
from scipy.sparse import load_npz
from sklearn.metrics.pairwise import cosine_similarity
import tensorflow as tf
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import plotly.graph_objects as go
import plotly.express as px
import sys
import os

sys.path.append('.')
from preprocessing.text_cleaner import preprocess_pipeline, PreprocessingError

# Page configuration
st.set_page_config(
    page_title="Ticket Classification System",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
MAX_LENGTH = 100
NLP_THRESHOLD = 0.6
DL_THRESHOLD = 0.95

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main headers */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
        padding: 1rem 0;
    }
    
    .sub-header {
        font-size: 1.3rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Result boxes */
    .result-box-nlp {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 5px solid #1f77b4;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .result-box-dl {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border-left: 5px solid #4caf50;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Metric cards */
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.2rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #e0e0e0;
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Info boxes */
    .info-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* Success boxes */
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* Workflow steps */
    .workflow-step {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        height: 100%;
        transition: all 0.3s;
    }
    
    .workflow-step:hover {
        border-color: #1f77b4;
        box-shadow: 0 4px 12px rgba(31, 119, 180, 0.2);
    }
    
    /* Tables */
    .dataframe {
        font-size: 0.95rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1rem;
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background-color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Cache model loading
@st.cache_resource
def load_nlp_models():
    """Load NLP models"""
    with open('models/tfidf_vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    
    with open('models/nlp_classifier.pkl', 'rb') as f:
        classifier = pickle.load(f)
    
    with open('models/label_encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    
    train_vectors = load_npz('models/train_tfidf_vectors.npz')
    
    return vectorizer, classifier, label_encoder, train_vectors

@st.cache_resource
def load_dl_models():
    """Load DL models"""
    model = load_model('models/dl_model.h5')
    
    with open('models/tokenizer.pkl', 'rb') as f:
        tokenizer = pickle.load(f)
    
    with open('models/label_encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    
    # Build model to access layers
    _ = model(np.zeros((1, MAX_LENGTH)))
    
    # Create embedding model
    from tensorflow.keras.layers import Input
    input_layer = Input(shape=(MAX_LENGTH,))
    x = model.get_layer('embedding')(input_layer)
    lstm_output = model.get_layer('lstm')(x)
    embedding_model = Model(inputs=input_layer, outputs=lstm_output)
    
    return model, tokenizer, label_encoder, embedding_model

@st.cache_data
def load_train_embeddings():
    """Load training embeddings"""
    return np.load('models/train_embeddings_normalized.npy')

def preprocess_text(text):
    """Preprocess text using shared pipeline"""
    try:
        processed, metadata = preprocess_pipeline(text, return_string=True)
        return processed, None
    except PreprocessingError as e:
        return None, str(e)

def predict_nlp(text, vectorizer, classifier, label_encoder, train_vectors):
    """Predict using NLP pipeline"""
    processed, error = preprocess_text(text)
    if error:
        return None, error
    
    # Classification
    X_tfidf = vectorizer.transform([processed])
    y_pred = classifier.predict(X_tfidf)[0]
    y_proba = classifier.predict_proba(X_tfidf)[0]
    category = label_encoder.inverse_transform([y_pred])[0]
    confidence = y_proba[y_pred] * 100
    
    # Duplicate detection
    similarities = cosine_similarity(X_tfidf, train_vectors).flatten()
    top_3_indices = np.argsort(similarities)[-3:][::-1]
    top_3_similarities = similarities[top_3_indices]
    max_similarity = similarities.max()
    is_duplicate = 1 if max_similarity > NLP_THRESHOLD else 0
    
    return {
        'category': category,
        'confidence': confidence,
        'is_duplicate': is_duplicate,
        'max_similarity': max_similarity,
        'top_3_similarities': top_3_similarities.tolist(),
        'all_probabilities': {label_encoder.classes_[i]: y_proba[i] * 100 for i in range(len(y_proba))}
    }, None

def predict_dl(text, model, tokenizer, label_encoder, embedding_model, train_embeddings):
    """Predict using DL pipeline"""
    processed, error = preprocess_text(text)
    if error:
        return None, error
    
    # Convert to sequence
    sequence = tokenizer.texts_to_sequences([processed])
    padded = pad_sequences(sequence, maxlen=MAX_LENGTH, padding='post')
    
    # Classification
    y_proba = model.predict(padded, verbose=0)[0]
    y_pred = np.argmax(y_proba)
    category = label_encoder.inverse_transform([y_pred])[0]
    confidence = y_proba[y_pred] * 100
    
    # Duplicate detection
    test_embedding = embedding_model.predict(padded, verbose=0)
    test_embedding_norm = test_embedding / np.linalg.norm(test_embedding, axis=1, keepdims=True)
    similarities = cosine_similarity(test_embedding_norm, train_embeddings).flatten()
    max_similarity = similarities.max()
    is_duplicate = 1 if max_similarity > DL_THRESHOLD else 0
    
    return {
        'category': category,
        'confidence': float(confidence),
        'is_duplicate': is_duplicate,
        'max_similarity': float(max_similarity),
        'all_probabilities': {label_encoder.classes_[i]: float(y_proba[i]) * 100 for i in range(len(y_proba))}
    }, None

# Sidebar navigation
st.sidebar.title("🎫 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Home", "Analyze Ticket", "Batch Processing", "Model Comparison", "About"]
)

# Load models
try:
    with st.spinner("Loading models..."):
        nlp_vectorizer, nlp_classifier, nlp_label_encoder, nlp_train_vectors = load_nlp_models()
        dl_model, dl_tokenizer, dl_label_encoder, dl_embedding_model = load_dl_models()
        dl_train_embeddings = load_train_embeddings()
    models_loaded = True
except Exception as e:
    st.error(f"Error loading models: {str(e)}")
    models_loaded = False

# HOME PAGE
if page == "Home":
    st.markdown('<div class="main-header">🎫 Customer Support Ticket Classification System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Comparing NLP (TF-IDF) vs Deep Learning (LSTM) Approaches</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Problem and Solution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Problem Statement")
        st.markdown("""
        <div class="info-box">
        Customer support teams receive <strong>thousands of tickets daily</strong>. Manual classification and 
        duplicate detection is time-consuming and error-prone.
        <br><br>
        <strong>Key Challenges:</strong>
        <ul>
            <li>Categorizing tickets into billing, technical, delivery, or account issues</li>
            <li>Identifying duplicate tickets to avoid redundant work</li>
            <li>Processing tickets quickly and accurately</li>
            <li>Maintaining consistency across support agents</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### ✨ Our Solution")
        st.markdown("""
        <div class="success-box">
        We built <strong>two AI-powered systems</strong> to automate ticket classification and duplicate detection:
        <br><br>
        <strong>🔵 NLP Approach (TF-IDF + Logistic Regression):</strong>
        <ul>
            <li>Fast inference and low computational cost</li>
            <li>Interpretable features</li>
            <li>Excellent for classification tasks</li>
        </ul>
        <br>
        <strong>🟢 Deep Learning Approach (LSTM):</strong>
        <ul>
            <li>Captures semantic meaning and context</li>
            <li>Superior duplicate detection</li>
            <li>Learns complex patterns</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Workflow
    st.markdown("### 🔄 System Workflow")
    st.write("")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="workflow-step">
            <h2 style="color: #1f77b4;">📝</h2>
            <h4>1. Input</h4>
            <p>Customer ticket text</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="workflow-step">
            <h2 style="color: #1f77b4;">🧹</h2>
            <h4>2. Preprocessing</h4>
            <p>Clean & normalize text</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="workflow-step">
            <h2 style="color: #1f77b4;">🎯</h2>
            <h4>3. Classification</h4>
            <p>Predict category</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="workflow-step">
            <h2 style="color: #1f77b4;">🔄</h2>
            <h4>4. Duplicate Check</h4>
            <p>Find similar tickets</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key Results
    st.markdown("### 📊 Key Performance Results")
    st.write("")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Classification Accuracy",
            value="~90%",
            delta="Both models",
            delta_color="off"
        )
    
    with col2:
        st.metric(
            label="NLP Duplicate F1",
            value="10.31%",
            delta="Baseline"
        )
    
    with col3:
        st.metric(
            label="DL Duplicate F1",
            value="50.80%",
            delta="+393%"
        )
    
    with col4:
        st.metric(
            label="DL Recall",
            value="98.75%",
            delta="+1480%"
        )
    
    st.markdown("---")
    
    # Quick stats
    st.markdown("### 📈 Dataset Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #1f77b4; margin: 0;">5,851</h3>
            <p style="margin: 0; color: #666;">Total Samples</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #1f77b4; margin: 0;">4</h3>
            <p style="margin: 0; color: #666;">Categories</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #1f77b4; margin: 0;">80/20</h3>
            <p style="margin: 0; color: #666;">Train/Test Split</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #1f77b4; margin: 0;">~33%</h3>
            <p style="margin: 0; color: #666;">Duplicate Rate</p>
        </div>
        """, unsafe_allow_html=True)

# ANALYZE TICKET PAGE
elif page == "Analyze Ticket":
    st.markdown('<div class="main-header">🔍 Analyze Single Ticket</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Compare NLP and Deep Learning predictions side-by-side</div>', unsafe_allow_html=True)
    
    if not models_loaded:
        st.error("⚠️ Models not loaded. Please check the models directory.")
    else:
        # Input section
        st.markdown("### 📝 Enter Ticket Text")
        
        ticket_text = st.text_area(
            "Ticket Text",
            height=150,
            placeholder="Example: My payment failed but I was charged twice. Please refund the duplicate charge.",
            label_visibility="collapsed"
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            analyze_button = st.button("🚀 Analyze Ticket", type="primary", width='stretch')
        
        with col2:
            if st.button("🗑️ Clear", width='stretch'):
                st.rerun()
        
        if analyze_button:
            if not ticket_text.strip():
                st.warning("⚠️ Please enter ticket text.")
            else:
                with st.spinner("🔄 Analyzing ticket..."):
                    # Get predictions
                    nlp_result, nlp_error = predict_nlp(
                        ticket_text, nlp_vectorizer, nlp_classifier, 
                        nlp_label_encoder, nlp_train_vectors
                    )
                    
                    dl_result, dl_error = predict_dl(
                        ticket_text, dl_model, dl_tokenizer, 
                        dl_label_encoder, dl_embedding_model, dl_train_embeddings
                    )
                
                if nlp_error or dl_error:
                    st.error(f"❌ Error: {nlp_error or dl_error}")
                else:
                    st.success("✅ Analysis complete!")
                    
                    st.markdown("---")
                    
                    # Results in two columns
                    col1, col2 = st.columns(2)
                    
                    # NLP Results
                    with col1:
                        st.markdown("### 🔵 NLP Results (TF-IDF)")
                        
                        st.markdown(f"""
                        <div class="result-box-nlp">
                            <h4 style="margin-top: 0;">Classification</h4>
                            <p style="font-size: 1.1rem; margin: 0.5rem 0;">
                                <strong>Category:</strong> <span style="color: #1f77b4; font-size: 1.3rem;">{nlp_result['category'].upper()}</span>
                            </p>
                            <p style="margin: 0.5rem 0;">
                                <strong>Confidence:</strong> {nlp_result['confidence']:.2f}%
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.progress(float(nlp_result['confidence']) / 100)
                        
                        st.markdown(f"""
                        <div class="result-box-nlp">
                            <h4 style="margin-top: 0;">Duplicate Detection</h4>
                            <p style="font-size: 1.1rem; margin: 0.5rem 0;">
                                <strong>Status:</strong> {'✅ Duplicate Found' if nlp_result['is_duplicate'] else '❌ Not a Duplicate'}
                            </p>
                            <p style="margin: 0.5rem 0;">
                                <strong>Max Similarity:</strong> {nlp_result['max_similarity']:.4f}
                            </p>
                            <p style="margin: 0.5rem 0;">
                                <strong>Threshold:</strong> {NLP_THRESHOLD}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Top 3 similar tickets
                        st.markdown("**Top 3 Similar Tickets:**")
                        for i, sim in enumerate(nlp_result['top_3_similarities'], 1):
                            st.write(f"  {i}. Similarity: {sim:.4f}")
                        
                        # Category probabilities chart
                        st.markdown("**Category Probabilities:**")
                        fig = go.Figure(data=[
                            go.Bar(
                                x=list(nlp_result['all_probabilities'].keys()),
                                y=list(nlp_result['all_probabilities'].values()),
                                marker_color='#1f77b4',
                                text=[f"{v:.1f}%" for v in nlp_result['all_probabilities'].values()],
                                textposition='outside'
                            )
                        ])
                        fig.update_layout(
                            yaxis_title="Probability (%)",
                            xaxis_title="Category",
                            height=300,
                            showlegend=False,
                            margin=dict(t=20, b=20)
                        )
                        st.plotly_chart(fig, width='stretch')
                    
                    # DL Results
                    with col2:
                        st.markdown("### 🟢 DL Results (LSTM)")
                        
                        st.markdown(f"""
                        <div class="result-box-dl">
                            <h4 style="margin-top: 0;">Classification</h4>
                            <p style="font-size: 1.1rem; margin: 0.5rem 0;">
                                <strong>Category:</strong> <span style="color: #4caf50; font-size: 1.3rem;">{dl_result['category'].upper()}</span>
                            </p>
                            <p style="margin: 0.5rem 0;">
                                <strong>Confidence:</strong> {dl_result['confidence']:.2f}%
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.progress(float(dl_result['confidence']) / 100)
                        
                        st.markdown(f"""
                        <div class="result-box-dl">
                            <h4 style="margin-top: 0;">Duplicate Detection</h4>
                            <p style="font-size: 1.1rem; margin: 0.5rem 0;">
                                <strong>Status:</strong> {'✅ Duplicate Found' if dl_result['is_duplicate'] else '❌ Not a Duplicate'}
                            </p>
                            <p style="margin: 0.5rem 0;">
                                <strong>Max Similarity:</strong> {dl_result['max_similarity']:.4f}
                            </p>
                            <p style="margin: 0.5rem 0;">
                                <strong>Threshold:</strong> {DL_THRESHOLD}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Category probabilities chart
                        st.markdown("**Category Probabilities:**")
                        fig = go.Figure(data=[
                            go.Bar(
                                x=list(dl_result['all_probabilities'].keys()),
                                y=list(dl_result['all_probabilities'].values()),
                                marker_color='#4caf50',
                                text=[f"{v:.1f}%" for v in dl_result['all_probabilities'].values()],
                                textposition='outside'
                            )
                        ])
                        fig.update_layout(
                            yaxis_title="Probability (%)",
                            xaxis_title="Category",
                            height=300,
                            showlegend=False,
                            margin=dict(t=20, b=20)
                        )
                        st.plotly_chart(fig, width='stretch')
                    
                    # Comparison summary
                    st.markdown("---")
                    st.markdown("### 📊 Quick Comparison")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        agreement = "✅ Agree" if nlp_result['category'] == dl_result['category'] else "⚠️ Disagree"
                        st.metric("Category Prediction", agreement)
                    
                    with col2:
                        dup_agreement = "✅ Agree" if nlp_result['is_duplicate'] == dl_result['is_duplicate'] else "⚠️ Disagree"
                        st.metric("Duplicate Detection", dup_agreement)
                    
                    with col3:
                        avg_conf = (nlp_result['confidence'] + dl_result['confidence']) / 2
                        st.metric("Avg Confidence", f"{avg_conf:.1f}%")

# BATCH PROCESSING PAGE
elif page == "Batch Processing":
    st.markdown('<div class="main-header">📦 Batch Processing</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Process multiple tickets at once from CSV file</div>', unsafe_allow_html=True)
    
    if not models_loaded:
        st.error("⚠️ Models not loaded. Please check the models directory.")
    else:
        st.markdown("### 📤 Upload CSV File")
        st.info("💡 Your CSV file must contain a column named **'text'** with ticket descriptions.")
        
        uploaded_file = st.file_uploader("Choose CSV file", type=['csv'], label_visibility="collapsed")
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                
                if 'text' not in df.columns:
                    st.error("❌ CSV must contain a 'text' column.")
                else:
                    st.success(f"✅ Loaded {len(df)} tickets")
                    
                    st.markdown("### 📋 Preview")
                    st.dataframe(df.head(10), width='stretch')
                    
                    st.markdown("---")
                    
                    col1, col2, col3 = st.columns([1, 1, 2])
                    
                    with col1:
                        process_button = st.button("🚀 Process All Tickets", type="primary", width='stretch')
                    
                    if process_button:
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        results = []
                        
                        for idx, row in df.iterrows():
                            status_text.text(f"🔄 Processing ticket {idx + 1}/{len(df)}...")
                            progress_bar.progress((idx + 1) / len(df))
                            
                            text = row['text']
                            
                            nlp_result, _ = predict_nlp(
                                text, nlp_vectorizer, nlp_classifier,
                                nlp_label_encoder, nlp_train_vectors
                            )
                            
                            dl_result, _ = predict_dl(
                                text, dl_model, dl_tokenizer,
                                dl_label_encoder, dl_embedding_model, dl_train_embeddings
                            )
                            
                            results.append({
                                'ticket_id': idx + 1,
                                'text': text[:100] + '...' if len(text) > 100 else text,
                                'nlp_category': nlp_result['category'] if nlp_result else 'Error',
                                'nlp_confidence': f"{nlp_result['confidence']:.2f}%" if nlp_result else 'N/A',
                                'nlp_duplicate': 'Yes' if nlp_result and nlp_result['is_duplicate'] else 'No',
                                'nlp_similarity': f"{nlp_result['max_similarity']:.4f}" if nlp_result else 'N/A',
                                'dl_category': dl_result['category'] if dl_result else 'Error',
                                'dl_confidence': f"{dl_result['confidence']:.2f}%" if dl_result else 'N/A',
                                'dl_duplicate': 'Yes' if dl_result and dl_result['is_duplicate'] else 'No',
                                'dl_similarity': f"{dl_result['max_similarity']:.4f}" if dl_result else 'N/A',
                                'category_match': '✅' if (nlp_result and dl_result and nlp_result['category'] == dl_result['category']) else '⚠️'
                            })
                        
                        status_text.text("✅ Processing complete!")
                        progress_bar.progress(1.0)
                        
                        results_df = pd.DataFrame(results)
                        
                        st.markdown("---")
                        st.markdown("### 📊 Results Summary")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Total Processed", len(results_df))
                        
                        with col2:
                            nlp_dups = results_df['nlp_duplicate'].value_counts().get('Yes', 0)
                            st.metric("NLP Duplicates", nlp_dups)
                        
                        with col3:
                            dl_dups = results_df['dl_duplicate'].value_counts().get('Yes', 0)
                            st.metric("DL Duplicates", dl_dups)
                        
                        with col4:
                            matches = results_df['category_match'].value_counts().get('✅', 0)
                            match_pct = (matches / len(results_df)) * 100
                            st.metric("Category Agreement", f"{match_pct:.1f}%")
                        
                        st.markdown("### 📋 Detailed Results")
                        st.dataframe(results_df, width='stretch', height=400)
                        
                        # Download button
                        csv = results_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Results CSV",
                            data=csv,
                            file_name="ticket_analysis_results.csv",
                            mime="text/csv",
                            type="primary",
                            width='stretch'
                        )
                        
                        # Category distribution
                        st.markdown("### 📊 Category Distribution")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            nlp_cats = results_df['nlp_category'].value_counts()
                            fig = px.pie(values=nlp_cats.values, names=nlp_cats.index, 
                                        title="NLP Categories", color_discrete_sequence=px.colors.sequential.Blues_r)
                            st.plotly_chart(fig, width='stretch')
                        
                        with col2:
                            dl_cats = results_df['dl_category'].value_counts()
                            fig = px.pie(values=dl_cats.values, names=dl_cats.index, 
                                        title="DL Categories", color_discrete_sequence=px.colors.sequential.Greens_r)
                            st.plotly_chart(fig, width='stretch')
            
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")

# MODEL COMPARISON PAGE
elif page == "Model Comparison":
    st.markdown('<div class="main-header">📊 Model Comparison</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Detailed performance analysis of NLP vs Deep Learning approaches</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Classification Performance
    st.markdown("### 🎯 Classification Performance")
    st.write("Both models achieve similar accuracy for ticket categorization (~90%)")
    
    classification_data = {
        'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
        'NLP (TF-IDF)': ['91.33%', '91.81%', '91.33%', '91.42%'],
        'DL (LSTM)': ['90.05%', '90.11%', '90.05%', '90.05%'],
        'Difference': ['-1.28%', '-1.70%', '-1.28%', '-1.37%']
    }
    
    clf_df = pd.DataFrame(classification_data)
    
    # Style the dataframe
    st.dataframe(
        clf_df.style.set_properties(**{
            'background-color': '#f8f9fa',
            'border-color': '#dee2e6',
            'text-align': 'center'
        }).set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#1f77b4'), ('color', 'white'), ('font-weight', 'bold')]}
        ]),
        width='stretch',
        hide_index=True
    )
    
    st.info("💡 **Insight:** Both models perform similarly for classification with NLP having a slight edge (~91% vs ~90% accuracy)")
    
    # Classification visualization
    fig = go.Figure()
    
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    nlp_values = [91.33, 91.81, 91.33, 91.42]
    dl_values = [90.05, 90.11, 90.05, 90.05]
    
    fig.add_trace(go.Bar(
        name='NLP (TF-IDF)',
        x=metrics,
        y=nlp_values,
        marker_color='#1f77b4',
        text=[f"{v:.2f}%" for v in nlp_values],
        textposition='outside'
    ))
    
    fig.add_trace(go.Bar(
        name='DL (LSTM)',
        x=metrics,
        y=dl_values,
        marker_color='#4caf50',
        text=[f"{v:.2f}%" for v in dl_values],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Classification Metrics Comparison",
        yaxis_title="Score (%)",
        xaxis_title="Metric",
        barmode='group',
        height=400,
        yaxis_range=[0, 100]
    )
    
    st.plotly_chart(fig, width='stretch')
    
    st.markdown("---")
    
    # Duplicate Detection Performance
    st.markdown("### 🔄 Duplicate Detection Performance")
    st.write("Deep Learning significantly outperforms NLP for finding duplicate tickets")
    
    duplicate_data = {
        'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
        'NLP (TF-IDF)': ['63.01%', '29.41%', '6.25%', '10.31%'],
        'DL (LSTM)': ['34.95%', '34.20%', '98.75%', '50.80%'],
        'Improvement': ['-44.5%', '+16.3%', '+1480.0%', '+392.7%']
    }
    
    dup_df = pd.DataFrame(duplicate_data)
    
    # Style the dataframe with conditional formatting
    def highlight_improvement(val):
        if isinstance(val, str) and '+' in val:
            return 'background-color: #d4edda; color: #155724; font-weight: bold'
        elif isinstance(val, str) and '-' in val and 'Improvement' in val:
            return 'background-color: #f8d7da; color: #721c24'
        return ''
    
    st.dataframe(
        dup_df.style.map(highlight_improvement, subset=['Improvement']).set_properties(**{
            'text-align': 'center'
        }).set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#1f77b4'), ('color', 'white'), ('font-weight', 'bold')]}
        ]),
        width='stretch',
        hide_index=True
    )
    
    st.success("✅ **Key Finding:** DL achieves 98.75% recall (finds almost all duplicates) vs NLP's 6.25% recall")
    
    # Duplicate detection visualization
    col1, col2 = st.columns(2)
    
    with col1:
        fig = go.Figure()
        
        metrics = ['Precision', 'Recall', 'F1-Score']
        nlp_dup = [29.41, 6.25, 10.31]
        dl_dup = [34.20, 98.75, 50.80]
        
        fig.add_trace(go.Bar(
            name='NLP',
            x=metrics,
            y=nlp_dup,
            marker_color='#1f77b4',
            text=[f"{v:.2f}%" for v in nlp_dup],
            textposition='outside'
        ))
        
        fig.add_trace(go.Bar(
            name='DL',
            x=metrics,
            y=dl_dup,
            marker_color='#4caf50',
            text=[f"{v:.2f}%" for v in dl_dup],
            textposition='outside'
        ))
        
        fig.update_layout(
            title="Duplicate Detection Metrics",
            yaxis_title="Score (%)",
            barmode='group',
            height=400,
            yaxis_range=[0, 110]
        )
        
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        improvement_data = {
            'Metric': ['Recall', 'F1-Score'],
            'Improvement (%)': [1480.0, 392.7]
        }
        
        fig = go.Figure(data=[
            go.Bar(
                x=improvement_data['Metric'],
                y=improvement_data['Improvement (%)'],
                marker_color='#ff7f0e',
                text=[f"+{v:.1f}%" for v in improvement_data['Improvement (%)']],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title="DL Improvement over NLP",
            yaxis_title="Improvement (%)",
            height=400
        )
        
        st.plotly_chart(fig, width='stretch')
    
    st.markdown("---")
    
    # Why DL is better for duplicates
    st.markdown("### 🤔 Why Deep Learning Excels at Duplicate Detection")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-box">
        <h4>🔵 NLP Approach (TF-IDF)</h4>
        <p><strong>Method:</strong> Cosine similarity on word frequency vectors</p>
        <p><strong>Limitation:</strong> Only captures lexical similarity (exact word matches)</p>
        <p><strong>Example:</strong></p>
        <ul>
            <li>"Payment failed" vs "Charge didn't work" → Low similarity ❌</li>
            <li>Misses semantic duplicates with different wording</li>
        </ul>
        <p><strong>Result:</strong> 6.25% recall (misses 93.75% of duplicates)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="success-box">
        <h4>🟢 DL Approach (LSTM)</h4>
        <p><strong>Method:</strong> Cosine similarity on learned embeddings</p>
        <p><strong>Advantage:</strong> Captures semantic meaning and context</p>
        <p><strong>Example:</strong></p>
        <ul>
            <li>"Payment failed" vs "Charge didn't work" → High similarity ✅</li>
            <li>Understands synonyms and paraphrases</li>
        </ul>
        <p><strong>Result:</strong> 98.75% recall (finds almost all duplicates)</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key Takeaways
    st.markdown("### 🔑 Key Takeaways")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔵 NLP (TF-IDF) Strengths")
        st.markdown("""
        - ✅ **Fast inference** (~10ms per ticket)
        - ✅ **Interpretable features** (word frequencies)
        - ✅ **Good classification** (91.33% accuracy)
        - ✅ **Low computational cost** (CPU-friendly)
        - ✅ **Easy to deploy** (small model size)
        - ✅ **No GPU required**
        
        **Best for:** Quick classification when speed matters
        """)
    
    with col2:
        st.markdown("#### 🟢 DL (LSTM) Strengths")
        st.markdown("""
        - ✅ **Semantic understanding** (context-aware)
        - ✅ **Excellent duplicate detection** (98.75% recall)
        - ✅ **5x better F1-score** for duplicates (50.80% vs 10.31%)
        - ✅ **Handles paraphrases** (different wording, same meaning)
        - ✅ **Learns complex patterns**
        - ✅ **Comparable classification** (90.05% accuracy)
        
        **Best for:** Duplicate detection and semantic similarity
        """)
    
    st.markdown("---")
    
    # Recommendation
    st.markdown("### 💡 Recommendation")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 10px; margin: 1rem 0;">
        <h3 style="margin-top: 0; color: white;">🎯 Hybrid Approach</h3>
        <p style="font-size: 1.1rem;">
            Use <strong>NLP for classification</strong> (fast, accurate) and <strong>DL for duplicate detection</strong> (semantic understanding).
        </p>
        <p>
            This combines the best of both worlds: speed and interpretability from NLP, with superior duplicate detection from DL.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ABOUT PAGE
elif page == "About":
    st.markdown('<div class="main-header">ℹ️ About This Project</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Technical details and implementation overview</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Project Overview
    st.markdown("### 📖 Project Overview")
    
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #1f77b4;">
        <p style="font-size: 1.1rem; margin: 0;">
            This project compares <strong>two approaches</strong> for customer support ticket classification and duplicate detection:
        </p>
        <br>
        <ol style="font-size: 1.05rem;">
            <li><strong>Traditional NLP:</strong> TF-IDF vectorization + Logistic Regression</li>
            <li><strong>Deep Learning:</strong> LSTM neural network with word embeddings</li>
        </ol>
        <br>
        <p style="font-size: 1.05rem; margin: 0;">
            The goal is to <strong>automate ticket routing</strong> and <strong>reduce redundant work</strong> by identifying duplicate tickets.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tech Stack
    st.markdown("### 🛠️ Tech Stack")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #1f77b4; margin-top: 0;">🔵 NLP Pipeline</h4>
            <ul style="font-size: 0.95rem;">
                <li><strong>Vectorization:</strong> TF-IDF</li>
                <li><strong>Features:</strong> 5000 (bigrams)</li>
                <li><strong>Classifier:</strong> Logistic Regression</li>
                <li><strong>Duplicates:</strong> Cosine similarity</li>
                <li><strong>Threshold:</strong> 0.6</li>
                <li><strong>Library:</strong> Scikit-learn</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #4caf50; margin-top: 0;">🟢 DL Pipeline</h4>
            <ul style="font-size: 0.95rem;">
                <li><strong>Architecture:</strong> LSTM</li>
                <li><strong>Embedding:</strong> 128 dimensions</li>
                <li><strong>LSTM Units:</strong> 64</li>
                <li><strong>Duplicates:</strong> Embedding similarity</li>
                <li><strong>Threshold:</strong> 0.95</li>
                <li><strong>Framework:</strong> TensorFlow/Keras</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #ff7f0e; margin-top: 0;">🔧 Shared Components</h4>
            <ul style="font-size: 0.95rem;">
                <li><strong>Preprocessing:</strong> NLTK</li>
                <li><strong>Contractions:</strong> contractions</li>
                <li><strong>Lemmatization:</strong> WordNet</li>
                <li><strong>UI:</strong> Streamlit</li>
                <li><strong>Visualization:</strong> Plotly</li>
                <li><strong>Data:</strong> Pandas, NumPy</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Dataset Information
    st.markdown("### 📊 Dataset Information")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📈 Statistics")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("Total Samples", "5,851")
        
        with col_b:
            st.metric("Training Set", "4,675")
        
        with col_c:
            st.metric("Test Set", "1,176")
        
        st.markdown("")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("Categories", "4")
        
        with col_b:
            st.metric("Train/Test", "80/20")
        
        with col_c:
            st.metric("Duplicates", "~33%")
    
    with col2:
        st.markdown("#### 🏷️ Categories")
        
        st.markdown("""
        <div class="metric-card">
            <ul style="font-size: 1rem; margin: 0;">
                <li><strong>💳 Billing:</strong> Payment issues, refunds, charges</li>
                <li><strong>🔧 Technical:</strong> App crashes, bugs, errors</li>
                <li><strong>📦 Delivery:</strong> Shipping, tracking, delays</li>
                <li><strong>👤 Account:</strong> Login, password, profile</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 🔄 Duplicate Generation")
        
        st.markdown("""
        <div class="metric-card">
            <p style="margin: 0; font-size: 0.95rem;">
                Synthetic duplicates created using:
            </p>
            <ul style="font-size: 0.95rem; margin-top: 0.5rem;">
                <li>Synonym replacement</li>
                <li>Paraphrasing techniques</li>
                <li>Maintained semantic meaning</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Implementation Details
    st.markdown("### 👨‍💻 Implementation Details")
    
    tab1, tab2, tab3 = st.tabs(["📝 Preprocessing", "🏗️ Model Architectures", "⚙️ Training"])
    
    with tab1:
        st.markdown("#### Preprocessing Pipeline")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.code("""
# Step-by-step preprocessing:

1. HTML entity decoding
   (&amp; → &, &lt; → <)

2. Contraction expansion
   (hasn't → has not)

3. Lowercasing
   (Hello → hello)

4. Punctuation replacement
   (Replace with space, not remove)

5. Stopword removal
   (Keep negations: not, no, never)

6. Lemmatization
   (running → run, better → good)
            """, language="python")
        
        with col2:
            st.markdown("**Example:**")
            
            st.markdown("""
            <div class="metric-card">
                <p><strong>Input:</strong></p>
                <code style="background: #e9ecef; padding: 0.5rem; display: block; border-radius: 5px;">
                    "My payment hasn't been processed & I'm charged twice!"
                </code>
                <br>
                <p><strong>Output:</strong></p>
                <code style="background: #e9ecef; padding: 0.5rem; display: block; border-radius: 5px;">
                    "payment processed charged twice"
                </code>
            </div>
            """, unsafe_allow_html=True)
            
            st.info("💡 Consistent preprocessing ensures both models work with the same input format")
    
    with tab2:
        st.markdown("#### Model Architectures")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔵 NLP Model**")
            st.code("""
# TF-IDF Vectorizer
TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    min_df=2
)

# Logistic Regression
LogisticRegression(
    max_iter=1000,
    random_state=42
)

# Duplicate Detection
- Cosine similarity on TF-IDF vectors
- Threshold: 0.6
- Returns top 3 matches
            """, language="python")
        
        with col2:
            st.markdown("**🟢 DL Model**")
            st.code("""
# LSTM Architecture
Sequential([
    Embedding(
        vocab_size, 128,
        mask_zero=True
    ),
    LSTM(64),
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dense(4, activation='softmax')
])

# Duplicate Detection
- Cosine similarity on LSTM embeddings
- Threshold: 0.95 (tuned)
- 64-dimensional embeddings
            """, language="python")
    
    with tab3:
        st.markdown("#### Training Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔵 NLP Training**")
            st.markdown("""
            <div class="metric-card">
                <ul style="font-size: 0.95rem;">
                    <li><strong>Training time:</strong> ~2 seconds</li>
                    <li><strong>Hardware:</strong> CPU only</li>
                    <li><strong>Model size:</strong> ~50 MB</li>
                    <li><strong>Inference:</strong> ~10ms per ticket</li>
                    <li><strong>Optimization:</strong> None needed</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("**🟢 DL Training**")
            st.markdown("""
            <div class="metric-card">
                <ul style="font-size: 0.95rem;">
                    <li><strong>Epochs:</strong> 10</li>
                    <li><strong>Batch size:</strong> 32</li>
                    <li><strong>Validation split:</strong> 20%</li>
                    <li><strong>Optimizer:</strong> Adam</li>
                    <li><strong>Loss:</strong> Categorical crossentropy</li>
                    <li><strong>Training time:</strong> ~5 minutes (GPU)</li>
                    <li><strong>Model size:</strong> ~15 MB</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Source and Credits
    st.markdown("### 📚 Data Source")
    
    st.markdown("""
    <div style="background-color: #e3f2fd; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #1f77b4;">
        <p style="margin: 0; font-size: 1.05rem;">
            <strong>Dataset:</strong> Customer Support on Twitter (TWCS)
        </p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.95rem;">
            <strong>Source:</strong> Kaggle - thoughtvector/customer-support-on-twitter
        </p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.95rem;">
            <strong>Original size:</strong> 2.8M tweets from customer support interactions
        </p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.95rem;">
            <strong>Processed:</strong> Semi-supervised labeling + synthetic duplicate generation
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background-color: #f8f9fa; border-radius: 10px; margin-top: 2rem;">
        <h3 style="color: #1f77b4; margin-top: 0;">🎫 Ticket Classification System</h3>
        <p style="color: #666; margin: 0.5rem 0;">
            A demonstration project comparing NLP and Deep Learning approaches
        </p>
        <p style="color: #666; margin: 0.5rem 0; font-size: 0.9rem;">
            Built with Streamlit • TensorFlow • Scikit-learn • NLTK
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem;">
    <p style="margin: 0; font-weight: bold; color: #1f77b4;">🎫 Ticket Classification System</p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem; color: #666;">Version 1.0</p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; color: #999;">NLP vs Deep Learning</p>
</div>
""", unsafe_allow_html=True)
