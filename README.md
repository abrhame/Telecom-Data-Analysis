# Telecom User Analysis

## Overview

This repository contains scripts and analyses for understanding user behavior and engagement within a telecom dataset. The analysis is divided into two primary tasks:

1. **User Overview Analysis**
2. **User Engagement Analysis**

## Table of Contents

1. [User Overview Analysis](#user-overview-analysis)
2. [User Engagement Analysis](#user-engagement-analysis)
3. [Setup](#setup)
5. [License](#license)

## User Overview Analysis

### Description

The User Overview Analysis aims to understand user behavior across various applications and identify key metrics related to handset usage. 

### Tasks

1. **Identify Top Handsets and Manufacturers**
   - Determine the top 10 handsets used by customers.
   - Identify the top 3 handset manufacturers.
   - Determine the top 5 handsets for each of the top 3 manufacturers.
   - Provide recommendations to the marketing team.

2. **User Behavior Analysis**
   - Aggregate user data including session frequency, duration, and total data traffic per application.
   - Perform Exploratory Data Analysis (EDA) to identify missing values and outliers.
   - Describe relevant variables and perform variable transformations.
   - Conduct both non-graphical and graphical univariate analysis.
   - Perform bivariate analysis and correlation analysis.
   - Apply Principal Component Analysis (PCA) for dimensionality reduction and interpret the results.

### Files

- `task11.py`: Script for performing the User Overview Analysis.
- `task1.ipynb`: Jupyter notebook for detailed analysis and visualization.

## User Engagement Analysis

### Description

The User Engagement Analysis focuses on tracking and improving user engagement based on session metrics and application usage.

### Tasks

1. **Aggregate and Normalize Engagement Metrics**
   - Aggregate metrics such as session frequency, duration, and total traffic per customer.
   - Normalize the metrics and classify customers using K-means clustering.

2. **Cluster Analysis and Visualization**
   - Compute cluster statistics (min, max, average, total) for non-normalized metrics.
   - Aggregate and visualize user traffic per application.
   - Determine the top 10 most engaged users per application.
   - Use K-means clustering to identify engagement clusters and find the optimal number of clusters using the elbow method.

### Files

- `task2.ipynb`: Jupyter notebook for detailed analysis and visualization.

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/abrhame/Telecom-Data-Analysis.git
   ```

2. **Install Dependencies**

   Ensure you have Python 3.7+ and install the required packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

3. **Download Dataset**

   Place your dataset files in the `data/` directory. Ensure the filenames match those used in the scripts.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to open issues or submit pull requests if you have any suggestions or improvements.
```