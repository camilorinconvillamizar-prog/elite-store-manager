import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL) if DATABASE_URL else None
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class UserRole(str, Enum):
    ADMIN = "Administrador"
    CAJERO = "Cajero"

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    role = Column(String, default="Cajero")
    created_at = Column(DateTime, default=datetime.utcnow)

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact_name = Column(String)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    products = relationship("Product", back_populates="supplier")

class Product(Base):
    __tablename__ = "products"
    barcode = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String)
    purchase_cost = Column(Float, nullable=False)
    sale_price = Column(Float, nullable=False)
    stock = Column(Float, default=0.0)
    min_stock = Column(Float, default=5.0)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    supplier = relationship("Supplier", back_populates="products")

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("profiles.id"))
    total_amount = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)
    payment_method = Column(String, nullable=False) # JSON o String para multi-pagos
    timestamp = Column(DateTime, default=datetime.utcnow)

    items = relationship("SaleItem", back_populates="sale")

class SaleItem(Base):
    __tablename__ = "sale_items"
    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"))
    product_barcode = Column(String, ForeignKey("products.barcode"))
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    sale = relationship("Sale", back_populates="items")
    product = relationship("Product")

class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"
    id = Column(Integer, primary_key=True, index=True)
    product_barcode = Column(String, ForeignKey("products.barcode"))
    transaction_type = Column(String, nullable=False) # Venta, Compra, Ajuste, Merma
    quantity = Column(Float, nullable=False)
    justification = Column(String)
    user_id = Column(String, ForeignKey("profiles.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product")

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String, ForeignKey("profiles.id"))

def init_db():
    if engine:
        Base.metadata.create_all(bind=engine)
