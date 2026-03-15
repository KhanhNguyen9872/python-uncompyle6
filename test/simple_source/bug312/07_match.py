# Tests for 3.12 match/case
x = 5
match x:
    case 1:
        print("one")
    case 2:
        print("two")
    case _:
        print("other")
