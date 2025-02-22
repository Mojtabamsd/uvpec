# Extraction of features (based on Fabio's code - WISIP)
from uvpec.custom import get_uvp6_features
import os
import pandas as pd

def extract_features(path_to_subfolders, use_C):
    """
    Function that extracts features from images of plankton given in specific subfolders.
    It outputs a dataset of features with their associated label.
    """
    
    # https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
    # Lists of all subfolders within the path_to_subfolders
    _, folderList, _ = next(os.walk(path_to_subfolders))
    
    # split taxon names and their IDs from EcoTaxa
    folderList_splitted = [folder.split('_') for folder in folderList]

    # create a dict with taxon names and their relevant ID 
    dico_id = {folderList_splitted[i][0] : folderList_splitted[i][1] for i in range(len(folderList_splitted))}
    #dico_id = {folderList_splitted[i][0] : i for i in range(len(folderList_splitted))} ## TBD, here we just assign pseudo-random numbers and not their EcoTaxa IDs.

    # back to regular list with only taxon names
    folderList_splitted = list(dico_id.keys())

    # saveguard : the number of image folders should not be greater than 40 (technical limit, see with Marc Picheral/Fabio Dias/Camille Catalano)
    if len(folderList) > 40:
        raise ValueError('Max number of classes is 40.')

    # Threshold value used to split image pixels into foreground (> threshold) and background (<= threshold) pixels.
    threshold = 20 # ATTENTION here
    
    # create empty lists to construct the dataset
    Features = list()
    labels = list()

    for folder in folderList:
        print(folder)
        _, _, images = next(os.walk(os.path.join(path_to_subfolders, folder)))
        for image in images:
            label = folder.split('__')[0]

            # get thumbnail features using the uvp6lib function and append to dataset
            F = get_uvp6_features(os.path.join(path_to_subfolders, folder, image), threshold, use_C)
            if len(F) > 0:  # test if feature extraction succeeded before appending to dataset
                Features.append(F)
                labels.append(label)

    # turn dataset into a Pandas Dataframe and extract number of classes
    dataset = pd.DataFrame(Features)
    dataset['labels'] = labels
    
    return(dataset, dico_id)
