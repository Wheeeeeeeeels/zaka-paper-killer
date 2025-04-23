from core.database import Base, engine
from models.models import User, Paper, Review

def init_db():
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("数据库表创建成功！")

if __name__ == "__main__":
    init_db() 