# ====================================================================================================================================
# SUPERSTORE SALES ANALYSIS PROJECT
# Author: Suchithra Masuri
#
# Objective:
# Analyze retail sales data to identify business insights
# sales trends, and profit Opportunities.
#
# Tools Used:
# - Python
# - Pandas
# - NumPy
# - Matplotlib
# - Seaborn
# ====================================================================================================================================



# =====================================================================================================================================
# IMPORT LIBRARIES
# =====================================================================================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ====================================================================================================================================
# LOAD DATASET
#Read Superstore Sales dataset
# ====================================================================================================================================

df = pd.read_csv(r'Data/Sample - Superstore.csv', encoding='latin1')

print("Data Loaded Successfully!")

# =======================================================================================================================================
#INITIAL DATA EXPLORATION
# =======================================================================================================================================

print("shape:", df.shape)
print("columns:", df.columns.tolist())
print(df.head())
print(df.info())
print(df.describe())

# Check for missing values in each column
print("\n--- Missing Values ---")
print(df.isnull().sum())


# =======================================================================================================================================================
# DATA CLEANING AND FEATURE ENGINEERING
# =======================================================================================================================================================

print("\n--- Fixing Data Columns ---")
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])
print("Date columns fixed!")
print(df[['Order Date','Ship Date']].dtypes)


df['Order Year'] = df['Order Date'].dt.year
df['Order Month'] = df['Order Date'].dt.month
df['Order Month Name'] = df['Order Date'].dt.strftime('%B')
print("\nYear and Month columns created!")


df['Profit Margin'] = (df['Profit'] / df['Sales']) * 100
print("\nProfit Margin column created!")

df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days
print("Shipping Days column Created!")

df['Discount Range'] = pd.cut(df['Discount'],bins=[0,0.2,0.4,0.6,0.8],labels = ['Low','Medium','High','Very High'])
print("Discount Range column created!")

print('\n--- New Columns Added ---')
print(df[['Order Date', 'Order Year', 'Order Month', 'Order Month Name','Profit Margin','Shipping Days','Discount Range']].head())

df.drop(columns = ['Row ID','Country'],inplace=True)
print("\nUseless columns dropped!")


print("\n--- Final Shape After Cleaning ---")
print("Shape:",df.shape)
print("\n All columns Now:")
print(df.columns.tolist())


# ============================================================================================================================================================================================
# SAVE CLEANED DATASET
# ============================================================================================================================================================================================

df.to_csv(r'Data/superstore_cleaned.csv', index=False)
print("\nCleaned data Saved!")


# ========================================================================================================================================
# EXPLORATORY DATA ANALYSIS
# ========================================================================================================================================
 
print("\n--- Sales by region ---")
print(df.groupby("Region")['Sales'].sum().sort_values(ascending=False))

print("\n--- Profit by Region ---")
print(df.groupby('Region')['Profit'].sum().sort_values(ascending=False))

print("\n--- Sales by Category ---")
print(df.groupby('Category')['Sales'].sum().sort_values(ascending=False))

print("\n--- Profit by Category ---")
print(df.groupby('Category')['Profit'].sum().sort_values(ascending=False))

print("\n--- Sales by Customer Segment ---")
print(df.groupby('Segment')['Sales'].sum().sort_values(ascending=False))

print('\n--- Top 10 States by Sales ---')
print(df.groupby('State')['Sales'].sum().sort_values(ascending=False).head(10))

print("\n--- Top 10 States by Profit ---")
print(df.groupby('State')['Profit'].sum().sort_values(ascending=False).head(10))

print("\n--- States Making Loss ---")
print(df.groupby('State')['Profit'].sum().sort_values(ascending=True).head(5))

# ===========================================================================================================================================================================================
# ADVANCED BUSINESS ANALYSIS
# ===========================================================================================================================================================================================

print("\n--- Sales by Sub-Category ---")
print(df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(10))

print("\n--- Profit by Sub-Category ---")
print(df.groupby('Sub-Category')['Profit'].sum().sort_values(ascending=False))

print("\n--- Orders by Ship Mode ---")
print(df['Ship Mode'].value_counts())

print("\n--- Orders by Segment ---")
print(df['Segment'].value_counts())

print("\n--- Sales and Profit by Category and Region ---")
pivot = df.pivot_table(values = ['Sales','Profit'],index = 'Category',columns = 'Region',aggfunc = 'sum')
print(pivot)


# =========================================================================================================================================================================
# KEY BUSINESS METRICS
# ========================================================================================================================================================================
print("\n--- key Business Metrics ---")
print("Average Sale Value: $"+str(round(df['Sales'].mean(),2)))
print("Average Profit: $"+str(round(df['Profit'].mean(),2)))
print("Average Profit Margin: "+str(round(df['Profit Margin'].mean(),2)) + "%")
print("Average Shipping Days: "+str(round(df['Shipping Days'].mean(), 2)))


print("\n--- Correlation Analysis ---")
print(df[['Sales','Profit','Discount','Quantity','Shipping Days','Profit Margin']].corr())

print("\n--- Unique Value Counts--- ")
print("Total Customers: ", df['Customer Name'].nunique())
print("Total Products:", df['Product Name'].nunique())
print("Total Cities:",df['City'].nunique())
print("Total States:", df['State'].nunique())

print("\n--- Average Profit by Discount Range ---")
print(df.groupby('Discount Range',observed = True)['Profit'].mean())



# ==========================================================================================================================================================================
# DATA VISUALIZATION
#
# Charts:
# 1. Sales by Region
# 2. Profit by Region
# 3. Sales by Category
# 4. Profit by category
# 5. Monthly Sales Trend
# 6. Sales by Customer Segment
# 7. Top Sub-Categories
# 8.Discount vs Profit
# =======================================================================================================================================================================

import os
visuals_path = os.path.join("Visuals")
if not os.path.exists(visuals_path):
    os.makedirs(visuals_path)

# Chart 1: Sales preformance by region
plt.figure(figsize=(8,5))
region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
plt.bar(region_sales.index,region_sales.values,color=['#2196F3','#4CAF50','#FF9800','#F44336'])
plt.title('Sales by Region',fontsize = 16)
plt.xlabel('Region',fontsize=12)
plt.ylabel('Total Sales ($)', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(visuals_path,"sales_by_region.png"))
plt.show()
print("Chart 1 - Sales by Region Saved!")


# Chart 2: Profit performance by region
plt.figure(figsize = (8,5))
region_profit = df. groupby('Region')['Profit'].sum().sort_values(ascending = False)
plt.bar(region_profit.index,region_profit.values, color = ['#4CAF50','#2196F3','#FF9800','#F44336'])
plt.title('Profit by Region',fontsize=12)
plt.xlabel('Region', fontsize = 12)
plt.ylabel('Total Profit ($)', fontsize = 12)
plt.tight_layout()
plt.savefig(os.path.join(visuals_path, "profit_by_region.png"))
plt.show()
print("Chart 2 - Profit by Region Saved!")


# Chart 3: Sales by Category
plt.figure(figsize=(8,5))
cat_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending = False)
plt.bar(cat_sales.index,cat_sales.values, color = ['#9C27B0','#2196F3','#FF9800'])
plt.title('Sales by Category',fontsize = 16)
plt.xlabel('Category',fontsize = 12)
plt.ylabel('Total Sales ($)', fontsize = 12)
plt.tight_layout()
plt.savefig(os.path.join(visuals_path, "sales_by_category.png"))
plt.show()
print("Chart 3 - Sales by Category Saved!")


# Chart 4: Profit by category
plt.figure(figsize=(8,5))
cat_profit = df.groupby('Category')['Profit'].sum().sort_values(ascending = False)
colors = ['#4CAF50' if x > 0 else '#F44336' for x in cat_profit.values]
plt.bar(cat_profit.index,cat_profit.values,color = colors)
plt.title('Profit by Category', fontsize = 16)
plt.xlabel('Category',fontsize = 12)
plt.ylabel('Total Profit ($)',fontsize = 12)
plt.tight_layout()
plt.savefig(os.path.join(visuals_path, "profit_by_category.png"))
plt.show()
print("Chart 4 - Profit by Category Saved!")


# Chart 5: Monthly sales trend
plt.figure(figsize=(12,5))
monthly_sales = df.groupby(['Order Year','Order Month'])['Sales'].sum()
plt.plot(range(len(monthly_sales)),monthly_sales.values,color = '#2196F3',linewidth = 2)
plt.title("Monthly Sales Trend",fontsize = 16)
plt.xlabel('Month', fontsize = 12)
plt.ylabel('Total Sales ($)', fontsize = 12)
plt.tight_layout()
plt.savefig(os.path.join(visuals_path, "monthly_sales_trend.png"))
plt.show()
print("Chart 5 - Monthly Sales Trend Saved")


# Chart 6: Customer segment contribution
plt.figure(figsize=(8,8))
segment_sales = df.groupby('Segment')['Sales'].sum()
plt.pie(segment_sales.values,labels = segment_sales.index,autopct='%1.1f%%',colors = ['#2196F3','#4CAF50','#FF9800'])
plt.title('Sales by Customer Segment', fontsize = 16)
plt.tight_layout()
plt.savefig(os.path.join(visuals_path, "sales_by_segment.png"))
plt.show()
print('Chart 6 - Sales by Segment saved!')


# Chart 7: Top sub-categories by sales
plt.figure(figsize=(10,6))
subcat_sales = df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending = True).tail(10)
plt.barh(subcat_sales.index,subcat_sales.values, color='#2196F3')
plt.title('Top 10 Sub-Categories by Sales', fontsize = 16)
plt.xlabel('Total Sales ($)',fontsize = 12)
plt.tight_layout()
plt.savefig(os.path.join(visuals_path, "top-subcategories.png"))
plt.show()
print('Chart 7 - Top Sub-Categories Saved!')


# Chart 8: Relationship between discount and profit
plt.figure(figsize=(8,5))
plt.scatter(df['Discount'],df['Profit'],alpha = 0.3,color = '#2196F3')
plt.title('Discount vs Profit', fontsize = 12)
plt.xlabel('Discount',fontsize = 12)
plt.ylabel('Profit ($)', fontsize = 12)
plt.axhline(y = 0,color = 'Red',linestyle = '--')
plt.tight_layout()
plt.savefig(os.path.join(visuals_path, "discount_vs_profit.png"))
plt.show()
print("Chart 8 - Discount vs Profit Saved")

print('\n All 8 Charts in Visuals Folder')

# ================================================================================================================================================================================
# PROJECT SUMMARY
#
# Key Insights:
# - West region generated highest sales and profit.
# - Tables sub-category generated significant losses.
# - Texas was unprofitable despite high sales.
# - Higher discounts reduced profitability.
# - California was the strongest market.
# - Consumer segment contributed the highest sales.
# ================================================================================================================================================================================