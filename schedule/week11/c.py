import sys

def say_hello(name):
    print(f"Hello, {name}!")

def main():
    name = sys.argv[1] #in array, the first variable [0] is the name of the script, so that's why we do 1
    say_hello(name)

if __name__ == "__main__":
    main()