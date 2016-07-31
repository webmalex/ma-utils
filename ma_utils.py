#!/usr/bin/env python3

# import atexit
import click
import sys
from subprocess import call as subprocess_call

def print_color(msg, color, **kargs):
    click.echo(click.style(msg, fg=color), **kargs)
def print_er(msg):
    print_color(msg, 'red', file=sys.stderr)
def print_ok(msg):
    print_color(msg, 'green')

# cli = click.Group()
@click.group()
def cli(): pass

@cli.command()
@click.argument('cmd')
@click.option('--echo/--no-echo', default=True)
@click.option('--stop/--no-stop', default=True, help='on error')
def call(cmd, echo, stop):
    '''Run cmd'''
    return _call(cmd, echo, stop)

def _call(cmd, echo=True, stop=True):
    if echo:
        print_ok(cmd)
    try:
        code = subprocess_call(cmd, shell=True)
    except OSError as e:
        code = -1
        print_er(e)
    if code:
        print_er("error=%i" % code)
        if stop:
            # raise
            exit(code)
    return code

@cli.command()
@click.pass_context
def test(ctx):
    ''' Test cmd '''
    from click.testing import CliRunner
    def run(task, arg):
        result = CliRunner().invoke(task, arg)
        assert result.exit_code == 0
        return result.output
    assert run(call, ['echo 1']) == 'echo 1\n'
    assert run(call, ['echo 2', '--no-echo']) == ''

    ctx.invoke(call, cmd='echo 1')
    ctx.invoke(call, cmd='echo 2', echo=False)
    ctx.invoke(call, cmd='exit 3', stop=False)
    ctx.invoke(call, cmd='exit 4')
    # try: ctx.invoke(call, cmd='exit 4')
    # except: print('ok')
    ctx.invoke(call, cmd='echo 5')

def _test():
    assert _call('echo 1') == 0
    assert _call('echo 2', echo=False) == 0
    assert _call('exit 3', stop=False) == 3
    assert _call('exit 4') == 0
    assert _call('echo 5') != 0

# @atexit.register
# def goodbye():
#     print_er("stop error in script")

if __name__ == '__main__':
    pass
    # test()
    cli()
