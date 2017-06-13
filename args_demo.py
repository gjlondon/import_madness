# Copyright (c) 2013-2017 Survata, All Rights Reserved


src = ""
with open("with_args.py") as f:
    for line in f:
        src += line

a = "10"
b = "21"

src = src.replace("a = None", f"a = {a}")
src = src.replace("b = None", f"b = {b}")

with open("with_args.py", "w") as f:
    for line in src.split("\n"):
        f.write(line + "\n")

from with_args import result

print(result)  # it's 31!