'''Instructions: save the raw data file as 'national_park_trails.csv' and then run this code
in the same directory as the csv file.
This script does the following:
1. Converts the string containing latitude and longitude into two new columns.
2. Converts features list into columns and adds a 1 if the feature is present, and a 0 if it is not.
3. Converts activities list into columns and adds a 1 if the feature is present, and a 0 if it is not.

Returns: A pre-cleaned dataframe from the 'national_park_trails.csv' file.'''


def cleanit():
    import pandas as pd
    import ast
    import os
    import time

    # Start measuring the time of this script
    start_time = time.time()
    
    #load the dataset in to a dataframe
    parks_data=pd.read_csv('national_park_trails.csv')

    #split off features into list of unique values
    unique_features=[]
    for index, row in parks_data.iterrows():
        features=ast.literal_eval(row['features'])
        for feature in features:
            if feature not in unique_features:
                unique_features.append(feature)


    #split off activities into list of unique values
    unique_activities=[]
    for index, row in parks_data.iterrows():
        activities=ast.literal_eval(row['activities'])
        for activity in activities:
            if activity not in unique_activities:
                unique_activities.append(activity)


    #extracting lat/lon from each into a list
    latlist=[]
    lonlist=[]
    for index,row in parks_data.iterrows():
        lat_lon_dict=ast.literal_eval(row['_geoloc'])
        lat=lat_lon_dict['lat']
        lon=lat_lon_dict['lng']
        latlist.append(lat)
        lonlist.append(lon)


    #adding separate lat and lon columns to parks_data and inserting the data
    parks_data['lat']=latlist
    parks_data['lon']=lonlist


    #verifying that the insertion worked correctly
    correct_count=0
    for index, row in parks_data.iterrows():
        geoloc_dict=ast.literal_eval(row['_geoloc'])
        geoloc_lat=geoloc_dict['lat']
        geoloc_lon=geoloc_dict['lng']
        if row['lat']==geoloc_lat and row['lon']==geoloc_lon:
            correct_count +=1
        else:
            print('lat/lon disagreement for ' + row['name'])
    print('The number of rows in the dataframe is: ' + str(len(parks_data.index)))
    print('If this number matches the number of trails in the file, lat/lon split correctly: ' + str(correct_count))

    should_continue=input('If lat/lon appears to have split correctly, enter "y" to continue. Otherwise enter any key to abort: ')


    if should_continue=='y' or should_continue=='Y':
        #seeing that the above worked, dropping the _geoloc column from the dataframe
        parks_data.drop(columns=['_geoloc'], inplace = True)


        #split off features and activities into lists of unique values
        print('\nCreating lists for unique features and activities...')
        unique_features=[]
        unique_activities=[]

        for index, row in parks_data.iterrows():
            features=ast.literal_eval(row['features'])
            activities=ast.literal_eval(row['activities'])
            for feature in features:
                if feature not in unique_features:
                    unique_features.append(feature)
            for activity in activities:
                if activity not in unique_activities:
                    unique_activities.append(activity)
        print('List creation complete.\n')

        # Create new columns for each feature in the unique_features list (initailized to 0, but it doesn't matter)
        print('Creating columns in dataframe for unique features...')
        for item in unique_features:
            parks_data[item] = 0

        # Loop through each row in the dataframe
        for index, row in parks_data.iterrows():
            # Grab a list of the features for the current row
            features=ast.literal_eval(row['features'])

            # Loop through each item in the unique_features list
            for item in unique_features:
                # If the item is in the features list that we created for the row
                if item in features:
                    # Change the value of the appropriate column to a 1
                    parks_data.loc[index, item] = 1
                else:
                    # Otherwise it is not present, and we leave it as a 0
                    parks_data.loc[index, item] = 0

        print('Column creation and fill complete for features.\n')
        
        # Create new columns for each activities in the unique_activities list (initailized to 0, but it doesn't matter)
        print('Creating columns in dataframe for unique activities...')
        for item in unique_activities:
            parks_data[item] = 0

        # Loop through each row in the dataframe
        for index, row in parks_data.iterrows():
            # Grab a list of the activities for the current row
            activities=ast.literal_eval(row['activities'])
            # Loop through each item in the unique_activities list
            for item in unique_activities:
                # If the item is in the activities list that we created for the row
                if item in activities:
                    # Change the value of the appropriate column to a 1
                    parks_data.loc[index, item] = 1
                else:
                    # Otherwise it is not present, and we leave it as a 0
                    parks_data.loc[index, item] = 0

        print('Column creation and fill complete for activities.\n')
        
        print('Dropping unncessary features and activities columns.\n')
        parks_data.drop(columns=['features', 'activities'], inplace = True)

        """
        Commented out the below code because we don't need to create the brand new CSV file.
        If you want to create a new CSV file, uncomment this block.
        
        #############################
        # Get the working directory #
        #############################
        working_dir = os.getcwd()

        #writing parks_data with separate lat/lon to a new csv to preserve original dataset
        parks_data.to_csv('national_park_trails_rev2.csv', index = False)
        new_csv_path=os.path.join(working_dir,'national_park_trails_rev2.csv')
        print('Wrote new CSV with updated latitude and longitude: ' + str(new_csv_path) + '\n')


        #importing the new sheet to double check
        print('A sample of your cleaned up data: ')
        parks_data_rev2=pd.read_csv('national_park_trails_rev2.csv')
        print(parks_data_rev2.head(5))
        """

        # Measure the time the script ended
        end_time = time.time()
        
        print('Complete!')
        print(f'This script ran in {end_time - start_time:.2f} seconds.')
    else:
        print('Aborted data cleanup script.')
        sys.exit(0)

    return parks_data