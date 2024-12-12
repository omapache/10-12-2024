import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Tarea(Base):
    __tablename__ = 'tareas'
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String(100))
    descripcion = Column(String(500))
    completada = Column(Boolean, default=False)
