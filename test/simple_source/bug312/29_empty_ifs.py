# Adapted from bug35/05_empty_ifs.py
# Tests nested if with pass
if __file__:
    if __name__:
        pass
    elif __import__:
        pass
