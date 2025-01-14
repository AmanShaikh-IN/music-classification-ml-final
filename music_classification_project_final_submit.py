# -*- coding: utf-8 -*-
"""Music_Classification_Project_Final_Submit.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DnUalEcGETrKEVtCTg1G_x5vSzcwiBCJ
"""

import numpy as np
import pandas as pd
import os
import shutil
from google.colab import files
from google.colab import drive
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

sns.set()
drive.mount("/content/drive", force_remount = True)

for dir, subdir, files in os.walk("/content/drive/MyDrive"):
  print(dir, subdir, files, sep = "\n")
  print()

file_path = "/content/drive/MyDrive/MLProcessAZ/Project_Data"
raw_data = pd.read_csv(file_path)