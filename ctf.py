def function(string):
    result=0
    print(string)
    for s in string:
        result += ord(s)*2
        result &= 0xFF
    return result

def check(string):
    flag="capturedtheflag"
    coded_value=150
    if function(string)==coded_value:
        print(flag)
    else:
        print("incorrect")


