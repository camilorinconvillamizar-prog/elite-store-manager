import os
from supabase import create_client, Client
from dotenv import load_dotenv
import streamlit as st
from database import SessionLocal, Profile

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

@st.cache_resource
def init_supabase() -> Client:
    if SUPABASE_URL and SUPABASE_KEY:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    return None

supabase: Client = init_supabase()

def login_user(email, password):
    if not supabase:
        st.error("Supabase no está configurado. Revisa las variables de entorno.")
        return None, "Error de configuración"
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if response.user:
            # Obtener el rol desde la base de datos (SQLAlchemy)
            db = SessionLocal()
            profile = db.query(Profile).filter(Profile.id == response.user.id).first()
            role = profile.role if profile else "Cajero"
            full_name = profile.full_name if profile else response.user.email
            db.close()
            
            return {
                "id": response.user.id,
                "email": response.user.email,
                "role": role,
                "full_name": full_name,
                "access_token": response.session.access_token
            }, None
    except Exception as e:
        return None, str(e)

def logout_user():
    if supabase:
        try:
            supabase.auth.sign_out()
        except:
            pass

def init_session_state():
    if "user" not in st.session_state:
        st.session_state.user = None

def get_current_user():
    return st.session_state.get("user")

def require_auth():
    if not get_current_user():
        st.warning("Debes iniciar sesión para ver esta página.")
        st.stop()

def require_role(allowed_roles):
    user = get_current_user()
    if not user:
        st.warning("Debes iniciar sesión para ver esta página.")
        st.stop()
    if user["role"] not in allowed_roles:
        st.error(f"Acceso denegado. Se requiere uno de los siguientes roles: {', '.join(allowed_roles)}")
        st.stop()
