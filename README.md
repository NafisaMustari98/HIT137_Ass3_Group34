Open your terminal and create a virtual environment with this command
python -m venv ai_env

Activate your environment with this command
.\ai_env\Scripts\activate

Install all the required libraries with these commands.
# 1. Install core tools
pip install setuptools==65.5.0 wheel

# 2. Install numerical core
pip install numpy==1.24.4

# 3. Install the stable TensorFlow version for Python 3.9
pip install tensorflow==2.10.0 keras==2.10.0

# 4. Install the high-level interface
pip install transformers==4.30.0 pillow

#5. Install the pytorch
pip install torch

Now run this, $env:KMP_DUPLICATE_LIB_OK="TRUE"
Then, finally, run the project with this command python main_app.py
