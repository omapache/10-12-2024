import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

# Configuración de la base de datos
Base = declarative_base()
engine = create_engine('sqlite:///tareas.db', echo=True)
Session = sessionmaker(bind=engine)

# Modelo de datos
class Tarea(Base):
    __tablename__ = 'tareas'
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String(100))
    descripcion = Column(String(500))
    completada = Column(Boolean, default=False)

# Crear tablas
Base.metadata.create_all(engine)

#****************************** Funciones CRUD ******************************
def agregar_tarea(titulo, descripcion):
    session = Session()
    try:
        nueva_tarea = Tarea(titulo=titulo, descripcion=descripcion)
        session.add(nueva_tarea)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False
    finally:
        session.close()

def listar_tareas():
    session = Session()
    try:
        return session.query(Tarea).all()
    finally:
        session.close()

def marcar_completada(id_tarea):
    session = Session()
    try:
        tarea = session.query(Tarea).filter_by(id=id_tarea).first()
        if tarea:
            tarea.completada = True
            session.commit()
            return True
        return False
    except:
        session.rollback()
        return False
    finally:
        session.close()

def eliminar_tarea(id_tarea):
    session = Session()
    try:
        tarea = session.query(Tarea).filter_by(id=id_tarea).first()
        if tarea:
            session.delete(tarea)
            session.commit()
            return True
        return False
    except:
        session.rollback()
        return False
    finally:
        session.close()
#****************************************************************************

# Interfaz de Streamlit
st.title("Gestión de Tareas")

# Sección para crear tareas
with st.form(key="nueva_tarea", clear_on_submit=True):
    st.subheader("Agregar Nueva Tarea")
    titulo = st.text_input("Título")
    descripcion = st.text_area("Descripción")
    submitted = st.form_submit_button("Agregar Tarea")
    
    if submitted:
        if titulo and descripcion:
            if agregar_tarea(titulo, descripcion):
                st.success("Tarea agregada exitosamente")
            else:
                st.error("Error al agregar la tarea")
        else:
            st.warning("Por favor complete todos los campos")

# lista de tareas
st.subheader("Lista de Tareas")
tareas = listar_tareas()

for tarea in tareas:
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.write(f"**{tarea.titulo}**")
        st.write(tarea.descripcion)
        st.write("Estado: " + ("✅ Completada" if tarea.completada else "⏳ Pendiente"))
    
    with col2:
        if not tarea.completada:
            if st.button(f"Completar #{tarea.id}"):
                if marcar_completada(tarea.id):
                    st.rerun()
    
    with col3:
        if st.button(f"Eliminar #{tarea.id}"):
            if eliminar_tarea(tarea.id):
                st.rerun()

# Exportar/Importar tareas
st.subheader("Exportar/Importar Tareas")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Exportar Tareas")

    if st.button("Exportar Tareas"):
        tareas_dict = [{"id": t.id, "titulo": t.titulo, 
                       "descripcion": t.descripcion, 
                       "completada": t.completada} for t in tareas]
        st.download_button(
            label="Descargar JSON",
            data=json.dumps(tareas_dict, indent=2),
            file_name="tareas.json",
            mime="application/json"
        )

with col2:
    st.subheader("Importar Tareas")
    uploaded_file = st.file_uploader("Importar tareas desde JSON")
    
    if uploaded_file is not None:
        if st.button("Importar Tareas"):
            try:
                tareas_importadas = json.load(uploaded_file)
                session = Session()
                for tarea in tareas_importadas:
                    nueva_tarea = Tarea(
                        titulo=tarea['titulo'],
                        descripcion=tarea['descripcion'],
                        completada=tarea['completada']
                    )
                    session.add(nueva_tarea)
                st.success("Tareas importadas correctamente")
                session.commit()
                session.close()
                st.rerun()
            except Exception as e:
                st.error(f"Error al importar tareas: {str(e)}")
