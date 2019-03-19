import click
from mfcc_full_track_analyzer import TrackMFCCExtractor


@click.group()
def g():
    pass


@click.command()
@click.argument('filepath', required=True)
@click.argument('exportpath', required=True)
def analyzer_single(filepath, exportpath):
    analyzer = TrackMFCCExtractor(filepath)
    analyzer.run()
    analyzer.export(exportpath)
    click.echo("Track analyzed successfully")


g.add_command(analyzer_single)


if __name__ == '__main__':
    g()
