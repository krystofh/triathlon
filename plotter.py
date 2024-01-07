import os
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import norm, skewnorm
import numpy as np
from datetime import timedelta

# Analysis of results of 40. Leipziger Triathlon 2023
# 23.12.2023
# Legend: DNF - did not finish, DSQ - disqualified, DNS - did not start (not mentioned)

def parse_minutes(data: pd.Series):
    """Convert to timedelta and to minutes"""
    data = pd.to_timedelta(data)
    minutes = data.dt.total_seconds() / 60
    return  minutes.values

def placement_label(placement: int, participants:int):
    """Generate label of the placement with percentile"""
    return f"{placement}/{participants} ({(1-placement/participants)*100:.1f}th perc.)"

def format_time(t_minutes: np.float64):
    """Generate string from time in minutes (float) in the format HH:MM:SS"""
    td = timedelta(minutes=t_minutes)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_time = "{:02}:{:02}:{:02}".format(hours, minutes, seconds)
    return formatted_time

def fit_gauss(data, ax):
    # Based on https://www.geeksforgeeks.org/how-to-plot-normal-distribution-over-histogram-in-python/
    mean, std, vars = skewnorm.fit(data, loc=np.mean(data), scale=np.std(data)) # norm-symetric function, skewnorm - added skew and kurtosis
    xmin, xmax = ax.get_xlim()
    x = np.linspace(xmin, xmax, 100)
    y = skewnorm.pdf(x, mean, std, vars) # probability density function using the params and x axis
    ax.plot(x,y, 'g', linestyle='--', alpha=0.2) # plot gauss
    ax.vlines(mean, 0, skewnorm.pdf(mean, mean, std, vars), color='g', alpha=0.6) # plot mean as a line
    ax.set_ylim(0)

# Read data from CSV and preprocess
print("Reading results from Leipziger triathlon...")
results_df = pd.read_csv(os.path.join("data", "triathlon_results.csv"), index_col="Platz")
results_df.drop(index=["DNF", "DSQ"], inplace=True) # get rid of disqualified and not finished
swim = parse_minutes(results_df["Schwimmen"])
bike = parse_minutes(results_df["Rad"])
run = parse_minutes(results_df["Laufen"])
total = parse_minutes(results_df["Zeit"])
participants = len(results_df)
# Personal results
personal = results_df[results_df["Name"]=="Hes"]
personal_swim = parse_minutes(personal["Schwimmen"])
personal_bike = parse_minutes(personal["Rad"])
personal_run = parse_minutes(personal["Laufen"])
personal_total = parse_minutes(personal["Zeit"])
personal_placement = int(personal.index[0])
# Categories
swim_df=results_df.sort_values(by=['Schwimmen']) # sort results by swim time
swim_df.reset_index(inplace=True) # reset the indices, total placement ignored
swim_placement=swim_df[swim_df["Name"]=='Hes'].index[0] # get index from the sorted df
run_df=results_df.sort_values(by=['Laufen'])
run_df.reset_index(inplace=True)
run_placement=run_df[run_df["Name"]=='Hes'].index[0]
bike_df = results_df[results_df['Rad'] != '00:00:00'] # delete entries with no bike time
bike_df=bike_df.sort_values(by=['Rad']) # sort according to bike time
bike_df.reset_index(inplace=True)
bike_placement=bike_df[bike_df["Name"]=='Hes'].index[0]
bike_participants = len(bike_df) # number of participants finishing bike part
# Plot design
fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(2,3)
ax0 = fig.add_subplot(gs[0,0]) # design layoyt using gridspace
ax1 = fig.add_subplot(gs[0,1])
ax2 = fig.add_subplot(gs[0,2])
ax3 = fig.add_subplot(gs[1,:]) # span entire row with the plot
# Plot data
ax0.hist(swim, 60, edgecolor='gray') # add border of the bins
ax0.axvline(personal_swim, color='r')
ax0.set_title("Swimming 1590 m")
ax0.set_xlabel("Minutes")
ax0.set_xlim(15,60)
ax0.set_ylabel("Participants")
ax0.text(0.55, 0.68, f"{format_time(np.median(swim))} median", color='g',transform=ax0.transAxes)
ax0.text(0.55, 0.6, f"{personal['Schwimmen'].values[0]} personal", color='r', transform=ax0.transAxes) # transform axes to use placement in axes coord 0-1
ax0.text(0.55, 0.52, placement_label(swim_placement, participants), transform=ax0.transAxes)
ax0_norm=ax0.twinx()
fit_gauss(swim, ax0_norm)

ax1.hist(bike, 60, edgecolor='gray')
ax1.axvline(personal_bike, color='r')
ax1.set_title("Bike 42 km")
ax1.set_xlabel("Minutes")
ax1.set_xlim(50)
ax1.text(0.55, 0.68, f"{format_time(np.median(bike))} median", color='g',transform=ax1.transAxes)
ax1.text(0.55, 0.6, f"{personal['Rad'].values[0]} personal", color='r', transform=ax1.transAxes)
ax1.text(0.55, 0.52, placement_label(bike_placement, bike_participants), transform=ax1.transAxes)
ax1_norm=ax1.twinx()
fit_gauss(bike, ax1_norm)

ax2.hist(run, 60, edgecolor='gray')
ax2.axvline(personal_run, color='r')
ax2.set_title("Running 10 km")
ax2.set_xlabel("Minutes")
ax2.set_xlim(30)
ax2.set_ylabel("Participants")
ax2.text(0.55, 0.68, f"{format_time(np.median(run))} median", color='g',transform=ax2.transAxes)
ax2.text(0.55, 0.6, f"{personal['Laufen'].values[0]} personal", color='r', transform=ax2.transAxes)
ax2.text(0.55, 0.52, placement_label(run_placement, participants), transform=ax2.transAxes)
ax2_norm=ax2.twinx()
fit_gauss(run, ax2_norm)

ax3.hist(total, 150, edgecolor='gray')
ax3.axvline(personal_total, color='r')
ax3.set_title("Total")
ax3.set_xlabel("Minutes")
ax3.set_xlim(100)   
ax3.set_ylabel("Participants")
ax3.text(0.75, 0.68, f"{format_time(np.median(total))} mean", color='g',transform=ax3.transAxes)
ax3.text(0.75, 0.6, f"{personal['Zeit'].values[0]} personal", color='r', transform=ax3.transAxes)
ax3.text(0.75, 0.5, placement_label(personal_placement, participants), transform=ax3.transAxes) # placement
ax3_norm=ax3.twinx() # create a secondary y-axis for the PDF sharing the x
fit_gauss(total, ax3_norm) # fit gaussian distribution (PDF)to the data, see gaussian_fit.py
plt.suptitle("Results of 40. Leipziger triathlon 2023, men category")
plt.show()
print("Done")