# Adapted from bug35/01_loop_if_continue.py
# Tests continue as last statement of if
def parse_parts(it, parts):
    for part in it:
        if not part:
            continue
        parts = 1
    return parts

print(parse_parts([], 5))
print(parse_parts([True], 6))
print(parse_parts([False], 6))
