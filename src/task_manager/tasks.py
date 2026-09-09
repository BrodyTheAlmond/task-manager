import enum
from pathlib import Path
from platformdirs import user_data_dir
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy import Integer, String, Boolean, Enum, create_engine, select



class Base(DeclarativeBase):
    pass


class PriorityLevel(enum.Enum):
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'


APP_NAME = 'TaskManager'
DATA_DIR = Path(user_data_dir(APP_NAME))
DEFAULT_PATH = DATA_DIR / 'tasks.db'


class Task(Base):
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    priority: Mapped[PriorityLevel] = mapped_column(Enum(PriorityLevel), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False)


def get_engine(file_path=DEFAULT_PATH):
    return create_engine(f'sqlite:///{file_path}')


def ensure_file(file_path=DEFAULT_PATH):
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)  # create dir if missing
    engine = get_engine(file_path)
    Base.metadata.create_all(engine)  # creates tables if they don't exist
    return engine


def add(title, description='', priority='medium', file_path=DEFAULT_PATH):
    engine = ensure_file(file_path)
    with Session(engine) as session:
        new_task = Task(
            title=title,
            description=description,
            priority=PriorityLevel(priority),
            completed=False
        )
        session.add(new_task)
        session.commit()
    return f'{title} has been added to Task Manager'


def complete(task_id, file_path=DEFAULT_PATH):
    engine = ensure_file(file_path)
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if task is None:
            return f'chosen id is out of range or invalid: {task_id}'
        task.completed = True
        session.commit()
        return f'{task.title} has been completed in Task Manager'


def delete(task_id, file_path=DEFAULT_PATH):
    engine = ensure_file(file_path)
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if task is None:
            return f'chosen id is out of range or invalid: {task_id}'
        title = task.title
        session.delete(task)
        session.commit()
        return f'{title} has been removed from Task Manager'


def show(file_path=DEFAULT_PATH):
    engine = ensure_file(file_path)
    with Session(engine) as session:
        return session.scalars(select(Task)).all()
