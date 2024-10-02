## Training Data folder

## Purpose
All the batch of training data should be in this folder.

# Definition
A batch of training data is made of different dictionnaries or .h5 files output from iEBE-MUSIC.
This batch is contained in a folder inside this directory. 

## Use
To train a model on a batch of training data, simply give the name of the folder in the parameter file.

## Features
The models are trained with potential features. The features corresponds to the additional information 
given to the training procedure to increase the accuracy. 
For instance if the training batch contains data from different nucleus it may be interesting to give 
that information for the training on top of the data = adding a feature to classify the data. 
Doing that allows the model to be trained on a larger set, comprehend what is in comon between 
all training data batches but still understand that the training has sub training categories.

This can be done by giving the "DataInformation" parameter in the parameter file. 
This is a list containing a list for each a training data file as [Nucleus, sqrt(s)].
In sort that:
"DataInformation":[[Au, 19.6], [Ru, 200], [Au, 7.7], ...]


If the DataInformation is not set up (or not setup properly), the models are trained 
without features. 
