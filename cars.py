import collections, os, json
import pandas as pd


def process_carfile(dir_path):
    carsfiles_list = os.listdir(dir_path)

    carsfile_name = [name.split(".mp4")[0] for name in carsfiles_list if name != ".DS_Store"]
    
    # creat a carfile_dict
    carfile_dict = collections.defaultdict(list)

    for carsfile in carsfile_name:
        if len(carsfile.split("_")) == 6:
            cars = "_".join(carsfile.split("_")[:2])
            cars_color =  carsfile.split("_")[2]
            carfile_dict[cars].append(cars_color) 
        else:
            print("Is len not 6:", carsfile)
    
    return carfile_dict

def to_pandas(carfile_dict, path_info):
    
    cars_df = pd.DataFrame([carfile_dict.keys(), carfile_dict.values()]).T
    
    # Processing car_name
    cars_df["car_name"] = cars_df[0].apply(lambda x : x.split("_")[0])
    # Processing car_year
    cars_df["car_year"] = cars_df[0].apply(lambda x : x.split("_")[1])
    # Processing repetition color
    cars_df["color"] = cars_df[1].apply(lambda x : list(set(x)))
    # count car color
    cars_df["color_count"] = cars_df["color"].apply(lambda x : len(x))
    # Processing values split "["  "]", replace " ' "
    cars_df["color"] = cars_df["color"].apply(lambda x : str(x).split("[")[1].split("]")[0].replace("'",""))
    # drop columns 0 and 1
    cars_df = cars_df.drop([0,1], axis=1)
    
    # to_csv
    filepath = path_info['filepath']
    if os.path.isfile(filepath): 
        cars_df.to_csv("./carfileinfo.csv", 'a', encoding='utf-8-sig', index=False)
    else:
        cars_df.to_csv("./carfileinfo.csv",encoding='utf-8-sig', index=False)
    
    return cars_df

def to_mysql(cars_df):
    cars_df["incvat"] = "0"
    print(cars_df)




if __name__ == "__main__":

    path = "./any.txt"
    with open(path,'r') as f:
        path_info = json.loads(f.read())

    # get dirpath    
    dir_path = path_info['dir_path']
    
   
    carfile_name = process_carfile(dir_path)
    topandas = to_pandas(carfile_name , path_info) 
    to_mysql(topandas)     

