from app.core.database import engine


try:
    with engine.connect() as connexion:
        print("Engine connected!")
except Exception as e:
    print(f"Engine connexion FAILED : {e}")