import pandas as pd
import numpy as np
from collections import Counter

def athlete(athletes,gender,country_selected,game):
    if gender != "Both":
        athletes=athletes[athletes['gender']==gender]

    if country_selected != "All":
        athletes = athletes[athletes['country'] == country_selected]

    if game != "All":
        athletes = athletes[athletes['disciplines'] == game]

    return athletes




