# Bengaluru House Price Analysis and Prediction 

This project is a comprehensive data analysis and machine learning study aimed at predicting residential house prices in Bengaluru, India, using a publicly available dataset.

---

## Overview
The analysis involves extensive **Exploratory Data Analysis (EDA)**, data cleaning, feature engineering, and training various regression models to determine the best approach for price prediction.

---

## Methodology
The Jupyter Notebook (`Bengaluru_House_Analysis.ipynb`) walks through the following steps:

1. **Data Loading & Cleaning**  
   Loading the dataset and handling missing values in columns like `society`, `location`, `bath`, and `balcony`.

2. **Feature Engineering**  
   Extracting relevant features from existing columns (e.g., standardizing `size` and converting `total_sqft` into a numerical format).

3. **Outlier Removal**  
   Using statistical methods to remove extreme outliers based on price per square foot and bathroom counts to improve model performance.

4. **Model Training**  
   Training and evaluating several regression algorithms, including:  
   - Linear Regression  
   - Ridge/Lasso Regression  
   - Decision Tree Regressor  
   - Random Forest Regressor  
   - XGBoost Regressor

5. **Model Selection & Export**  
   The best-performing model is selected and saved for deployment.

---

## 💾 Data Source
The data used for this analysis is sourced from Kaggle:

- **Dataset:** Bengaluru House Price Dataset  
- **Link:** [Kaggle Dataset](https://www.kaggle.com/datasets/bhaweshsinha07/bengaluru-house-price-dataset)

---

## Key Output
- **`bangalore_price_model.pkl`**: A serialized machine learning model file (joblib format) containing the trained algorithm ready for use in a prediction service.

---

## Technologies & Libraries
**Primary Language:** Python  

**Core Libraries:**  
- `pandas`, `numpy` — Data manipulation  
- `matplotlib`, `seaborn` — Data visualization  
- `scikit-learn` — Machine learning models and utilities  
- `xgboost` — Advanced boosting model  
- `joblib` — Model serialization

---
