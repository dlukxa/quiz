from flask import Flask, render_template, request, jsonify
import random
import csv
import json

app = Flask(__name__)

# Sample question sets (same format as in your original code)
question_sets = [
    [["How many e are in the periodic table?"], ["A. 116", "B. 117", "C. 118", "D. 119"], "C"],
    [["What is the first step in the data science process?"],
     ["A. Data Analysis", "B. Data Cleaning", "C. Data Visualization", "D. Data Collection"], "D"],
    [["Which programming language is widely used in data science?"],
     ["A. Python", "B. Java", "C. C++", "D. Ruby"], "A"],
    [["Which statistical measure gives the middle value of a dataset?"],
     ["A. Mean", "B. Median", "C. Mode", "D. Standard Deviation"], "B"],
    [["Which data structure is used to store data in key-value pairs?"],
     ["A. List", "B. Array", "C. Dictionary", "D. Stack"], "C"],
    [["What is the process of converting categorical variables into numerical values?"],
     ["A. Data Scaling", "B. Feature Engineering", "C. Data Encoding", "D. Data Normalization"], "C"],
    [["Which graph is used to show the relationship between two continuous variables?"],
     ["A. Bar Chart", "B. Pie Chart", "C. Scatter Plot", "D. Histogram"], "C"],
    [["Which Python library is commonly used for data manipulation and analysis?"],
     ["A. Matplotlib", "B. Numpy", "C. Scikit-learn", "D. Pandas"], "D"],
    [["Which type of data visualization is best suited for displaying the distribution of a single continuous variable?"],
     ["A. Line Chart", "B. Box Plot", "C. Bar Chart", "D. Pie Chart"], "B"],
    [["Which statistical test is used to determine if there is a significant difference between two groups?"],
     ["A. T-test", "B. Chi-square test", "C. ANOVA", "D. Pearson correlation"], "A"],
    [["What is the measure of the spread of data points in a dataset?"],
     ["A. Mean", "B. Variance", "C. Median", "D. Standard Deviation"], "D"],
    [["Which machine learning approach is inspired by the functioning of the human brain?"],
     ["A. Deep Learning", "B. Reinforcement Learning", "C. Supervised Learning", "D. Unsupervised Learning"], "A"],
    [["What is the term used to describe the process of finding hidden patterns in large datasets?"],
     ["A. Data Mining", "B. Data Wrangling", "C. Data Visualization", "D. Data Cleansing"], "A"],
    [["Which data structure is used to implement First-In-First-Out (FIFO) order?"],
     ["A. Stack", "B. Queue", "C. Linked List", "D. Tree"], "B"],
    [["Which statistical measure represents the average value of a dataset?"],
     ["A. Mean", "B. Median", "C. Mode", "D. Range"], "A"],
    [["Which Python library is primarily used for numerical and scientific computing?"],
     ["A. Matplotlib", "B. Seaborn", "C. Pandas", "D. NumPy"], "D"],
    [["Which data visualization technique is used to represent the relationship between two variables?"],
     ["A. Bar Chart", "B. Scatter Plot", "C. Line Chart", "D. Pie Chart"], "B"],
    [["What is the process of combining multiple datasets into one called?"],
     ["A. Data Merging", "B. Data Blending", "C. Data Aggregation", "D. Data Concatenation"], "D"],
    [["Which type of sampling technique involves selecting a random subset from the entire population?"],
     ["A. Stratified Sampling", "B. Systematic Sampling", "C. Convenience Sampling", "D. Simple Random Sampling"], "D"],
    [["Which type of data science task involves making predictions based on historical data?"],
     ["A. Clustering", "B. Classification", "C. Anomaly Detection", "D. Regression"], "D"],
    [["What is the process of cleaning and preparing data before analysis called?"],
     ["A. Data Visualization", "B. Data Mining", "C. Data Preprocessing", "D. Data Analysis"], "C"],
    [["Which data structure is used to store data in an organized and hierarchical manner?"],
     ["A. List", "B. Array", "C. Tree", "D. Stack"], "C"],
    [["What is the statistical measure representing the most frequent value in a dataset?"],
     ["A. Mean", "B. Median", "C. Mode", "D. Standard Deviation"], "C"],
    [["Which type of machine learning algorithm predicts numerical values?"],
     ["A. Classification", "B. Clustering", "C. Regression", "D. Reinforcement Learning"], "C"],
    [["What is the technique used to group similar data points together based on their features?"],
     ["A. Classification", "B. Clustering", "C. Regression", "D. Association Rule Mining"], "B"],
    [["What does the term 'correlation' represent in data analysis?"],
     ["A. The relationship between two categorical variables",
      "B. The strength and direction of the linear relationship between two numerical variables",
      "C. The comparison of multiple datasets in a box plot",
      "D. The arrangement of data points in a scatter plot"], "B"],
    [["Which method is used to handle outliers in a dataset?"],
     ["A. Removing the entire row containing the outlier",
      "B. Replacing the outlier with the mean of the dataset",
      "C. Ignoring the outlier during analysis",
      "D. Replacing the outlier with the median of the dataset"], "C"],
    [["Which measure of variability is affected the most by extreme values (outliers)?"],
     ["A. Range", "B. Variance", "C. Standard Deviation", "D. Interquartile Range (IQR)"], "B"],
    [["What is the formula for calculating the arithmetic mean of a set of values?"],
     ["A. Sum of all values divided by the number of values",
      "B. Product of all values divided by the number of values",
      "C. Square root of the sum of all values",
      "D. Median of the values"], "A"],
    [["Which statistical test is used to determine if there is a significant difference between two or more groups?"],
     ["A. T-test", "B. ANOVA (Analysis of Variance)", "C. Chi-square test", "D. Pearson correlation"], "B"],
    [["What does the p-value represent in hypothesis testing?"],
     ["A. The probability of rejecting a true null hypothesis",
      "B. The probability of accepting a false null hypothesis",
      "C. The level of significance for the test",
      "D. The margin of error in the test"], "A"],
    [["What is the formula for calculating the variance of a dataset?"],
     ["A. Sum of all values divided by the number of values",
      "B. Square root of the sum of squared differences from the mean",
      "C. Square root of the sum of squared differences from zero",
      "D. Sum of squared differences from the mean divided by the number of values"], "D"],
    [["Which measure of central tendency is resistant to extreme values?"],
     ["A. Mean", "B. Median", "C. Mode", "D. Range"], "B"],
    [["What is the standard deviation of a dataset with values {5, 5, 5, 5, 5}?"],
     ["A. 0", "B. 1", "C. 2", "D. 5"], "A"],
    [["Which statistical test is used to compare the means of two independent groups?"],
     ["A. Chi-square test", "B. t-test", "C. ANOVA", "D. Mann-Whitney U test"], "B"],
    [["What is the formula for calculating the range of a dataset?"],
     ["A. Difference between the highest and lowest values",
      "B. Sum of all values divided by the number of values",
      "C. Median of the values",
      "D. Product of all values divided by the number of values"], "A"],
    [["Which measure of variability represents the spread of data around the median?"],
     ["A. Range", "B. Variance", "C. Standard Deviation", "D. Interquartile Range (IQR)"], "D"],
    [["What is the formula for calculating the median of a dataset with an odd number of values?"],
     ["A. Middle value",
      "B. Average of the two middle values",
      "C. Sum of all values divided by the number of values",
      "D. Difference between the highest and lowest values"], "A"],
    [["What is the primary purpose of conducting hypothesis testing in statistics?"],
     ["A. To confirm the null hypothesis",
      "B. To establish causation between two variables",
      "C. To make predictions about future events",
      "D. To test a claim about a population based on sample data"], "D"],
    [["What is the primary goal of inferential statistics?"],
     ["A. To describe and summarize data",
      "B. To make predictions based on data patterns",
      "C. To test hypotheses and draw conclusions about populations",
      "D. To visualize data using graphs and charts"], "C"],
    [["Which measure of central tendency is most appropriate to use when the data contains extreme outliers?"],
     ["A. Mean", "B. Median", "C. Mode", "D. Range"], "B"]
]

# Helper function to read scores from the CSV file
def read_scores():
    scores = []
    with open('scores.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            score_data = json.loads(row[0].replace("'", '"'))
            scores.append(score_data)

    # Sort scores in ascending order based on 'score'
    scores.sort(key=lambda x: x['score'])

    return scores


@app.route('/')
def index():
    selected_questions = random.sample(question_sets, 8)
    return render_template('index.html', question_sets=selected_questions)

@app.route('/get_new_questions', methods=['GET'])
def get_new_questions():
    # Generate and return a new set of randomly selected questions
    new_question_sets = random.sample(question_sets, 7)
    return jsonify(new_question_sets)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    selected_idx = int(request.form.get('selected_idx'))
    correct_answer = question_sets[int(request.form.get('current_question'))][2]
    is_correct = selected_idx == ord(correct_answer) - ord("A")
    return jsonify({"is_correct": is_correct})

@app.route('/post_score', methods=['POST'])
def post_score():
    data = request.json

    # Append the score to a CSV file
    with open('scores.csv', 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([data])

    return 'Score received', 200

@app.route('/get_scoreboard')
def get_scoreboard():
    scores = read_scores()

    # Remove entries with None score
    scores = [entry for entry in scores if entry['score'] is not None]

    # Sort in descending order based on 'score'
    scores.sort(key=lambda x: int(x['score']), reverse=True)

    # Get the top 5 scores
    top_scores = scores[:5]
    print(top_scores)

    return jsonify(top_scores)

if __name__ == '__main__':
    app.run(debug=True)
