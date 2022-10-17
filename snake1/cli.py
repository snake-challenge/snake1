import click

from snake1.prepare import prepare
from snake1.meta import cli as meta
from snake1.task import Task
from snake1.score import score

main = click.Group(commands=[prepare, meta, Task.cli, score])

if __name__ == "__main__":
    main()
