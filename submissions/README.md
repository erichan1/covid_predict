# submissions

## Format
See sample_submission.csv for the format of a correct submission. 

Submissions must include predictions for all required dates, for every required county.
Required dates: All days from 2020-04-01 to 2020-06-30, inclusive.
Required county codes: all codes in ‘fips’ column in nyt_us_counties_daily.csv

## Explanation of an example row in submission

Header (column names):
id,10,20,30,40,50,60,70,80,90
Example row: 
2020-04-01-10001,1,3,4,5.5,6,9,10,14,20

You can see that id is in form:
id = (year)-(mo)-(day)-(county fips code)

Quantiles are more complicated. 
Your job is to output the number of new deaths per day for each us county. We also want to capture the confidence of your prediction for each day and county. Thus, you will produce the 10-90th quantiles for your prediction. 

You will approximate a probability distribution for your model’s belief of number of deaths. In our example row, the approximation looks like this:
10% chance number of deaths is 1 or below. 
20% chance number of deaths is 3 or below.
40% chance number of deaths is 5.5 or below.
90% chance number of deaths is 20 or below. 
The distribution here is clearly not normal, since it is not symmetric. It is up to you to decide how to model these ‘enhanced error bars’. 
