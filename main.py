import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters # Create locators for ticks on the time axis
import scipy.stats as stats

register_matplotlib_converters()
pd.options.display.float_format = '{:,.2f}'.format
pd.set_option('display.width', 640)
pd.set_option('display.max.columns', 10)

df_yearly = pd.read_csv('annual_deaths_by_clinic.csv')
# parse_dates avoids DateTime conversion later
df_monthly = pd.read_csv('monthly_deaths.csv', parse_dates=['date'])

# print(df_yearly.info())
# print(df_monthly.info())

# Check NAN Values
# print(df_monthly.isna().values.sum())
# print(df_yearly.isna().values.any())

# Check Duplicate
# print(df_yearly.duplicated().values.any())
# print(df_monthly.duplicated().values.any())

# print(df_yearly.describe())
# print(df_monthly.describe())

"""Percentage of Women Dying in Childbirth In The 1840s in Vienna"""
prob = df_yearly.deaths.sum() / df_yearly.births.sum() * 100
# print(f'Chances of dying in the 1840s in Vienna: {prob:.3}%')

# Create locators for ticks on the time axis
years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter('%Y')

# plt.figure(figsize=(6, 4), dpi=200)
# plt.yticks(fontsize=7)
# plt.xticks(fontsize=7, rotation=45)
# plt.title('Total Number of Monthly Births and Deaths', fontsize=18)
#
# ax1 = plt.gca()
# ax2 = ax1.twinx()
#
# ax1.grid(linestyle='--', color='grey')
# ax1.set_ylabel('Births', color='skyblue', fontsize=8)
# ax2.set_ylabel('Deaths', color='crimson', fontsize=8)
# # Use Locators
# ax1.set_xlim([df_monthly.date.min(), df_monthly.date.max()])
# ax1.xaxis.set_major_locator(years)
# ax1.xaxis.set_major_formatter(years_fmt)
# ax1.xaxis.set_minor_locator(months)
#
# ax1.plot(df_monthly.date, df_monthly.births, color='skyblue', linewidth='2')
# ax2.plot(df_monthly.date, df_monthly.deaths, color='crimson', linewidth='2')
#
# plt.show()

"""The Yearly Data Split by Clinic"""
# Total Yearly Births by Clinic
# line = px.line(df_yearly,
#                x='year',
#                y='births',
#                color='clinic',
#                title='Total Yearly Births by Clinic'
#                )
# line.show()

# line = px.line(df_yearly,
#                x='year',
#                y='deaths',
#                color='clinic',
#                title='Total Yearly Deaths By Clinic')
# line.show()

"""Proportion of Deaths at Each Clinic"""
df_yearly['pct_death'] = df_yearly.deaths/df_yearly.births

# The average death rate for the entire time
clinic_1 = df_yearly[df_yearly.clinic == "clinic 1"]
avg_clinic_1 = clinic_1.deaths.sum() / clinic_1.births.sum() *100
# print(avg_clinic_1)

clinic_2 = df_yearly[df_yearly.clinic == "clinic 2"]
avg_clinic_2 = clinic_2.deaths.sum() / clinic_2.births.sum() *100
# print(avg_clinic_2)

# line = px.line(df_yearly,
#                x='year',
#                y="pct_death",
#                color='clinic',
#                title=' Yearly Deaths by Clinic')
#
# line.show()

"""The Effect of Handwashing"""
df_monthly['pct_deaths'] = df_monthly.deaths/df_monthly.births
# print(df_monthly)
before_handwashing = df_monthly[df_monthly.date < '1847']
after_handwashing = df_monthly[df_monthly.date >= '1847']
# print(before_handwashing)
# print(after_handwashing)

bh_avg = before_handwashing.deaths.sum() / before_handwashing.births.sum() *100
ah_avg = after_handwashing.deaths.sum() / after_handwashing.births.sum() *100
# print(bh_avg, ah_avg)
# 10.75566890281089 3.223028662812154

roll_df = before_handwashing.set_index('date')
roll_df = roll_df.rolling(window=6).mean()
# print(roll_df)

# plt.figure(figsize=(6, 4), dpi=200)
# plt.title("% of Monthly Death Over Time", fontsize=8)
# plt.yticks(fontsize=6)
# plt.xticks(fontsize=6, rotation=45)
#
# plt.ylabel("% of Death", color='crimson', fontsize=6)
#
# ax = plt.gca()
# ax.xaxis.set_major_locator(years)
# ax.xaxis.set_major_formatter(years_fmt)
# ax.xaxis.set_minor_locator(months)
# ax.set_xlim([df_monthly.date.min(), df_monthly.date.max()])
# plt.grid(color='grey', linestyle='--',  linewidth=.6)

# ma_line, = plt.plot(roll_df.index,
#                     roll_df.pct_deaths,
#                     color='crimson',
#                     linewidth=2,
#                     linestyle='--',
#                     label='6m Moving Average')
# bw_line, = plt.plot(before_handwashing.date,
#                     before_handwashing.pct_deaths,
#                     color='black',
#                     linewidth=.5,
#                     linestyle='--',
#                     label='Before Handwashing')
# aw_line, = plt.plot(after_handwashing.date,
#                     after_handwashing.pct_deaths,
#                     color='skyblue',
#                     linewidth=2,
#                     marker='o',
#                     label='After Handwashing')
#
# plt.legend(handles=[ma_line, bw_line, aw_line],
#            fontsize=6)
#
# plt.show()

avg_prob_before = before_handwashing.pct_deaths.mean() * 100
avg_prob_after = after_handwashing.pct_deaths.mean() * 100
mean_diff = avg_prob_before-avg_prob_after
times = avg_prob_before / avg_prob_after
# print(avg_prob_before, avg_prob_after)
# 10.691840432632764 3.1727637898556225
# print("diff:", mean_diff)
# print(f'improvement is {times:.2}x ')

df_monthly['washing_hands'] = np.where(df_monthly.date < '1847', 'No', 'Yes')

# box = px.box(df_monthly,
#              x='washing_hands',
#              y='pct_deaths',
#              color='washing_hands',
#              title='How Have the Stats Changed with Handwashing?')
#
# box.update_layout(xaxis_title='Washing Hands?',
#                   yaxis_title='Percentage of Monthly Deaths', )
#
# box.show()

# hist = px.histogram(df_monthly,
#                     x='pct_deaths',
#                     color='washing_hands',
#                     nbins=30,
#                     opacity=0.6,
#                     barmode='overlay',
#                     histnorm='percent',
#                     marginal='box', )
#
# hist.update_layout(xaxis_title='Proportion of Monthly Deaths',
#                    yaxis_title='Count', )
#
# hist.show()

"""Monthly Death Rate Before and After Handwashing"""
plt.figure(figsize=(6, 4), dpi=200)
sns.kdeplot(data=before_handwashing.pct_deaths, shade=True, clip=(0, 1))
sns.kdeplot(data=after_handwashing.pct_deaths, shade=True, clip=(0, 1))
plt.title('Monthly Death Rate Before and After Handwashing')

plt.xlim(0, 0.40)
plt.show()

t_stat, p_value = stats.ttest_ind(a=before_handwashing.pct_deaths,
                                  b=after_handwashing.pct_deaths)

# p_value we see that it is 0.0000010362 or which is far below even 1%. In other words,
# the difference in means is highly statistically significant
print(f'p-palue is {p_value:.10f}')
print(f't-statstic is {t_stat:.4}')