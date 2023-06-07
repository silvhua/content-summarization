import pandas as pd
import pickle
from datetime import datetime
import json

# 2022-10-27 17:02 Update the sampling function to avoid loading entire dataframe.
def load_csv(filename,filepath,column1_as_index=False,truncate=None, usecols=None, sep=','):
    """
    Load a csv file as a dataframe using specified file path copied from windows file explorer.
    Back slashes in file path will be converted to forward slashes.
    Arguments:
    - filepath (raw string): Use the format r'<path>'.
    - filename (string).
    - colum1_as_index (bool): If true, take the first column as the index. 
        Useful when importing CSV files from previously exported dataframes.

    Returns: dataframe object.
    """
    filename = f'{filepath}/'.replace('\\','/')+filename
    df = pd.read_csv(filename, usecols=usecols, sep=sep)
    if column1_as_index==True:
        df.set_index(df.columns[0], inplace=True)
        df.index.name = None
    print('Dataframe shape: ',df.shape)
    print('DataFrame columns:', [col for col in df.columns])
    print('Time completed:', datetime.now())

    if truncate:
        return df.sample(n=truncate,random_state=0)
    else:
        return df

def save_csv(df,filename,path=None,append_version=False, index=True):
    """
    Export dataframe to CSV.
    Parameters:
    - df: Dataframe variable name.
    - filename: Root of the filename.
    - filepath (raw string): Use the format r'<path>'. If None, file is saved in same director.
    - append_version (bool): If true, append date and time to end of filename.
    """
    if path:
        path = f'{path}/'.replace('\\','/')
    if append_version == True:
        filename+=datetime.now().strftime('%Y-%m-%d_%H%M')
    df.to_csv(path+filename+'.csv', index=index)
    print('File saved: ',path+filename+'.csv')
    print('Time completed:', datetime.now())


def savepickle(model,filename, ext='sav', path=None,append_version=False):
    """
    Export object as a pickle.
    Parameters:
    - model: Model variable name.
    - filename: Root of the filename.
    - extension: Extension to append (do not include dot as it will be added)
    - filepath (raw string): Use the format r'<path>'. If None, file is saved in same director.
    - append_version (bool): If true, append date and time to end of filename.
    """
    if path:
        path = f'{path}/'.replace('\\','/')
    if append_version == True:
        filename+=datetime.now().strftime('%Y-%m-%d_%H%M')
    with open (path+filename+'.'+ext, 'wb') as fh:
        pickle.dump(model, fh)
    print('File saved: ',path+filename+'.'+ext)
    print('Time completed:', datetime.now())

def loadpickle(filename,filepath):
    """
    Load a pickled model using specified file path copied from windows file explorer.
    Back slashes in file path will be converted to forward slashes.
    Arguments:
    - filepath (raw string): Use the format r'<path>'.
    - filename (string).
    
    Returns saved object.
    """
    filename = f'{filepath}/'.replace('\\','/')+filename
    object = pickle.load(open(filename, 'rb'))
    print('Time completed:', datetime.now())
    if type(object) == pd.core.frame.DataFrame:
        print('Dataframe shape: ',object.shape)
        print('DataFrame columns:', [col for col in object.columns])
    if type(object) == dict:
        print('Dictionary keys:', [key for key in object.keys()])
    return object

def save_output(df, filename=None, description=None, append_version=True, iteration_id=None,
    csv_path=r'C:\Users\silvh\OneDrive\lighthouse\Ginkgo coding\content-summarization\output\CSV',
    pickle_path=r'C:\Users\silvh\OneDrive\lighthouse\Ginkgo coding\content-summarization\output\pickles'
    ):
    """
    Save an Python object as both pickle and CSV. Automatically create filename using date and time 
    if not provided.
    
    """
    if description:
        filename = f'{description}_{datetime.now().strftime("%Y-%m-%d_%H%M")}'
        append_version = False
    elif filename == None:
        filename = f'{datetime.now().strftime("%Y-%m-%d_%H%M")}_outputs'
        append_version = False
    if iteration_id:
        filename += f'_{"{:02d}".format(iteration_id)}'
    try:
        savepickle(df, filename=filename, path=pickle_path, append_version=append_version)
        print('\tObject saved as pickle')
    except:
        print('Unable to save pickle')
    if (type(df) == pd.core.frame.DataFrame) & (csv_path != None):
        save_csv(df, filename=filename, path=csv_path, append_version=append_version)
        print('\tDataFrame saved as CSV')
    elif (type(df) == dict) & (csv_path != None):
        try:
            save_csv(pd.DataFrame(df), filename=filename, path=csv_path, append_version=append_version)
            print('\tDictionary converted to CSV')
        except:
            print('\tUnable to save CSV')


def save_to_json(obj, filename=None, description='output_dictionary', append_version=False,
    path=r'C:\Users\silvh\OneDrive\lighthouse\Ginkgo coding\content-summarization\output\json'
    ):
    """
    Save Python object as a JSON file.
    Parameters:
    - obj: Python object to be saved.
    - filename: Root of the filename.
    - path (raw string): Use the format r'<path>'. If None, file is saved in same directory as script.
    - append_version (bool): If true, append date and time to end of filename.
    """
    if description:
        filename = f'{description}_{datetime.now().strftime("%Y-%m-%d_%H%M")}'
        append_version = False
    elif filename == None:
        filename = f'{datetime.now().strftime("%Y-%m-%d_%H%M")}_outputs'
        append_version = False
    if path:
        path = f'{path}/'.replace('\\','/')
    if append_version:
        filename += f'_{datetime.now().strftime("%Y-%m-%d_%H%M%S")}'
    filename += '.json'
    with open(path+filename, 'w') as f:
        json.dump(obj, f)
    print(f'Object saved as JSON: {filename}')