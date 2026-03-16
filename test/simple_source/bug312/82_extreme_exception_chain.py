# EXTREME: complex exception hierarchy + reraise + exception chaining + nested finally
# Maximum try/except/else/finally complexity

class AppError(Exception):
    def __init__(self, msg, code=0):
        super().__init__(msg)
        self.code = code

class ValidationError(AppError):
    pass

class ProcessingError(AppError):
    pass

def process_level3(val):
    try:
        if val < 0:
            raise ValidationError("negative", code=-1)
        elif val == 0:
            raise ProcessingError("zero", code=0)
        return val * 2
    except ValidationError:
        raise
    except ProcessingError as pe:
        raise RuntimeError("wrapped") from pe

def process_level2(val):
    try:
        result = process_level3(val)
    except ValidationError as ve:
        try:
            return process_level3(abs(val))
        except Exception:
            return -999
        finally:
            print("level2_inner_finally")
    except RuntimeError as re:
        try:
            raise ProcessingError("retry_failed", code=2) from re
        except ProcessingError:
            return -1
        else:
            return -2
        finally:
            print("level2_reraise_finally")
    else:
        return result
    finally:
        print("level2_outer_finally")

def process_level1(val):
    try:
        try:
            try:
                return process_level2(val)
            except Exception as e:
                raise AppError("level1_wrap") from e
            finally:
                print("level1_inner_finally")
        except AppError as ae:
            print(f"AppError: {ae}, code={ae.code}")
            return -100
        finally:
            print("level1_mid_finally")
    finally:
        print("level1_outer_finally")

print("=== positive ===")
print(process_level1(5))
print("=== negative ===")
print(process_level1(-3))
print("=== zero ===")
print(process_level1(0))
