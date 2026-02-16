def data_types():
    integer=5
    string="abc"
    f=3.14
    b=True
    mas=[1,2,3]
    d={'a':1,'b':2}
    t=(1,2)
    s={1,2}

    print(f"[{type(integer).__name__}, {type(string).__name__}, {type(f).__name__}, {type(b).__name__}, "
          f"{type(mas).__name__}, {type(d).__name__}, {type(t).__name__}, {type(s).__name__}]")

if __name__ == '__main__':
     data_types()