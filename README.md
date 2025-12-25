
## Dataset

**`city_power_cut_data.csv`**  
A CSV dataset with city power outage records. Typical columns might include:

- `Date` or `Timestamp` – Date and time of the outage
- `Duration` – Duration of the power cut (hours/minutes)
- `Location` – Area or sector affected
- `Cause` – Reason for the outage (if available)


## Python Script

**`power_cut.py`**  
This script performs the following tasks:

1. Reads the power cut dataset (`.csv` file)
2. Cleans and preprocesses the data
3. Performs exploratory data analysis
4. Generates visualizations to show trends, patterns, and insights

You can extend the script with additional analyses such as:
- Time series decomposition
- Seasonal trend analysis
- Predictive models for outage forecasting

## Requirements

Make sure you have **Python 3.7+** installed. Install dependencies using:

```bash
pip install pandas numpy matplotlib
