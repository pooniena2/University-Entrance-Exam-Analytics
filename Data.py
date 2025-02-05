import pandas as pd

class Data:
    def __init__(self,option):
        self.courses = ["dia","cd","hoa","khtn","su","anh","van","toan","sinh","li"]
        # check option to open the correct file
        try:
            if option == 1:
                dataframe = pd.read_csv("diemthi/2018.csv")
            elif option == 2:
                dataframe = pd.read_csv("diemthi/2019.csv")
            elif option == 3:
                dataframe = pd.read_csv("diemthi/2020.csv")
            self.df = dataframe.apply (pd.to_numeric, errors='coerce')
            del self.df["Unnamed: 0"]
            del self.df ["city"]
        except FileExistsError:
            print("An exception occurred")

    def average_score(self):
        average_score_dict = dict.fromkeys(courses, None)
        for course in self.courses:
            average = self.df[course].mean(skipna= True).round(decimals=2)
            average_score_dict[course] = average
        return average_score_dict

    def get_graph_data(self):
        data = []
        for course in self.courses:
            unique_score = self.df [course].value_counts()
            unique_score.sort_index(inplace = True)
            data.append(unique_score)
        return data
    
    def course_combination(self):
        #code -> combination of the courses
        course_comb={'A':["toan","li","hoa"],'B':["toan","hoa","sinh"],'C':["van","su","dia"],'D':["toan","van","anh"]}
        comb_score = []
        for key in course_comb:
            temp_df = (self.df[course_comb[key]].dropna())
            temp_df = pd.concat([temp_df,pd.DataFrame(temp_df.sum(axis=1),columns=['total'])],axis=1)
            comb_score.append(temp_df)
        return comb_score

    def search_valedictorian(self):
        valedictorian_list = []
        counter = 0
        comb_score = self.course_combination()
        for comb in comb_score :
            _ = comb.loc[comb['total'].idxmax()]
            valedictorian_list.append(_)
            #print(comb['total'].sort_values().max())
        for i in range (0,len(valedictorian_list)):
            if counter == 0:
                print("Valedictorian of A Combination: ")
                print(valedictorian_list[i].to_string())
            elif counter == 1:
                print("Valedictorian of B Combination: ")
                print(valedictorian_list[i].to_string())
            elif counter == 2:
                print("Valedictorian of C Combination: ")
                print(valedictorian_list[i].to_string())
            elif counter == 3:
                print("Valedictorian of D Combination: ")
                print(valedictorian_list[i].to_string())
            counter += 1

    def search_grades(self,ID):
        try:
            ID_int = int (ID)
            df = self.df.set_index('code')
            if self.df['code'].isin([ID]).any():
                print(df.loc[[ID_int]].dropna(axis=1, how='all'))
        except ValueError:
            print("Wrong IDs. Please try again!")
