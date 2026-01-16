from sqlalchemy import create_engine

engine = create_engine("sqlite:///skillswap.db", pool_size=20, max_overflow=30, pool_timeout=60)
