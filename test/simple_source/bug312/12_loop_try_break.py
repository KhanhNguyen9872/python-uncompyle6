# Adapted from bug38/03_loop_try_break.py
# Test break inside try in a loop
while True:
    try:
        x = 1
        break
    except Exception:
        pass
