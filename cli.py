import click

from breeze_bot.cli.api import start


@click.group()
def main():
    pass


main.add_command(start)

if __name__ == '__main__':
    main()
