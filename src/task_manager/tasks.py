from pathlib import Path
from platformdirs import user_data_dir
import pandas as pd

APP_NAME = "TaskManager"
DATA_DIR = Path(user_data_dir(APP_NAME))
DEFAULT_PATH = DATA_DIR / "tasks.csv"
fieldnames = ['Task', 'Completed']


def ensure_file(file_path=DEFAULT_PATH):
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)  # create dir if missing
    if not file_path.is_file():
        pd.DataFrame(columns=fieldnames).to_csv(file_path, index=False)


def add(task, file_path=DEFAULT_PATH):
    ensure_file(file_path)
    new_task = pd.DataFrame([{'Task': task, 'Completed': 'no'}])
    new_task.to_csv(file_path, mode='a', index=False, header=False)


def complete(index, file_path=DEFAULT_PATH):
    tasks = pd.read_csv(file_path)
    tasks.loc[index, 'Completed'] = 'yes'
    tasks.to_csv('tasks.csv', index=False)


def delete(index, file_path=DEFAULT_PATH):
    tasks = pd.read_csv(file_path).drop(index=index).reset_index(drop=True)
    tasks.to_csv('tasks.csv', index=False)


def show(file_path=DEFAULT_PATH):
    tasks = pd.read_csv(file_path)
    return tasks
