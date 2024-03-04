# Import Libraries
# Pandas
import pandas as pd
# LS
from .ls import LS
# Import CSS
from .cs import CSS

# DataManager Class -> Class
class DataManager:

    # Class litarals
    CHAINAGE:str = 'Chainage'
    LEFT:str = 'Left Side'
    RIGHT:str = 'Right Side'
    BACK:str = 'Back Site'
    CENTER:str = 'Intermittent Site'
    FRONT:str = 'Fore Site'
    RAISFALL:str = 'Rise/ Fall'
    REDUCED:str = 'Reduced Level'
    DESCRIPTION:str = 'Description'

    # Class Constructor -> Method
    def __init__(self, data_file: str) -> None:

        # DataFrame
        self.__df:pd.DataFrame = pd.DataFrame()
        # DataFrame data availability
        self.__df_bool:pd.DataFrame = pd.DataFrame()
        # LS list
        self.__ls_data: list = []
        # CSS list
        self.__css_data: list = []

        # Load data
        self.__load_file(location=data_file)
        # Calculate rais/fall
        self.__calculate_raise_fall()
        # Calculate reduced levels
        self.__calculate_reduced_level()
        # Create LS
        self.__create_ls()
        # Create CSS
        self.__create_css()

        #print(self.__ls_data)
        #print(self.__css_data)

        #print(self.__df.to_string())
    
    # Class properies
    @property
    def get_ls_data(self):
        return self.__ls_data
    
    @property
    def get_css_data(self):
        return self.__css_data

    # Load data file -> Method
    def __load_file(self, location: str) -> None:
        # Find file type
        file_name:str = location.split('/')[-1]
        file_type:str = file_name.split('.')[-1]

        # If file type is *.xlsx
        if (file_type == 'xlsx'):
            # Try to load data file
            try:
                # Load file
                self.__df = pd.read_excel(location)
                # Set df_bool
                self.__df_bool = self.__df.notnull()

            # File not found error
            except FileNotFoundError as ex:
                # Print exception
                print(ex)
        
        # If file type is *.ods
        elif (file_type == 'ods'):
            # Try to load data file
            try:
                # Load file
                self.__df = pd.read_excel(location, engine='odf')
                # Set df_bool
                self.__df_bool = self.__df.notnull()
            
            # File not found error
            except FileNotFoundError as ex:
                # Print exception
                print(ex)
   
    # Row data seloctor -> Method
    def __row_data(self, index: int, type: list=[]) -> bool:
        # If type is [0, 0, 0]
        if (type == [0, 0, 0]):
            # Return value
            return (not(self.__df_bool.iloc[index][DataManager.BACK]) and not(self.__df_bool.iloc[index][DataManager.CENTER]) and not(self.__df_bool.iloc[index][DataManager.FRONT]))
        
        # If type is [0, 0, 1]
        elif (type == [0, 0, 1]):
            # Return value
            return (not(self.__df_bool.iloc[index][DataManager.BACK]) and not(self.__df_bool.iloc[index][DataManager.CENTER]) and (self.__df_bool.iloc[index][DataManager.FRONT]))
        
        # If type is [0, 1, 0]
        elif (type == [0, 1, 0]):
            # Return value
            return (not(self.__df_bool.iloc[index][DataManager.BACK]) and (self.__df_bool.iloc[index][DataManager.CENTER]) and not(self.__df_bool.iloc[index][DataManager.FRONT]))
        
        # If type is [0, 1, 1]
        elif (type == [0, 1, 1]):
            # Return value
            return (not(self.__df_bool.iloc[index][DataManager.BACK]) and (self.__df_bool.iloc[index][DataManager.CENTER]) and (self.__df_bool.iloc[index][DataManager.FRONT]))
        
        # If type is [1, 0, 0]
        elif (type == [1, 0, 0]):
            # Return value
            return ((self.__df_bool.iloc[index][DataManager.BACK]) and not(self.__df_bool.iloc[index][DataManager.CENTER]) and not(self.__df_bool.iloc[index][DataManager.FRONT]))
        
        # If type is [1, 0, 1]
        elif (type == [1, 0, 1]):
            # Return value
            return ((self.__df_bool.iloc[index][DataManager.BACK]) and not(self.__df_bool.iloc[index][DataManager.CENTER]) and (self.__df_bool.iloc[index][DataManager.FRONT]))
        
        # If type is [1, 1, 0]
        elif (type == [1, 1, 0]):
            # Return value
            return ((self.__df_bool.iloc[index][DataManager.BACK]) and (self.__df_bool.iloc[index][DataManager.CENTER]) and not(self.__df_bool.iloc[index][DataManager.FRONT]))
        
        # If type is [1, 1, 1]
        elif (type == [1, 1, 1]):
            # Return value
            return ((self.__df_bool.iloc[index][DataManager.BACK]) and (self.__df_bool.iloc[index][DataManager.CENTER]) and (self.__df_bool.iloc[index][DataManager.FRONT]))
        
        # If type is ething else
        else:
            print('Please Enter Correct Type')
    
    # Get cell data -> Method
    def __get_cell_data(self, index: int, column: str) -> None:
        # Get data from df
        data = self.__df.iloc[index][column]
        return data
    
    # Set cell data -> Method
    def __set_cell_data(self, index: int, column: str, value: float) -> None:
        # Set data
        self.__df.at[index, column] = value
    
    # Calculate Raise/Fall -> Method
    def __calculate_raise_fall(self) -> None:
        # If data file loded
        if not(self.__df.empty):
            # Calculate
            for index, row in self.__df_bool.iterrows():
                # If index is 0
                if (index == 0):
                    continue

                # If index is grater than 0
                else:
                    # If row is [1, 0, 0]
                    if (self.__row_data(index=index, type=[1, 0, 0])):

                        # If uper row is [0, 0, 0]
                        if (self.__row_data(index=index-1, type=[0, 0, 0]) and (index-1 == 0)):
                            # Set data
                            self.__set_cell_data(index=index, column=DataManager.RAISFALL, value=0.000)
                        
                        # Else
                        else:
                            print(f'Data Format Error in row {index+1}')
                    
                    # If row is [0, 0, 1]
                    elif (self.__row_data(index=index, type=[0, 0, 1])):

                        # If upper row [1, 0, 1]
                        if (self.__row_data(index=index-1, type=[1, 0, 1])):
                            # Calculate Value
                            value: float = self.__get_cell_data(index=index-1, column=DataManager.BACK) - self.__get_cell_data(index=index, column=DataManager.FRONT)
                            # Set value
                            self.__set_cell_data(index=index, column=DataManager.RAISFALL, value=value)
                        
                        # If upper row is [0, 1, 0]
                        elif (self.__row_data(index=index-1, type=[0, 1, 0])):
                            # Calculate Value
                            value: float = self.__get_cell_data(index=index-1, column=DataManager.CENTER) - self.__get_cell_data(index=index, column=DataManager.FRONT)
                            # Set value
                            self.__set_cell_data(index=index, column=DataManager.RAISFALL, value=value)
                        
                        # Else
                        else:
                            print(f'Data Format Error in row {index+1}')
                    
                    # If row type is [1, 0, 1]
                    elif (self.__row_data(index=index, type=[1, 0, 1])):

                        # If upper row type is [1, 0, 0] or [1, 0, 1]
                        if (self.__row_data(index=index-1, type=[1, 0, 0]) or (self.__row_data(index=index-1, type=[1, 0, 1]))):
                            # Claculate value
                            value: float = self.__get_cell_data(index=index-1, column=DataManager.BACK) - self.__get_cell_data(index=index, column=DataManager.FRONT)
                            # Set data
                            self.__set_cell_data(index=index, column=DataManager.RAISFALL, value=value)
                        
                        # If upper row type is [0, 1, 0]
                        elif (self.__row_data(index=index-1, type=[0, 1, 0])):
                            # Calculate value
                            value: float = self.__get_cell_data(index=index-1, column=DataManager.CENTER) - self.__get_cell_data(index=index, column=DataManager.FRONT)
                            # Set data
                            self.__set_cell_data(index=index, column=DataManager.RAISFALL, value=value)

                        # Else
                        else:
                            print(f'Data Format Error in row {index+1}')
                    
                    # If row type [0, 1, 0]
                    elif (self.__row_data(index=index, type=[0, 1, 0])):

                        # If upper row type [1, 0, 0] or [1, 0, 1]
                        if (self.__row_data(index=index-1, type=[1, 0, 0]) or self.__row_data(index=index-1, type=[1, 0, 1])):
                            # Calculate value
                            value: float = self.__get_cell_data(index=index-1, column=DataManager.BACK) - self.__get_cell_data(index=index, column=DataManager.CENTER)
                            # Set data
                            self.__set_cell_data(index=index, column=DataManager.RAISFALL, value=value)
                        
                        # If upper row type [0, 1, 0]
                        elif (self.__row_data(index=index-1, type=[0, 1, 0])):
                            # Calculate value
                            value: float = self.__get_cell_data(index=index-1, column=DataManager.CENTER) - self.__get_cell_data(index=index, column=DataManager.CENTER)
                            # Set value
                            self.__set_cell_data(index=index, column=DataManager.RAISFALL, value=value)
                        
                        # Else
                        else:
                            print(f'Data Format Error in row {index+1}')

                    # Else
                    else:
                        print(f'Data Format Error in row {index+1}')   

        else:
            print('Data is not loaded corectly')
        
        # Update __df_bool
        self.__df_bool = self.__df.notnull()
    
    # Calculate reduced level -> Method
    def __calculate_reduced_level(self) -> None:

        # Set reduced levels
        for index, row in self.__df_bool.iterrows():
            # If row index is 0
            if (index == 0):
                continue

            # Else
            else:
                # Calculate value
                value: float = self.__get_cell_data(index=index-1, column=DataManager.REDUCED) + self.__get_cell_data(index=index, column=DataManager.RAISFALL)
                # Set data
                self.__set_cell_data(index=index, column=DataManager.REDUCED, value=value)
        
        # Update __df_bool
        self.__df_bool = self.__df.notnull()

    # Create lS objects -> Method
    def __create_ls(self) -> None:
        # Create ls
        for index, row in self.__df_bool.iterrows():

            # If chainage available
            if (self.__df_bool.iloc[index][DataManager.CHAINAGE]):
                
                # Add LS to list
                self.__ls_data.append(
                    LS(
                        chainage=self.__get_cell_data(index=index, column=DataManager.CHAINAGE),
                        redused_level=self.__get_cell_data(index=index, column=DataManager.REDUCED),
                        description=self.__get_cell_data(index=index, column=DataManager.DESCRIPTION)
                        )
                )
    
    # Create CSS object -> Method
    def __create_css(self) -> None:
        # Get data from 
        for index, row in self.__df_bool.iterrows():

            # Temp values
            temp_offsets: list[float] = []
            temp_reduced_levels: list[float] = []
            temp_descriptions: list[str] = []

            # If chainage available
            if (self.__df_bool.iloc[index][DataManager.CHAINAGE]):
            
                count = index + 1

                while ((self.__df_bool.iloc[count][DataManager.LEFT]) or (self.__df_bool.iloc[count][DataManager.RIGHT])):
                    # If left is available
                    if ((self.__df_bool.iloc[count][DataManager.LEFT]) and not(self.__df_bool.iloc[count][DataManager.RIGHT])):
                        # If next is change
                        if (not(self.__df_bool.iloc[count+1][DataManager.LEFT]) and (self.__df_bool.iloc[count+1][DataManager.RIGHT])):
                            # Set values
                            temp_offsets.append(self.__get_cell_data(index=count, column=DataManager.LEFT) * -1)
                            temp_offsets.append(0.0)

                            temp_reduced_levels.append(self.__get_cell_data(index=count, column=DataManager.REDUCED))
                            temp_reduced_levels.append(self.__get_cell_data(index=index, column=DataManager.REDUCED))

                            temp_descriptions.append(self.__get_cell_data(index=count, column=DataManager.DESCRIPTION))
                            temp_descriptions.append(self.__get_cell_data(index=index, column=DataManager.DESCRIPTION))
                        
                        # If not
                        else:
                            temp_offsets.append(self.__get_cell_data(index=count, column=DataManager.LEFT) * -1)
                            temp_reduced_levels.append(self.__get_cell_data(index=count, column=DataManager.REDUCED))
                            temp_descriptions.append(self.__get_cell_data(index=count, column=DataManager.DESCRIPTION))
                    
                    # If right available
                    elif (not(self.__df_bool.iloc[count][DataManager.LEFT]) and (self.__df_bool.iloc[count][DataManager.RIGHT])):
                          # If next is change
                        if ((self.__df_bool.iloc[count+1][DataManager.LEFT]) and not(self.__df_bool.iloc[count+1][DataManager.RIGHT])):
                            # Set values
                            temp_offsets.append(self.__get_cell_data(index=count, column=DataManager.RIGHT))
                            temp_offsets.append(0.0)

                            temp_reduced_levels.append(self.__get_cell_data(index=count, column=DataManager.REDUCED))
                            temp_reduced_levels.append(self.__get_cell_data(index=index, column=DataManager.REDUCED))

                            temp_descriptions.append(self.__get_cell_data(index=count, column=DataManager.DESCRIPTION))
                            temp_descriptions.append(self.__get_cell_data(index=index, column=DataManager.DESCRIPTION))
                        
                        # If not
                        else:
                            temp_offsets.append(self.__get_cell_data(index=count, column=DataManager.RIGHT))
                            temp_reduced_levels.append(self.__get_cell_data(index=count, column=DataManager.REDUCED))
                            temp_descriptions.append(self.__get_cell_data(index=count, column=DataManager.DESCRIPTION))  
                    
                    # Else
                    else:
                        break

                    # Increse count
                    count = count + 1

            # Else
            else:
                continue

            # Create CSS object and add to css list
            self.__css_data.append(
                CSS(
                    chainage=self.__get_cell_data(index=index, column=DataManager.CHAINAGE),
                    offsets=temp_offsets,
                    redused_levels=temp_reduced_levels,
                    descriptions=temp_descriptions
                )
            )