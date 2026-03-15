# Adapted from bug36/03_if_try.py
# Bug: parsing if with try/return inside
def info(md5hash, datahash, results):
    if md5hash == datahash:
        try:
            return md5hash
        except:
            return results
