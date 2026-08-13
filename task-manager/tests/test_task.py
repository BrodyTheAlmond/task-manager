import pandas as pd
import pytest
from tasks import add, show, complete, delete


@pytest.fixture
def csv_file(tmp_path):
    return tmp_path / "tasks.csv"


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


def test_complete_marks_task_true(csv_file):
    add("wash car", file_path=csv_file)
    complete(0, file_path=csv_file)
    df = pd.read_csv(csv_file)
    assert df.loc[0, 'Completed'] == ''


def test_delete_removes_row(csv_file):
    add("a", file_path=csv_file)
    add("b", file_path=csv_file)
    delete(0, file_path=csv_file)
    df = pd.read_csv(csv_file)
    assert len(df) == 1
    assert df.iloc[0]['Task'] == "b"


def test_complete_invalid_index_raises(csv_file):
    add("only task", file_path=csv_file)
    with pytest.raises(KeyError):
        complete(5, file_path=csv_file)

