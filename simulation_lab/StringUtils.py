# This class can be used for general public utility methods

# Sadly, in python the best way to check if a string is a float is to blindly try inside a try-except statement
def getFloatOrNone(val):
    try:
        return float(val)
    except:
        return None

