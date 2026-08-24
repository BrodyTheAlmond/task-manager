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
    return f'{task} has been added to Task Manager'


def complete(index, file_path=DEFAULT_PATH):
    task = pd.read_csv(file_path)
    if index < len(task):
        task.loc[index, 'Completed'] = 'yes'
        task.to_csv(file_path, index=False)
        return f'{task.loc[index, "Task"]} has been completed in Task Manager'
    else:
        return 'chosen index is out of range or invalid'


def delete(index, file_path=DEFAULT_PATH):
    task = pd.read_csv(file_path)
    if index < len(task):
        task = task.drop(index=index).reset_index(drop=True)
        task.to_csv(file_path, index=False)
        return f'{task.loc[index, "Task"]} has been removed from Task Manager'
    else:
        return 'chosen index is out of range or invalid'


def show(file_path=DEFAULT_PATH):
    task = pd.read_csv(file_path)
    return task
