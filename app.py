import streamlit as st
from auth import init_session_state, get_current_user, login_user, logout_user
from database import init_db

# Configuración inicial (SIEMPRE PRIMERO)
st.set_page_config(
    page_title="Gestión Comercial Elite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tema Dark Mode con acentos Esmeralda y Azul Eléctrico
st.markdown("""
    <style>
    /* Ocultar elementos por defecto de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fondo General Profundo */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    
    /* Botones Primarios (Verde Esmeralda) */
    .stButton>button[kind="primary"] {
        background-color: #10b981;
        color: white;
        border: none;
        border-radius: 8px;
        transition: all 0.3s ease;
        font-weight: 600;
        box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.4);
    }
    .stButton>button[kind="primary"]:hover {
        background-color: #059669;
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.5);
        transform: translateY(-2px);
    }
    
    /* Botones Secundarios (Azul Eléctrico) */
    .stButton>button[kind="secondary"] {
        background-color: #1e293b;
        color: #38bdf8;
        border: 1px solid #38bdf8;
        border-radius: 8px;
        transition: all 0.3s ease;
        font-weight: 600;
    }
    .stButton>button[kind="secondary"]:hover {
        background-color: #38bdf8;
        color: #0b0f19;
    }
    
    /* Formularios y Cajas de Texto */
    div[data-baseweb="input"] > div {
        background-color: #1e293b;
        border-color: #334155;
        border-radius: 8px;
        color: white;
    }
    div[data-baseweb="input"] > div:focus-within {
        border-color: #38bdf8;
        box-shadow: 0 0 0 1px #38bdf8;
    }
    
    /* Tablas modernas */
    .dataframe {
        border-collapse: collapse;
        width: 100%;
        color: #cbd5e1;
    }
    .dataframe th {
        background-color: #1e293b !important;
        color: #38bdf8 !important;
        padding: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .dataframe td {
        background-color: #0f172a;
        padding: 10px;
        border-bottom: 1px solid #334155;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
    
    /* Tarjetas Metrics (Crypto Style) - Para el Dashboard */
    .metric-card {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        border: 1px solid #334155;
        text-align: center;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #38bdf8;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #10b981;
        margin: 10px 0;
    }
    .metric-label {
        color: #94a3b8;
        text-transform: uppercase;
        font-size: 0.85rem;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

init_db()
init_session_state()
user = get_current_user()

if not user:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; color: #38bdf8;'>⚡ Elite Store OS</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94a3b8; margin-bottom: 30px;'>Acceso Seguro</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("Correo Electrónico 📧")
            password = st.text_input("Contraseña 🔒", type="password")
            submitted = st.form_submit_button("Ingresar al Sistema", type="primary")
            
            if submitted:
                if email and password:
                    user_data, error = login_user(email, password)
                    if error:
                        st.error(f"Error: {error}")
                    else:
                        st.session_state.user = user_data
                        st.rerun()
                else:
                    st.warning("Completa todos los campos.")
else:
    with st.sidebar:
        st.markdown(f"### 👤 {user['full_name']}")
        st.markdown(f"**🛡️ Rol:** <span style='color:#10b981;'>{user['role']}</span>", unsafe_allow_html=True)
        st.divider()
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            logout_user()
            st.session_state.user = None
            st.rerun()
            
    st.markdown("## 👋 Bienvenido al Sistema Elite")
    st.info("👈 Selecciona una operación en el menú lateral.")
