import os

# Suppress Intel MKL error on some systems
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'