#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 15:59:08 2020

@author: raskshithakoriraj
"""

import os 
import urllib.request
import tarfile
import pandas as pd
from tqdm import tqdm
import glob





#creating data folder
data_path = "data"
datasetroot_tar = os.path.join(data_path,"nf_prize_dataset.tar.gz")
datasetroot_dir = os.path.join(data_path,"download")
dataset_tar = os.path.join(data_path,"download","training_set.tar")


def main():
    if (os.path.exists(data_path)==False):
        os.mkdir(data_path)
       
    
    
    #Downloading and extractng the tar dataset from Kaggle 
    if os.path.exists(datasetroot_tar)==False:
        print("Downloading...")
        tar_url = 'https://archive.org/download/nf_prize_dataset.tar/nf_prize_dataset.tar.gz'
        filehandle, _ = urllib.request.urlretrieve(tar_url,datasetroot_tar)
    
    if os.path.exists(datasetroot_dir)==False:
        print("Extracting...")
        tar = tarfile.open(datasetroot_tar, "r:gz")
        tar.extractall(data_path)
        tar.close()
        tar = tarfile.open(dataset_tar, "r:")
        tar.extractall(datasetroot_dir)
        tar.close()
            
    #########End of download #########
        
    
    
    #########Combining data and writing to csv file #########
    csv_path = os.path.join(data_path, 'dataset.csv')
    if(os.path.exists(csv_path)==False):    
        dataset_dir = os.path.join(data_path,"download","training_set")
        files = glob.glob(dataset_dir + '/*.txt', recursive=True)
        data_list = []
        for file in tqdm(files):
            file1 = open(file,'r')
            #filepath, file_extension = os.path.splitext(file)
            #print(filepath)
            movie_id = file1.readline()
            movie_id = movie_id.strip()[:-1]
            for line in file1:
                mov_record = [movie_id]
                mov_record.extend(line.strip().split(","))
                data_list.append(mov_record)
                del mov_record
            file1.close()
            
        df = pd.DataFrame(data_list, columns=["movie_id", "customer_id", "ratings", "date"])
        del data_list
        df.to_csv(csv_path, index=False, header=True)
        del df

if __name__ == "__main__":
    main()
