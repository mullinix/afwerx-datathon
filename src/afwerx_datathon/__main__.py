"""Command line interface for afwerx-datathon.

See https://docs.python.org/3/using/cmdline.html#cmdoption-m for why module is
named __main__.py.
"""


from typer import Typer


app = Typer(help="Data science pipelines for the AFWERX Datathon, 2021.")


if __name__ == "__main__":
    app()
