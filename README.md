
# Second app with fastapi.

Upgrape the precision of my code.

-Annotated
## 🚀 Installation

1. Clone le repo
```bash
   git clone https://github.com/ton-username/ton-projet.git
   cd ton-projet
```

2. Crée ton fichier .env depuis le template
```bash
   cp .env.example .env
```

3. Édite .env avec tes vraies valeurs
```bash
   nano .env
   # Remplace les valeurs "your_*_here"
```

4. Génère une vraie SECRET_KEY
```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   # Copie le résultat dans .env
```

----------------------------------------------------

## Alembic:

### 1. Installation:
```python
pip install alembic
alembic --version
```

### 2. Initialisation:

```python
alembic init alembic
```

=> ca crée:
```java
alembic/
 ├─ versions/        ← TES MIGRATIONS (sacré)
 ├─ env.py           ← cerveau d’Alembic
 └─ script.py.mako
alembic.ini          ← config globale
```


 ==> Puis aller dans alembic/env.py et modifier target_metada = None.
 
 ==> IMPORTER TOUT LES MODELS!!


 ```python

# models que alembic prend en compte:
from app.models.users import User
from app.models.posts import Post
from app.models.posts_likes import PostLike

# tables :
from app.core.database import Base

 #target_metadata = None
  target_metadata = Base.metadata

```

== > Impoter l'url de SQL puis ajouter au context:

```python 

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", SQLALCHEMY_URL)
```

## Ici de cas:

-Setup au debut ( recommandé ):

Alembic crée tout
    1. init alembic 
    2. ecrires models
    3. generer migration initail
    4. appliquer migration

```bash
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```



-Setup en cours de projet avec un DB deja un peu rempli:

    1. generer une revision (vide ducoup)
    2. dire a alembic que c'est l'etat officiel
    3. continuer normalement

```bash
# veut dire qu'on prend ce point pour reference meme vide
alembic stamp head
```


ATTENTION quand on:


```bash
alembic revision --autogenerate -m "initial schema"
```

=> creer une table "alembic_version" dans la db.


-------------------------

# Ajout d'un Enum dans Postres avec Alembic

Exemple d'un enum pour un mixin:

### -Creation d'un ENUM

```python
from enum import Enum as PyEnum

class StatusEnum(PyEnum):
    ACTIVE = "active"
    DELETED = "deleted"
    ARCHIVED = "archived"
    SIGNALED = "signaled"
```

### -Creation pour Postgres

==> on lance la revision:
```bash 
alembic revision --autogenerate -m'ajout de "status"'
```

==> NE PAS UPGRADE

### Modification explicite de la version alembic generée:

-creer le type (enum)
-ajouter la colonne pour que les anciens rows soient remplis

```python
from alembic import op
from sqlalchemy.dialects import postgresql

def upgrade():
    # Création du type PostgreSQL
    status_enum = postgresql.ENUM("ACTIVE", "DELETED", "ARCHIVED", "SIGNALED", name="status_enum")
    status_enum.create(op.get_bind(), checkfirst=True)  # check_first: ecrase pas le type si deja present

    # Ajout des colonnes
    op.add_column(
        'users',
        sa.Column(
            'status',
            postgresql.ENUM("ACTIVE","DELETED","ARCHIVED","SIGNALED", name="status_enum"),
            nullable=False,
            server_default='ACTIVE'    # ca va remplir les rows deja existantes
        )
    )
```

Et pour le downgrade:

```python
def downgrade():
    op.drop_column('users', 'status')
    status_enum = postgresql.ENUM("ACTIVE", "DELETED", "ARCHIVED", "SIGNALED", name="status_enum")
    status_enum.drop(op.get_bind(), checkfirst=True)

```


==> Ici, tout est pret pour le coté db , mais pas en sqlalchemy.

### -Mixin dans SQLAlchemy

```python
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import ENUM as PGEnum

class StatusMixin:
    status = Column(
        PGEnum("ACTIVE", "DELETED", "ARCHIVED", "SIGNALED", name="status_enum"),
        nullable=False,
        server_default='ACTIVE'
    )
```

### Final

```bash 
alembic upgrade head
```


--- 

# .env et dotenv :

Sert a isolé des variables importantes:  

### Creer un fichier .env a la racine:
Dedans on met les trucs importants:

```bash
PASSWD="truc"
```
Puis on les retrouves:

```python
import os 
from dotenv import load_dotenv

# on charge les variables du fichier .env
load_dotenv()

print(os.getenv("PASSWD")) # existe donc renvoi la valeur 
print(os.getenv("YASSWD")) # inexistant return None

print(os.environ["PASSWD"]) # existe ou ERROR 
print(os.environ.get("YASSWD", "truc")) # safer: valeur default
```

### Attention : en .env **Tout est STRING** .


---

## Comment acceder aux variables ? 

> Avec Pydantic-settings

```bash
pip install pydantic-setting
```

On creer une class Settings on l'on setup les variables voulu.

```python
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # les '...' signifie OBLIGATOIRE:
    postgres_user : str = Field(..., env="POSTGRES_USER")
    # on peut mettre une valeur par defaut:
    postgres_port : str = Field(default="localhost", env="POSTGRES_PORT")

    # config sert a gerer la config de la class:
    class Config:
        env_file = ".env"  # dit ou chercher.
        case_sensitive = False

# crée une instance a utiliser pour mon app:
settings = Settings() 
```


---

# Gestion et Validations pydantic avancé:

On met un Field pour etre encore plus precis , puis des foncitons de validations.

```python
from pydantic import Field, field_validator
```

Exemple de field:
```python
class UserSchema(Basemodel):
    username: str = Field(
        ...,  # rend OBLIGATOIRE
        min_length=1,
        max_length=56,
        description="name for user: 1 to 56 char."
    )
```

Ensuite on utilise **field_validatoir** pour cibler un champ:
```python
import re # sert pour regex

@filed_validator('username')
@classmethod # subtil mais: c'est une verification AVANT la creation de l'instance donc on utilise un classmethod car l'instance est pas encore créé.
def username_alphanumeric(cls, name)->str:
    if re.match(r'^[a-zA-Z0-9_]+$', name) is None:
        # re.match compare le regex et la valeur de la func:
            # si ca marche : renvoi un objet regex
            # si marche PAS : renvoi None
        raise ValueError("Username need to be alphanumeric")
    return name
```

