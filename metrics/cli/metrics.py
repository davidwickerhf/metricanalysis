import click

@click.group()
def cli():
    pass

@cli.command()
def list():
    """
    List the available metrics. To add a metric, create a new file under the "metrics" folder
    """
    print("List of available metrics")

if __name__ == "__main__":
    list()