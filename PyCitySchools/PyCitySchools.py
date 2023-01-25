#!/usr/bin/env python
# coding: utf-8

# # PyCity Schools Analysis
# 
# * From Direct Summary Analysis, we can see that overall passing rate of students is 65%.
# 
# * From School Summary Analysis, it is clear that Highest performing school is Cabrera High School with highest passing rate (91.33%) and lowest performing school is Rodriguez High School with lowest passing rate(53%)
# 
# * From School Spending Analysis, it can be seen that school with lowest spending per student (<585 per student) performed very well with highest passing rate (90%). Schools with Lower spending per student performed well compared to schools with higher spending per student. School with highest spending per student (645 to 680) underperformed comared to schools with lower spending per student.
# 
# * Overall passing of small sized school and Medium sizeed school is higher compared to large sized schools. There is a vast difference between overall passing rates of medium sized schools and large sized schools.(90% overall passed vs 58% overall passed respectively)
# 
# * Also Charter schools has high overall passing rate compared to District schools. There is a vast difference between the overall passing rates of charter schools and district schools(90% overall passed vs 54% overall passed respectively)
# 

# In[2]:


import pandas as pd


# In[3]:


# read the school data file and store it in a data frame
data_file = "./Resources/schools_complete.csv"
school_df = pd.read_csv(data_file)
school_df.head()


# In[4]:


# read the student data file and store it in a data frame
data_file1 = "./Resources/students_complete.csv"
student_df = pd.read_csv(data_file1)
student_df.head()


# In[5]:


# combine both the files 
combined_data = pd.merge(student_df,school_df,how = "left", on = "school_name")
combined_data


# # District Summary

# In[6]:


# Calculate the total number of unique schools
total_schools = len(combined_data["school_name"].unique())
total_schools


# In[7]:


# Calculate the total number of students
total_students = len(student_df["student_name"])
total_students


# In[8]:


# Calculate the total budget
total_budget = school_df["budget"].sum()
total_budget


# In[9]:


# Calculate the average (mean) math score
avg_math_score = student_df["math_score"].mean()
avg_math_score


# In[10]:


# Calculate the average (mean) reading score
avg_reading_score = student_df["reading_score"].mean()
avg_reading_score


# In[11]:


#calculate the percentage of students who passed math (math scores greather than or equal to 70)
passing_math_count = combined_data[(combined_data["math_score"] >= 70)].count()["student_name"]
passing_math_percentage = passing_math_count / float(total_students) * 100
passing_math_percentage


# In[12]:


# Calculate the percentage of students who passeed reading (reading scores greather than or equal to 70) 
passing_reading_count = combined_data[(combined_data["reading_score"] >= 70)].count()["student_name"]
passing_reading_percentage = passing_reading_count / float(total_students) * 100
passing_reading_percentage


# In[13]:


# calculate the percentage of students that passed math and reading
passing_math_reading_count = combined_data[
    (combined_data["math_score"] >= 70) & (combined_data["reading_score"] >= 70)
    ].count()["student_name"]
overall_passing_rate = passing_math_reading_count /  float(total_students) * 100
overall_passing_rate


# In[14]:


# Create a snapshot of the district's key metrics in a DataFrame
district_summary = pd.DataFrame(
        {
            "Total Schools":[total_schools],
            "Total Students": [total_students],
            "Total Budget": [total_budget],
            "Average Math Score": [avg_math_score],
            "Average Reading Score": [avg_reading_score],
            "% Passing Math" : [passing_math_percentage],
            "% Passing Reading" : [passing_reading_percentage],
            "% Overall Passing": [overall_passing_rate]}
) 

# Formatting
district_summary["Total Students"] = district_summary["Total Students"].map("{:,}".format)
district_summary["Total Budget"] = district_summary["Total Budget"].map("${:,.2f}".format)

# Display the DataFrame
district_summary


# # School Summary

# In[15]:


# select the school type
school_types = school_df.set_index(["school_name"])["type"]
school_types


# In[16]:


# Calculate the total student count
per_school_counts = combined_data["school_name"].value_counts()
per_school_counts


# In[17]:


# Calculate the total school budget and per capita spending
per_school_budget = combined_data.groupby(["school_name"]).mean()["budget"]
per_school_capita = per_school_budget / per_school_counts
per_school_capita


# In[18]:


# Calculate the average test scores
per_school_math = combined_data.groupby(["school_name"]).mean()["math_score"]

per_school_reading = combined_data.groupby(["school_name"]).mean()["reading_score"]
per_school_math
#per_school_reading


# In[19]:


# Calculate the number of schools with math scores of 70 or higher
school_passing_math = combined_data[combined_data["math_score"] >= 70]
school_passing_math


# In[20]:


# Calculate the number of schools with reading scores of 70 or higher
school_passing_reading = combined_data[combined_data["reading_score"] >= 70]
school_passing_reading


# In[21]:


#  calculate the schools that passed both math and reading with scores of 70 or higher
passing_math_and_reading = combined_data[
    (combined_data["reading_score"] >= 70) & (combined_data["math_score"] >= 70)
]
passing_math_and_reading


# In[23]:


# calculate the passing rates
per_school_passing_math = school_passing_math.groupby(["school_name"]).count()["student_name"] / per_school_counts * 100
per_school_passing_reading = school_passing_reading.groupby(["school_name"]).count()["student_name"] / per_school_counts * 100
overall_passing_rate = passing_math_and_reading.groupby(["school_name"]).count()["student_name"] / per_school_counts * 100
per_school_passing_math


# In[24]:


# Creating a DataFrame called `per_school_summary` with columns for the calculations above.

per_school_summary = pd.DataFrame(
{
    "School Type": school_types,
    "Total Students":per_school_counts,
    "Total School Budget": per_school_budget,
    "Per Student Budget": per_school_capita,
    "Average Math Score": per_school_math,
    "Average Reading Score": per_school_reading,
    "% passing Math": per_school_passing_math,
    "% passing Reading" :per_school_passing_reading,
    "% Overall Passing": overall_passing_rate
    
})
# Formatting
per_school_summary["Total School Budget"] = per_school_summary["Total School Budget"].map("${:,.2f}".format)
per_school_summary["Per Student Budget"] = per_school_summary["Per Student Budget"].map("${:,.2f}".format)

# Display the DataFrame
per_school_summary


# # Highest-Performing Schools (by % Overall Passing)

# In[25]:


# Sort the schools by `% Overall Passing` in descending order and display the top 5 rows.
top_schools = per_school_summary.sort_values("% Overall Passing", ascending = False)
top_schools.head()


# # Bottom Performing Schools (By % Overall Passing)

# In[26]:


# Sort the schools by `% Overall Passing` in ascending order and display the top 5 rows.
bottom_schools = per_school_summary.sort_values("% Overall Passing", ascending = True)
bottom_schools.head()


# #  Math Scores by Grade

# In[27]:


#  separate the data by grade
ninth_graders = combined_data[(combined_data["grade"] == "9th")]
tenth_graders = combined_data[(combined_data["grade"] == "10th")]
eleventh_graders = combined_data[(combined_data["grade"] == "11th")]
twelfth_graders = combined_data[(combined_data["grade"] == "12th")]

# Group by "school_name" and take the mean of each.
ninth_graders_scores = ninth_graders.groupby(["school_name"]).mean()
tenth_graders_scores = tenth_graders.groupby(["school_name"]).mean()
eleventh_graders_scores = eleventh_graders.groupby(["school_name"]).mean()
twelfth_graders_scores = twelfth_graders.groupby(["school_name"]).mean()

# select only the `math_score`.
ninth_grade_math_scores = ninth_graders_scores["math_score"]
tenth_grader_math_scores = tenth_graders_scores["math_score"]
eleventh_grader_math_scores = eleventh_graders_scores.mean()["math_score"]
twelfth_grader_math_scores = twelfth_graders_scores["math_score"]

# Combine each of the scores above into single DataFrame called `math_scores_by_grade`
math_scores_by_grade = pd.DataFrame(
    {
        "9th":ninth_grade_math_scores,
        "10th": tenth_grader_math_scores,
        "11th": eleventh_grader_math_scores,
        "12th":twelfth_grader_math_scores        
    }
)

# Minor data wrangling
math_scores_by_grade.index.name = None

# Display the DataFrame
math_scores_by_grade


# # Reading Score by Grade  

# In[28]:


# separate the data by grade
ninth_graders = combined_data[(combined_data["grade"] == "9th")]
tenth_graders = combined_data[(combined_data["grade"] == "10th")]
eleventh_graders = combined_data[(combined_data["grade"] == "11th")]
twelfth_graders = combined_data[(combined_data["grade"] == "12th")]

# Group by "school_name" and take the mean of each.
ninth_graders_scores = ninth_graders.groupby(["school_name"]).mean()
tenth_graders_scores = tenth_graders.groupby(["school_name"]).mean()
eleventh_graders_scores = eleventh_graders.groupby(["school_name"]).mean()
twelfth_graders_scores = twelfth_graders.groupby(["school_name"]).mean()

#  select only the `reading_score`.
ninth_grade_reading_scores = ninth_graders_scores["reading_score"]
tenth_grader_reading_scores = tenth_graders_scores["reading_score"]
eleventh_grader_reading_scores = eleventh_graders_scores.mean()["reading_score"]
twelfth_grader_reading_scores = twelfth_graders_scores["reading_score"]

# Combine each of the scores above into single DataFrame called `reading_scores_by_grade`

reading_scores_by_grade = pd.DataFrame(
{
        "9th":ninth_grade_reading_scores,
        "10th": tenth_grader_reading_scores,
        "11th": eleventh_grader_reading_scores,
        "12th":twelfth_grader_reading_scores 
}


)
# Minor data wrangling
reading_scores_by_grade = reading_scores_by_grade[["9th", "10th", "11th", "12th"]]
reading_scores_by_grade.index.name = None

# Display the DataFrame
reading_scores_by_grade


# # Scores by School Spending

# In[29]:


# Establish the bins 
spending_bins = [0, 585, 630, 645, 680]
labels = ["<$585", "$585-630", "$630-645", "$645-680"]


# In[30]:


# Create a copy of the school summary since it has the "Per Student Budget" 
school_spending_df = per_school_summary.copy()
#school_spending_df


# In[31]:


# Using `pd.cut` to categorize spending based on the bins.
school_spending_df["Spending Ranges (Per Student)"] = pd.cut(per_school_capita, bins = spending_bins, labels = labels)
school_spending_df


# In[32]:


#  Calculate averages for the desired columns. 
spending_math_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["Average Math Score"]
spending_reading_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["Average Reading Score"]
spending_passing_math = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["% passing Math"]
spending_passing_reading = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["% passing Reading"]
overall_passing_spending = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["% Overall Passing"]


# In[33]:


# Assemble into DataFrame
spending_summary = pd.DataFrame(
{
    "Average Math Score" : spending_math_scores,
    "Average Reading Score": spending_reading_scores,
    "% passing Math": spending_passing_math,
    "% passing Reading": spending_passing_reading,
    "% Overall Passing": overall_passing_spending
}
)

# Display results
spending_summary


# # Scores by School Size

# In[34]:


# Establish the bins.
size_bins = [0, 1000, 2000, 5000]
labels = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]


# In[35]:


# Categorize the spending based on the bins
# Using `pd.cut` on the "Total Students" column of the `per_school_summary` DataFrame.

per_school_summary["School Size"] = pd.cut(per_school_summary["Total Students"], bins = size_bins, labels = labels)
per_school_summary


# In[36]:


# Calculate averages for the desired columns. 
size_math_scores = per_school_summary.groupby(["School Size"]).mean()["Average Math Score"]
size_reading_scores = per_school_summary.groupby(["School Size"]).mean()["Average Reading Score"]
size_passing_math = per_school_summary.groupby(["School Size"]).mean()["% passing Math"]
size_passing_reading = per_school_summary.groupby(["School Size"]).mean()["% passing Reading"]
size_overall_passing = per_school_summary.groupby(["School Size"]).mean()["% Overall Passing"]


# In[37]:


# Creating a DataFrame called `size_summary` that breaks down school performance based on school size (small, medium, or large).
# Using the scores above to create a new DataFrame called `size_summary`
size_summary = pd.DataFrame(
{
    "Average Math Score":size_math_scores,
    "Average Reading Score": size_reading_scores,
    "% passing Math": size_passing_math,
    "% passing Reading": size_passing_reading,
    "% Overall Passing":size_overall_passing 
}

)

# Display results
size_summary


# # Scores by School Type

# In[38]:


# Group the per_school_summary DataFrame by "School Type" and average the results.
type_math_scores = per_school_summary.groupby(["School Type"]).mean() 
type_reading_scores =  per_school_summary.groupby(["School Type"]).mean()
type_passing_math =  per_school_summary.groupby(["School Type"]).mean()
type_passing_reading =  per_school_summary.groupby(["School Type"]).mean()
type_overall_passing =  per_school_summary.groupby(["School Type"]).mean() 

#  select new column data
average_math_score_by_type = type_math_scores["Average Math Score"]
average_reading_score_by_type = type_reading_scores["Average Reading Score"]
average_percent_passing_math_by_type = type_passing_math["% passing Math"]
average_percent_passing_reading_by_type = type_passing_reading["% passing Reading"]
average_percent_overall_passing_by_type = type_overall_passing["% Overall Passing"]


# In[39]:


# Assemble the new data by type into a DataFrame called `type_summary`

type_summary = pd.DataFrame(
{
    "Average Math Score":average_math_score_by_type,
    "Average Reading Score": average_reading_score_by_type,
    "% passing Math":average_percent_passing_math_by_type,
    "% passing Reading": average_percent_passing_reading_by_type,
    "% Overall Passing":average_percent_overall_passing_by_type 
}

)

# Display results
type_summary


# In[ ]:





# In[ ]:




