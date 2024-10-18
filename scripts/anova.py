import statsmodels.api as sm
from statsmodels.formula.api import ols
import pandas as pd
import numpy as np
property_df = pd.read_csv("../data/curated/processed property_w_distance.csv")
property_df['log_min_train_dist'] = np.log1p(property_df['min_train_dist'])
# Rename the 'price (AUD per week)' column
property_df = property_df.rename(columns={'price (AUD per week)': 'price_per_week'})
# Rename the 'property type' column
property_df = property_df.rename(columns={'property type': 'property_type'})

# test effect of suburb on rental price
model_suburb = ols('price_per_week ~ C(suburb)', data=property_df).fit()

anova_suburb = sm.stats.anova_lm(model_suburb, typ=2)
print(anova_suburb)

# there is a statistically significant effect of suburb on rental price

# test effect of property type on rental price
model_type = ols('price_per_week ~ C(property_type)', data=property_df).fit()

anova_type = sm.stats.anova_lm(model_type, typ=2)
print(anova_type)

# there is a statistically significant effect of property type on rental price
