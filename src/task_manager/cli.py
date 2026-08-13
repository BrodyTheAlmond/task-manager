import argparse
from tasks import add, complete, delete, show, ensure_file


def main(argv=None):
    ensure_file()
    parser = argparse.ArgumentParser(prog='task-manager')
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add')
    add_parser.add_argument('task')

    complete_parser = subparsers.add_parser('complete')
    complete_parser.add_argument('index', type=int)

    delete_parser = subparsers.add_parser('delete')
    delete_parser.add_argument('index', type=int)

    show_parser = subparsers.add_parser('show')

    args = parser.parse_args(argv)

    if args.command == 'add':
        added_task = add(args.task)
        print(added_task)
    elif args.command == 'complete':
        complete(args.index)
    elif args.command == 'delete':
        delete(args.index)
    elif args.command == 'show':
        print(show())


if __name__ == '__main__':
    main()
