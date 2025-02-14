import pandas as pd
from scipy.io import loadmat
import os
import argparse


def export_mat_data(import_dir: str, export_dir: str, import_suffix: str = '.mat'):
    """This function loads the .mat data files and saves them as separate csv files
    for Holter data and the watch prototype data

    Args:
        import_dir (str): dir of .mat files
        export_dir (str): where to save .csv files
        import_suffix (str, optional): the suffix of the data files. Defaults to '.mat'.
    """
    # if the export dit doesn't exist, create it
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    # get the list of the files
    files = os.listdir(import_dir)
    # loop over the files and save them in export dir
    index = 0
    while index < len(files):
        filename = files[index]
        if filename.endswith(import_suffix):
            data = loadmat(os.path.join(import_dir,filename))
            
            subject_hr_data = pd.DataFrame(columns = ['timeECG','bpmECG'])
            for col in subject_hr_data.columns:
                subject_hr_data[col] = data[col].flatten()
            # save the Holter data as a csv file in the export dir
            subject_hr_data.to_csv(os.path.join(export_dir,filename[:-len(import_suffix)]+'_ECG.csv'), index=False)
            
            subject_sensor_data = pd.DataFrame(columns = ['sigPPG_1','sigPPG_2','sigPPG_3',
            'sigAcc_1','sigAcc_2','sigAcc_3',
            'sigGyro_1','sigGyro_2','sigGyro_3'])
            senesor_data_keys  = [i for i in data.keys() if '__' not in i and 'ECG' not in i]
            for key_ in senesor_data_keys:
                for sensor_count in range(1,4):
                    subject_sensor_data[key_+'_'+str(sensor_count)] = data[key_][sensor_count-1]
            # save the watch data as a csv file in the export dir
            subject_sensor_data.to_csv(os.path.join(export_dir,filename[:-len(import_suffix)]+'_watch.csv'), index=False)
        index += 1

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--import_dir', type=str, help='Input file path', default='og_mat')
    parser.add_argument('--export_dir', type=str, help='Output file path', default='exported_csv')
    args = parser.parse_args()

    export_mat_data(args.import_dir, args.export_dir)