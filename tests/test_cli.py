from unittest.mock import patch
from src.task_manager.cli import main


def test_add_command_calls_add():
    with patch('task_manager.cli.add') as mock_add, \
         patch('task_manager.cli.ensure_file'):
        main(['add', 'buy milk'])
        mock_add.assert_called_once_with('buy milk')


def test_complete_command_calls_complete_with_int_index():
    with patch('task_manager.cli.complete') as mock_complete, \
         patch('task_manager.cli.ensure_file'):
        main(['complete', '2'])
        mock_complete.assert_called_once_with(2)  # note: int, not string '2'


def test_delete_command_calls_delete():
    with patch('task_manager.cli.delete') as mock_delete, \
         patch('task_manager.cli.ensure_file'):
        main(['delete', '0'])
        mock_delete.assert_called_once_with(0)


def test_show_command_calls_show():
    with patch('task_manager.cli.show') as mock_show, \
         patch('task_manager.cli.ensure_file'):
        main(['show'])
        mock_show.assert_called_once()