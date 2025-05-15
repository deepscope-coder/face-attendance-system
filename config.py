import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/face_attendance')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY', 'pcsk_r8vKE_NHyBumzqjUcvYp7DDXu7HSqM4QP8iAvr9UmeBcJ5cU2fbWgmQY2r9R864hXNRjQ')
    PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME', 'face-embeddings')
    PINECONE_INDEX_HOST = os.getenv('PINECONE_INDEX_HOST', 'https://face-embeddings-5jlaegm.svc.aped-4627-b74a.pinecone.io')