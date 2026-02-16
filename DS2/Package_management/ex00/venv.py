#!/usr/bin/env python3
import os

def main():
    print(f"Your current virtual env is {os.environ.get('VIRTUAL_ENV')}")

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(error)