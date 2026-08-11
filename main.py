import pandas as pd

# بارگذاری دیتاست از گیتهاب
url = 'https://raw.githubusercontent.com/Ghorbanpoor/tasab_quera/main/Data/data.csv'
df = pd.read_csv(url)

# تبدیل تاریخ با فرمت دقیق M/D/YYYY
df['HIRE_YEAR'] = pd.to_datetime(df['HIREDATE_STRING'], format='%m/%d/%Y').dt.year

# ============ قسمت اول ============
# محاسبه میانگین حقوق هر دپارتمان برای مقایسه
dept_mean = df.groupby('DESCRSHORT')['COMPRATE'].transform('mean')

# فیلتر کردن کارمندانی که حقوقشان بالاتر از میانگین دپارتمان خودشان است
above_average_employees_df = df[df['COMPRATE'] > dept_mean][['OBJECTID', 'DESCRSHORT', 'COMPRATE']]

# مرتب‌سازی صعودی بر اساس OBJECTID
above_average_employees_df = above_average_employees_df.sort_values('OBJECTID').reset_index(drop=True)

# ============ قسمت دوم ============
# تعریف کارمند وفادار: استخدام قبل از سال 2000
df['LOYAL'] = df['HIRE_YEAR'] < 2000

# پیدا کردن دپارتمان‌هایی که حداقل 10 کارمند دارند
dept_counts = df.groupby('DESCRSHORT').size()
valid_depts = dept_counts[dept_counts >= 10].index

# فیلتر کردن فقط دپارتمان‌های معتبر
df_valid = df[df['DESCRSHORT'].isin(valid_depts)]

# محاسبه درصد کارمندان وفادار در هر دپارتمان
loyal_percentage_df = df_valid.groupby('DESCRSHORT')['LOYAL'].mean() * 100

# حذف دپارتمان‌هایی که کارمند وفادار ندارند (درصد صفر)
loyal_percentage_df = loyal_percentage_df[loyal_percentage_df > 0].reset_index()
loyal_percentage_df.columns = ['DESCRSHORT', 'Loyal_Employee_Percentage']

# رند کردن تا 2 رقم اعشار و مرتب‌سازی نزولی
loyal_percentage_df['Loyal_Employee_Percentage'] = loyal_percentage_df['Loyal_Employee_Percentage'].round(2)
loyal_percentage_df = loyal_percentage_df.sort_values('Loyal_Employee_Percentage', ascending=False).reset_index(drop=True)

# ============ قسمت سوم ============
# تقسیم‌بندی به 5 پنجک (Quintile) بر اساس سال استخدام
# نسل 1 جدیدترین‌ها، نسل 5 قدیمی‌ترین‌ها
df['Tenure_Quintile'] = pd.qcut(df['HIRE_YEAR'], 5, labels=[1, 2, 3, 4, 5])

# محاسبه میانگین حقوق برای هر پنجک
average_salary_by_quintile_df = df.groupby('Tenure_Quintile')['COMPRATE'].mean().round(2).reset_index()
average_salary_by_quintile_df.columns = ['Tenure_Quintile', 'Average_Salary']

# مرتب‌سازی نزولی بر اساس Tenure_Quintile (از 5 به 1)
average_salary_by_quintile_df = average_salary_by_quintile_df.sort_values('Tenure_Quintile', ascending=False).reset_index(drop=True)
