import pandas as pd
import pytest
from task_manager.tasks import add, show, complete, delete, ensure_file


@pytest.fixture
def csv_file(tmp_path):
    return tmp_path / "tasks.csv"


def test_ensure_file_creates_parent_dir(csv_file):
    ensure_file(csv_file)
    assert csv_file.parent.is_dir()


def test_ensure_file_creates_file_when_missing(csv_file):

    assert not csv_file.exists()
    ensure_file(csv_file)
    assert csv_file.is_file()


def test_ensure_file_does_not_overwrite_existing_data(tmp_path):
    # Arrange: a file that already has real data in it
    file_path = tmp_path / "tasks.csv"
    pd.DataFrame([{"Task": "buy milk", "Completed": "no"}]).to_csv(
        file_path, index=False
    )
    ensure_file(file_path)
    df = pd.read_csv(file_path)
    assert len(df) == 1
    assert df.loc[0, "Task"] == "buy milk"


def test_add_creates_one_row(csv_file):
    add("buy milk", file_path=csv_file)
    df = pd.read_csv(csv_file)
    assert len(df) == 1
    assert df.loc[0, 'Task'] == "buy milk"
    assert df.loc[0, 'Completed'] == 'no'


def test_add_appends_not_overwrites(csv_file):
    add("task one", file_path=csv_file)
    add("task two", file_path=csv_file)
    df = pd.read_csv(csv_file)
    assert len(df) == 2
    assert list(df['Task']) == ["task one", "task two"]


def test_complete_marks_task_(csv_file):
    add("wash car", file_path=csv_file)
    complete(0, file_path=csv_file)
    df = pd.read_csv(csv_file)
    assert df.loc[0, 'Completed'] == 'yes'


def test_delete_removes_row(csv_file):
    add("a", file_path=csv_file)
    add("b", file_path=csv_file)
    delete(0, file_path=csv_file)
    df = pd.read_csv(csv_file)
    assert len(df) == 1
    assert df.iloc[0]['Task'] == "b"


def test_delete_removes_middle_row(csv_file):
    add("a", file_path=csv_file)
    add("b", file_path=csv_file)
    add("c", file_path=csv_file)
    add("d", file_path=csv_file)
    delete(1, file_path=csv_file)
    delete(1, file_path=csv_file)
    df = pd.read_csv(csv_file)
    assert df.iloc[0]['Task'] == "a"
    assert df.iloc[0]['Task'] == "d"


def test_complete_does_not_accept_invalid_index(csv_file):
    add("only task", file_path=csv_file)
    assert complete(5, file_path=csv_file) == 'chosen index is out of range or invalid'


def test_show_returns_csv_file(csv_file):
    add("a", file_path=csv_file)
    add("b", file_path=csv_file)
    sample_csv = pd.read_csv(csv_file)
    assert show() == sample_csv


