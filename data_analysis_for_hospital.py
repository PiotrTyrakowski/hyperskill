import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', 8)


general = pd.read_csv("test/general.csv")
prenatal = pd.read_csv("test/prenatal.csv")
sports = pd.read_csv("test/sports.csv")


# rename columns
prenatal.columns = general.columns
sports.columns = general.columns


# merge dataframes into one
merged_df = pd.concat([general, prenatal, sports], ignore_index=True)

# drop Unnamed column
merged_df.drop(["Unnamed: 0"], axis=1, inplace=True)

# Delete all the empty rows
merged_df.dropna(subset=merged_df.columns, how="all", inplace=True)

# Correct all the gender column values to f and m respectively
merged_df["gender"] = merged_df["gender"].replace({"male": "m", "man": "m", "female": "f", "woman": "f"})

# Replace the NaN values in the gender column of the prenatal hospital with f
merged_df.loc[(merged_df["gender"].isna()) & (merged_df["hospital"] == "prenatal"), "gender"] = "f"

# Replace the NaN values in the bmi, diagnosis, blood_test, ecg, ultrasound, mri, xray, children, months columns with zeros
columns_to_replace = ['bmi', 'diagnosis', 'blood_test', 'ecg', 'ultrasound', 'mri', 'xray', 'children', 'months']
merged_df[columns_to_replace] = merged_df[columns_to_replace].fillna(0)


# STAGE 4

# Which hospital has the highest number of patients?
hospital_with_highest_patients = merged_df.groupby("hospital").size().idxmax()
print(f"The answer to the 1st question is {hospital_with_highest_patients}")

# What share of the patients in the general hospital suffers from stomach-related issues?
# Round the result to the third decimal place.
general_stomach_number = len(merged_df[(merged_df.diagnosis == 'stomach') & (merged_df["hospital"] == "general")])
general_all_number = len(merged_df[(merged_df["hospital"] == "general")])
print(f"The answer to the 2nd question is {round(general_stomach_number / general_all_number, 3)}")

# What share of the patients in the sports hospital suffers from dislocation-related issues?
# Round the result to the third decimal place.
sport_dislocation_number = len(merged_df[(merged_df["diagnosis"] == "dislocation") & (merged_df["hospital"] == "sports")])
sport_all_number = len(merged_df[(merged_df["hospital"] == "sports")])
print(f"The answer to the 3nd question is {round(sport_dislocation_number / sport_all_number, 3)}")


# What is the difference in the median ages of the patients in the general and sports hospitals?
general_median_age = merged_df[merged_df["hospital"] == "general"]["age"].median()
sports_median_age = merged_df[merged_df["hospital"] == "sports"]["age"].median()
age_difference = general_median_age - sports_median_age
print(f"The answer to the 4nd question is {age_difference}")

# After data processing at the previous stages, the blood_test column has three values: t = a blood test was taken, f = a blood test wasn't taken, and 0 = there is no information.
# In which hospital the blood test was taken the most often (there is the biggest number of t in the blood_test column among all the hospitals)? How many blood tests were taken?
blood_test_counts = pd.pivot_table(merged_df[merged_df.blood_test == 't'], index='hospital', values='blood_test', aggfunc='count')
hospital_with_most_blood_tests = blood_test_counts['blood_test'].idxmax()
max_blood_tests = blood_test_counts['blood_test'].max()
print(f'The answer to the 5th question is {hospital_with_most_blood_tests}, {max_blood_tests} blood tests')




# STAGE 5


# What is the most common age of a patient among all hospitals?
# Plot a histogram and choose one of the following age ranges: 0-15, 15-35, 35-55, 55-70, or 70-80.


bins = [0, 15, 35, 55, 70, 80]
labels = ['0-15', '15-35', '35-55', '55-70', '70-80']
merged_df['age_range'] = pd.cut(merged_df.age, bins, labels=labels, include_lowest=True)

# Plot histogram
plt.hist(merged_df['age_range'], bins=len(labels), color='skyblue', edgecolor='black')
plt.title('Age Distribution among All Hospitals')
plt.xlabel('Age Range')
plt.ylabel('Number of Patients')
plt.show()

print("The answer to the 1st question: 15-35")

# What is the most common diagnosis among patients in all hospitals? Create a pie chart.

# Count the occurrences of each diagnosis
diagnosis_counts = merged_df['diagnosis'].value_counts()

# Create pie chart
plt.figure(figsize=(10, 6))
plt.pie(diagnosis_counts, labels=diagnosis_counts.index, autopct='%1.1f%%')
plt.title('Most Common Diagnosis among All Hospitals')
plt.show()

print("The answer to the 2nd question: pregnancy")

# Build a violin plot of height distribution by hospitals. Try to answer the questions.
# What is the main reason for the gap in values? Why there are two peaks, which correspond to the relatively small and big values?
# No special form is required to answer this question

# Create violin plot
plt.figure(figsize=(10, 6))
sns.violinplot(x='hospital', y='height', data=merged_df)
plt.title('Height Distribution by Hospitals')
plt.show()

print("The answer to the 3rd question: It's because the height of the patients from the sports hospital was measured in feet, and the height of the patients from the general and prenatal hospital were measured in meters.")
