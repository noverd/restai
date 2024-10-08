from sqlalchemy import create_engine
from app.models.databasemodels import LLMDatabase, ProjectDatabase, RouterEntrancesDatabase, UserDatabase
from app.models.models import LLMModel, LLMUpdate, ProjectModelUpdate, User, UserUpdate
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

from app.config import MYSQL_HOST, MYSQL_URL, POSTGRES_HOST, POSTGRES_URL

if MYSQL_HOST:
    print("Using MySQL database: " + MYSQL_HOST)
    engine = create_engine(MYSQL_URL,
                           pool_size=100,
                           max_overflow=300,
                           pool_recycle=300)
elif POSTGRES_HOST:
    print("Using PostgreSQL database")
    engine = create_engine(POSTGRES_URL,
                           pool_size=100,
                           max_overflow=300,
                           pool_recycle=300)
else:
    print("Using sqlite database.")
    engine = create_engine(
        "sqlite:///./restai.db",
        connect_args={
            "check_same_thread": False},
        pool_size=100,
        max_overflow=300,
        pool_recycle=300)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db, username, password, admin=False, private=False):
    if password:
        password_hash = pwd_context.hash(password)
    else:
        password_hash = None
    db_user = UserDatabase(
        username=username, hashed_password=password_hash, is_admin=admin, is_private=private)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_llm(db, name, class_name, options, privacy, description, llm_type):
    db_llm = LLMDatabase(
        name=name, class_name=class_name, options=options, privacy=privacy, description=description, type=llm_type)
    db.add(db_llm)
    db.commit()
    db.refresh(db_llm)
    return db_llm


def get_users(db):
    users = db.query(UserDatabase).all()
    return users


def get_llms(db):
    llms = db.query(LLMDatabase).all()
    return llms


def get_llm_by_name(db, name):
    llm = db.query(LLMDatabase).filter(
        LLMDatabase.name == name).first()
    return llm


def get_user_by_apikey(db, apikey):
    user = db.query(UserDatabase).filter(
        UserDatabase.api_key == apikey).first()
    return user


def get_user_by_username(db, username):
    user = db.query(UserDatabase).filter(
        UserDatabase.username == username).first()
    return user


def update_user(db, user: User, userc: UserUpdate):
    if userc.password is not None:
        hash = pwd_context.hash(userc.password)
        user.hashed_password = hash

    if userc.is_admin is not None:
        user.is_admin = userc.is_admin

    if userc.is_private is not None:
        user.is_private = userc.is_private

    if userc.sso is not None:
        user.sso = userc.sso

    if userc.api_key is not None:
        user.api_key = userc.api_key

    db.commit()
    return True


def update_llm(db, llm: LLMModel, llmUpdate: LLMUpdate):
    if llmUpdate.class_name is not None and llm.class_name != llmUpdate.class_name:
        llm.class_name = llmUpdate.class_name

    if llmUpdate.options is not None and llm.options != llmUpdate.options:
        llm.options = llmUpdate.options

    if llmUpdate.privacy is not None and llm.privacy != llmUpdate.privacy:
        llm.privacy = llmUpdate.privacy

    if llmUpdate.description is not None and llm.description != llmUpdate.description:
        llm.description = llmUpdate.description

    if llmUpdate.type is not None and llm.type != llmUpdate.type:
        llm.type = llmUpdate.type

    db.commit()
    return True


def delete_llm(db, llm):
    db.delete(llm)
    db.commit()
    return True


def get_user_by_id(db, id):
    user = db.query(UserDatabase).filter(UserDatabase.id == id).first()
    return user


def delete_user(db, user):
    db.delete(user)
    db.commit()
    return True


def get_project_by_name(db, name):
    project = db.query(ProjectDatabase).filter(
        ProjectDatabase.name == name).first()
    return project


def create_project(
        db,
        name,
        embeddings,
        llm,
        vectorstore,
        human_name,
        type,
        creator):
    db_project = ProjectDatabase(
        name=name,
        embeddings=embeddings,
        llm=llm,
        vectorstore=vectorstore,
        human_name=human_name,
        type=type,
        creator=creator)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_projects(db):
    projects = db.query(ProjectDatabase).all()
    return projects


def delete_project(db, project):
    db.delete(project)
    db.commit()
    return True


def update_project(db):
    db.commit()
    return True


def edit_project(name, projectModel: ProjectModelUpdate, db):
    proj_db = get_project_by_name(db, name)
    if proj_db is None:
        return False

    changed = False
    if projectModel.llm is not None and proj_db.llm != projectModel.llm:
        proj_db.llm = projectModel.llm
        changed = True

    if projectModel.system is not None and proj_db.system != projectModel.system:
        proj_db.system = projectModel.system
        changed = True

    if projectModel.censorship is not None and proj_db.censorship != projectModel.censorship:
        proj_db.censorship = projectModel.censorship
        changed = True

    if projectModel.k is not None and proj_db.k != projectModel.k:
        proj_db.k = projectModel.k
        changed = True

    if projectModel.score is not None and proj_db.score != projectModel.score:
        proj_db.score = projectModel.score
        changed = True

    if projectModel.connection is not None and proj_db.connection != projectModel.connection and "://xxxx:xxxx@" not in projectModel.connection:
        proj_db.connection = projectModel.connection
        changed = True

    if projectModel.tables is not None and proj_db.tables != projectModel.tables:
        proj_db.tables = projectModel.tables
        changed = True

    if projectModel.llm_rerank is not None and proj_db.llm_rerank != projectModel.llm_rerank:
        proj_db.llm_rerank = projectModel.llm_rerank
        changed = True

    if projectModel.colbert_rerank is not None and proj_db.colbert_rerank != projectModel.colbert_rerank:
        proj_db.colbert_rerank = projectModel.colbert_rerank
        changed = True

    if projectModel.cache is not None and proj_db.cache != projectModel.cache:
        proj_db.cache = projectModel.cache
        changed = True

    if projectModel.cache_threshold is not None and proj_db.cache_threshold != projectModel.cache_threshold:
        proj_db.cache_threshold = projectModel.cache_threshold
        changed = True

    if projectModel.guard is not None and proj_db.guard != projectModel.guard:
        proj_db.guard = projectModel.guard
        changed = True

    if projectModel.human_name is not None and proj_db.human_name != projectModel.human_name:
        proj_db.human_name = projectModel.human_name
        changed = True

    if projectModel.human_description is not None and proj_db.human_description != projectModel.human_description:
        proj_db.human_description = projectModel.human_description
        changed = True

    if projectModel.tools is not None and proj_db.tools != projectModel.tools:
        proj_db.tools = projectModel.tools
        changed = True

    if projectModel.public is not None and proj_db.public != projectModel.public:
        proj_db.public = projectModel.public
        changed = True

    if projectModel.default_prompt is not None and proj_db.default_prompt != projectModel.default_prompt:
        proj_db.default_prompt = projectModel.default_prompt
        changed = True

    if projectModel.entrances is not None:
        proj_db.entrances = []
        for entrance in projectModel.entrances:
            proj_db.entrances.append(RouterEntrancesDatabase(
                name=entrance.name, description=entrance.description, destination=entrance.destination,
                project_id=proj_db.id))
        changed = True

    if changed:
        update_project(db)

    return True
