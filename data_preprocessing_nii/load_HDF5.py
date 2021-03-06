import dircache
import os
import h5py
import glob
import nibabel as nb

from os import listdir
from os.path import isfile, join
import random
import csv
import h5py 
import numpy as np
import pdb

path = '/cstor/xsede/users/xs-jdakka/keras_model/3D_fMRI_CNN/standardized_LPF_data/output_data'



def create_dictionary(subject_ID):

  #subject_ID=[]

  #for filename in glob.glob(os.path.join(path, '*.nii')):
  #  split_filename=os.path.basename(filename).split('_')
 #   subject_ID.append(split_filename[2]) 
  
  unique_IDs=[]
  [unique_IDs.append(i) for i in subject_ID if not unique_IDs.count(i)]
  dictionary_IDs={x:i for i,x  in enumerate(unique_IDs, start=1)} 
  for i in range(len(subject_ID)):
    subject_ID[i]= dictionary_IDs[subject_ID[i]]
   
  return unique_IDs

def collect_data():
  
  f=h5py.File('shuffled_output_runs.hdf5','w')
  g=h5py.File('shuffled_output_labels.hdf5','w')
  h=h5py.File('shuffled_output_subjects.hdf5','w')
  i=h5py.File('shuffled_output_features.hdf5', 'w') 


  dset_runs = f.create_dataset("runs", (380,))  
  dset_labels = g.create_dataset("labels", (380,))
  dset_subjects = h.create_dataset("subjects", (380,))
  dset_data=i.create_dataset("features", (380, 53, 64, 37, 137), dtype=np.float64)

  
  
  files=glob.glob('/cstor/xsede/users/xs-jdakka/original_resolution_nonLPF_standardized_masked/data/output_data/*.nii')
  import random
  SEED = 5
  pdb.set_trace()
  #random.seed(SEED) 
  #random.shuffle(files)
  print files[:30]
  runs, subjects, labels, features  = [], [], [], []

  count = 0
  for filename in files:
    
    img=nb.load(filename) # data shape is [x,y,z, time]
    data=img.get_data()
    dset_data[count] = data
    count += 1
    #-1_000353528637_0003_AO_2.nii

    split_filename=os.path.basename(filename).split('_')
    label=split_filename[0]
    dset_labels[:] = label
    subject=split_filename[1]
    dset_subjects[:] = subject
    run=split_filename[4]
    run=os.path.basename(run).split('.')
    run=run[0]
    dset_runs[:] = run

    #runs.append(run)
    #labels.append(label)
    #subjects.append(subject)
    #features.append(data)

  
def load_data():
  """
  Loads the data from HDF5. 

  Parameters
  ----------
  data_file: str

  Returns
  -------
  data: array_like
  """
  
  f=h5py.File('/cstor/xsede/users/xs-jdakka/keras_model/3D_fMRI_CNN/standardized_LPF_data/shuffled_output_runs.hdf5','r')
  g=h5py.File('/cstor/xsede/users/xs-jdakka/keras_model/3D_fMRI_CNN/standardized_LPF_data/shuffled_output_labels.hdf5','r')
  h=h5py.File('/cstor/xsede/users/xs-jdakka/keras_model/3D_fMRI_CNN/standardized_LPF_data/shuffled_output_subjects.hdf5','r')
  i=h5py.File('/cstor/xsede/users/xs-jdakka/keras_model/3D_fMRI_CNN/standardized_LPF_data/shuffled_output_features.hdf5','r')
 
  subjects, labels, features, runs  = [], [], [], []
  
  labels=g['/labels']
  print labels[:30]

'''
  for i in dataset.values():
    subjects.append(i.attrs['subject_ID'])
    labels.append(i.attrs['label'])
    import pdb
    pdb.set_trace()
    runs.append(i.attrs['run'])
    features.append(i[:])
    
  features = np.expand_dims(np.array(features).transpose([4, 0, 3, 1, 2]), axis=2)
 
  subjects=np.array(subjects)
  labels=np.array(labels)
  runs=np.array(runs)

  #print features.shape
  #print runs.shape
  #print runs
  print labels[:30]
  #print subjects.shape
  #print subjects 
'''

#create_dictionary()
collect_data()

#load_data()









 
