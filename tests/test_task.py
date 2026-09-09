from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy import Integer, String, Boolean, Enum, create_engine, select
from task_manager.tasks import add, show, complete, delete, ensure_file, Task, PriorityLevel
import pytest
import enum


@pytest.fixture
def database(tmp_path):
    return tmp_path / "tasks.db"


def test_ensure_file_creates_parent_dir(database):
    ensure_file(database)
    assert database.parent.is_dir()


def test_ensure_file_creates_file_when_missing(database):
    assert not database.exists()
    ensure_file(database)
    assert database.is_file()


def test_ensure_file_does_not_overwrite_existing_data(tmp_path):
    file_path = tmp_path / "tasks.db"
    engine = ensure_file(file_path)
    with Session(engine) as session:
        new_task = Task(
            title='test',
            description='description',
            priority=PriorityLevel('high'),
            completed=False
        )
        session.add(new_task)
        session.commit()

    engine = ensure_file(file_path)
    with Session(engine) as session:
        tasks = session.scalars(select(Task)).all()
    first_row = [tasks[0].title, tasks[0].description,  tasks[0].priority.value, tasks[0].completed]
    assert len(tasks) == 1
    assert first_row == ['test', 'description', 'high', False]


def test_add_creates_one_row(database):
    add('test', 'description', 'high', file_path=database)
    engine = ensure_file(database)
    with Session(engine) as session:
        tasks = session.scalars(select(Task)).all()
    first_row = [tasks[0].title, tasks[0].description, tasks[0].priority.value, tasks[0].completed]
    assert len(tasks) == 1
    assert first_row == ['test', 'description', 'high', False]


def test_add_appends_not_overwrites(database):
    add('test1', 'description1', 'high', file_path=database)
    add('test2', 'description2', 'low', file_path=database)
    engine = ensure_file(database)
    with Session(engine) as session:
        tasks = session.scalars(select(Task)).all()
    rows = [[task.title, task.description, task.priority.value, task.completed] for task in tasks]
    assert len(tasks) == 2
    assert rows[0] == ['test1', 'description1', 'high', False]
    assert rows[1] == ['test2', 'description2', 'low', False]


def test_complete_marks_task_(database):
    add('test', 'description', 'high', file_path=database)
    complete(1, file_path=database)
    engine = ensure_file(database)
    with Session(engine) as session:
        tasks = session.scalars(select(Task)).all()
    first_row = [tasks[0].title, tasks[0].description, tasks[0].priority.value, tasks[0].completed]
    assert first_row == ['test', 'description', 'high', True]


def test_delete_removes_row(database):
    add('test1', 'description1', 'high', file_path=database)
    add('test2', 'description2', 'low', file_path=database)
    delete(1, file_path=database)
    engine = ensure_file(database)
    with Session(engine) as session:
        tasks = session.scalars(select(Task)).all()
    first_row = [tasks[0].title, tasks[0].description, tasks[0].priority.value, tasks[0].completed]
    assert len(tasks) == 1
    assert first_row == ['test2', 'description2', 'low', False]


def test_delete_removes_middle_row(database):
    add('test1', 'description1', 'high', file_path=database)
    add('test2', 'description2', 'low', file_path=database)
    add('test3', 'description3', 'high', file_path=database)
    add('test4', 'description4', 'low', file_path=database)
    delete(2, file_path=database)
    delete(3, file_path=database)
    engine = ensure_file(database)
    with Session(engine) as session:
        tasks = session.scalars(select(Task)).all()
    rows = [[task.title, task.description, task.priority.value, task.completed] for task in tasks]
    assert rows[0] == ['test1', 'description1', 'high', False]
    assert rows[1] == ['test4', 'description4', 'low', False]


def test_complete_does_not_accept_invalid_index(database):
    add("only task", file_path=database)
    assert complete(5, file_path=database) == 'chosen id is out of range or invalid: 5'


def test_delete_does_not_accept_invalid_index(database):
    add("only task", file_path=database)
    assert delete(5, file_path=database) == 'chosen id is out of range or invalid: 5'


def test_show_returns_model_object(database):
    add('test1', 'description1', 'high', file_path=database)
    add('test2', 'description2', 'low', file_path=database)
    tasks = show(database)
    rows = [[task.title, task.description, task.priority.value, task.completed] for task in tasks]
    assert rows == [
        ['test1', 'description1', 'high', False],
        ['test2', 'description2', 'low', False]
    ]



