import argparse
from task_manager.tasks import add, complete, delete, show, ensure_file


def main(argv=None):
    ensure_file()
    parser = argparse.ArgumentParser(prog='task-manager')
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('title', help='Title of the task')
    add_parser.add_argument('-d', '--description', default='', help='Task description')
    add_parser.add_argument('-p', '--priority', default='medium',
                            choices=['low', 'medium', 'high'],
                            help='Task priority (default: medium)')

    complete_parser = subparsers.add_parser('complete', help='Mark a task complete')
    complete_parser.add_argument('task_id', type=int, help='ID of the task to complete')

    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('task_id', type=int, help='ID of the task')

    show_parser = subparsers.add_parser('show')

    args = parser.parse_args(argv)

    if args.command == 'add':
        result = add(args.title, description=args.description, priority=args.priority)
        print(result)
    elif args.command == 'complete':
        result = complete(args.task_id)
        print(result)
    elif args.command == 'delete':
        result = delete(args.task_id)
        print(result)
    elif args.command == 'show':
        for task in show():
            status = "✓" if task.completed else " "
            print(f"[{status}] {task.id}: {task.title} ({task.priority.value})")


if __name__ == '__main__':
    main()
