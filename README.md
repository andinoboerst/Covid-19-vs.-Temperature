# Covid-19 vs. Temperature

This visualization uses the data given in the .csv file obtained from: [https://github.com/GoogleCloudPlatform/covid-19-open-data](https://github.com/GoogleCloudPlatform/covid-19-open-data) and queried in BigQuery.

The data includes daily information on new covid cases and the average temperature in every country in europe.

The visual shows the temperature at the top and the new covid cases as percentage of the population at the bottom over the time span of 2020 and 2021.

The bottom visual, i.e. the new covid cases, includes a threshold value set to 0.0002% of the population, shown with the horizontal line. Depending on whether the number of new cases is above that threshold value, the temperature line at the top is colored in blue or red. This facilitates the analysis of correlation between the temperature and the number of new covid cases in any european country. The country can be selected by typing the name of the country into the provided text box.

 A picture of the visual is shown here:
![fig1](https://user-images.githubusercontent.com/73847250/185001803-7ec4780f-22c7-4333-a5f7-1c93eb12e7c5.png)

The data is is prepared by forward filling missing data points. Additionally the plotted lines are smoothed out with a gaussian filter to avoid rough edges in the plot. To obtain the line plot with differently colored sections the line was divided into LineCollections.
