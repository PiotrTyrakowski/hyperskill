import pandas as pd
import requests
import os

# scroll down to the bottom to implement your solution

if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('A_office_data.xml' not in os.listdir('../Data') and
        'B_office_data.xml' not in os.listdir('../Data') and
        'hr_data.xml' not in os.listdir('../Data')):
        print('A_office_data loading.')
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/A_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('B_office_data loading.')
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/B_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('hr_data loading.')
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/hr_data.xml', 'wb').write(r.content)
        print('Loaded.')

        # All data in now loaded to the Data folder.





    # STAGE 1

    # Loading data to variables
    a_office_data = pd.read_xml('../Data/A_office_data.xml')
    b_office_data = pd.read_xml('../Data/B_office_data.xml')
    hr_data = pd.read_xml('../Data/hr_data.xml')

    # Changing indexes
    a_office_data.index = [f'A{i}' for i in a_office_data['employee_office_id']]
    b_office_data.index = [f'B{i}' for i in b_office_data['employee_office_id']]
    hr_data.index = [x for x in hr_data["employee_id"]]

    # ANS
    # Print three Python lists containing office A, B, and HR data indexes.

    print("STAGE 1")
    print(a_office_data.index.tolist())
    print(b_office_data.index.tolist())
    print(hr_data.index.tolist())
    




    # STAGE 2

    unified_dataset = pd.concat([a_office_data, b_office_data])
    #print(unified_dataset.head())

    merged_dataset = unified_dataset.merge(hr_data, left_index=True, right_index=True,  indicator=True)

    merged_dataset.drop(columns=["employee_office_id", "employee_id", "_merge"], inplace=True)
    merged_dataset.sort_index(inplace=True)

    #ANS
    # Sort the final dataset by index and print two Python lists: the final DataFrame index and the column names.
    # Output each list on a separate line.

    print("STAGE 2")
    print(list(merged_dataset.index))
    print(list(merged_dataset.columns))




    # STAGE 3


    print("STAGE 3")

    # What are the departments of the top ten employees in terms of working hours? Output a Python list of values

    zad1 = list(merged_dataset.sort_values(by=['average_monthly_hours'], ascending=False)["Department"].head(10).values)
    print(zad1)

    # What is the total number of projects on which IT department employees with low salaries have worked?
    # Output a number;

    zad2 = merged_dataset[(merged_dataset.salary == "low" ) & (merged_dataset.Department == "IT")].iloc[:, 0].values.sum()
    print(zad2)

    # What are the last evaluation scores and the satisfaction levels of the employees A4, B7064, and A3033?
    # Output a Python list where each entry is a list of values of the last evaluation score and the satisfaction level of an employee.
    # The data for each employee should be specified in the same order as the employees' IDs in the question above.
    # Apply the .loc method of pandas to answer the question!

    zad3 = merged_dataset.loc[["A4", "B7064", "A3033"],["last_evaluation", "satisfaction_level"]].values.tolist()
    print(zad3)

    # STAGE 4


    # Write "the countr_bigger_5" function that countr the number of employees who
    # worked on more that five projects.

    def count_bigger_5(series):
        return series[series > 5].size

    # Generate a table according to the boss's needs.
    # the median number of projects the employees in a group worked upon, and how many
    # employees worked on more that five projects
    # the mean and median time spent in the company
    # the share of employees who've had work accidents
    # the mean and standard deviation of the last evaluation score
    # print in in dict format
    table = merged_dataset.groupby("left").agg({"number_project":["median", count_bigger_5], "time_spend_company": ["mean", "median"], "Work_accident":"mean", "last_evaluation":["mean", "std"] })

    print("STAGE 4")
    print(table.round(2).to_dict())

    # STAGE 5

    print("STAGE 5")
    
    
    # The first pivot table is a table that displays departments as rows and the employee's current status
    # (the left column) and their salary level (the salary column) as columns.
    # The values should be the median number of hours employees have worked per month (the average_monthly_hours columns).
    # In the table, the HR boss wants to see only those departments where either one is true:
    
    # For the currently employed: the median value of the working hours of high-salary employees is smaller than the hours of the medium-salary employees,
    # OR: For the employees who left: the median value of working hours of low-salary employees is smaller than the hours of high-salary employees

    zad1 = merged_dataset.pivot_table(index="Department", columns=["left", "salary"], values="average_monthly_hours", aggfunc='median')
    zad1 = zad1.query(" (`(0, 'high')` < `(0, 'medium')` ) |  (`(1, 'low')` < `(1, 'high')` )")
    print(zad1.round(2).to_dict())
    
    # The second pivot table is a table where each row is an employee's time in the company (time_spend_company); 
    # the columns indicate whether an employee has had any promotion (the promotion_last_5years column). 
    # The values are min, max, the mean of the last evaluation score and the satisfaction level (the satisfaction_level and last_evaluation columns). 
    # Filter the table by the following rule: select only those rows where the last mean evaluation score is higher for those who didn't have any promotion than those who had.
    
    
    zad2 = merged_dataset.pivot_table(index="time_spend_company", columns=["promotion_last_5years"], values=["satisfaction_level", "last_evaluation"], aggfunc=['min', 'max', 'mean'])
    zad2 = zad2.query(" `('mean', 'last_evaluation', 0)` > `('mean', 'last_evaluation', 1)` ")
    print(zad2.round(2).to_dict())


