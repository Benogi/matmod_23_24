import os

import numpy as np
import requests

class Dataloader:
      def __init__(self, file_url, file_name):
        self.data_folder = "data"
        self.file_path = os.path.join(self.data_folder, file_name)
        self.download(file_url = file_url, file_name = file_name)

        self.data = np.loadtxt(self.file_path)

      def download(self, file_url, file_name):
        os.makedirs(self.data_folder, exist_ok=True) # könyvtár létrehozása, ha már van ilyen = ne csinálja újra
        if not os.path.isfile(self.file_path): # tagadásos feltételkezelés
          r = requests.get(file_url, allow_redirects=True) # megnyitja a weboldalt és letülti a filet, átirányítást=engedélyez
          open(self.file_path, "wb").write(r.content) # wb: írási üzemmód