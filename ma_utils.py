#!/usr/bin/env python3

import click
import sys
from subprocess import call

# cli = click.Group()
@click.group()
def cli(): pass

@cli.command()
@click.argument('cmd')
@click.option('--echo/--no-echo', default=True)
@click.option('--stop/--no-stop', default=True, help='on error')
def cmd(cmd, echo, stop):
    '''Run cmd'''
    def print_error(msg):
        click.echo(click.style(msg, fg='red'), file=sys.stderr)
    if echo:
        click.echo(click.style(cmd, fg='green'))
    try:
        code = call(cmd, shell=True)
    except OSError as e:
        code = -1
        print_error(e)
    if code:
        print_error("error=%i" % code)
        if stop:
            exit(code)

@cli.command()
@click.pass_context
def test(ctx):
    ''' Test cmd '''
    from click.testing import CliRunner
    def _test(task, arg):
        result = CliRunner().invoke(task, arg)
        assert result.exit_code == 0
        return result.output
    assert _test(cmd, ['echo 1']) == 'echo 1\n'
    assert _test(cmd, ['echo 2', '--no-echo']) == ''

    ctx.invoke(cmd, cmd='echo 1')
    ctx.invoke(cmd, cmd='echo 2', echo=False)
    ctx.invoke(cmd, cmd='exit 3', stop=False)
    ctx.invoke(cmd, cmd='echo 4')

if __name__ == '__main__':
    pass
    # test()
    cli()
