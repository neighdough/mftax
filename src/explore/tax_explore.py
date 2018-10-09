import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv, find_dotenv
import matplotlib.pyplot as plt
import click

@click.group()
def main():
    pass

@main.command()
@click.option("--last", type=click.IntRange(2, 20))
def hello(last):
    print("Hello {}".format(last))

@main.command()
@click.option("--name")
def goodbye(name):
    print("Goodbye {}".format(name))

    # if method==1:
        # hello()
    # elif method==2:
        # goodbye()
    # elif method==3:
        # hello()
        # goodbye()


if __name__=="__main__":
    main()

