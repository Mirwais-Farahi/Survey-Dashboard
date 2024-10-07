import pandas as pd
from koboextractor import KoboExtractor
import streamlit as st

KOBO_TOKEN = "0e7a75b50290d146396d6a3efef6d6de287683c6"
kobo = KoboExtractor(KOBO_TOKEN, 'https://eu.kobotoolbox.org/api/v2')

@st.cache_data(ttl=600)  # Cache for 60 minutes
def load_dataset(option, submitted_after):
    if option == "LTA - Baseline":
        asset_uid = "aDf3pqeP6u9vuaoxjiaEAQ"  # Baseline Form ID
        new_data = kobo.get_data(asset_uid, submitted_after=submitted_after)  # Fetch data from KoBoToolbox
        df = pd.DataFrame(new_data['results'])
        return df
    elif option == "LTA - PDM":
        asset_uid = "aMSpJ7vpGUdDYfBakatSff"  # PDM Form ID
        new_data = kobo.get_data(asset_uid, submitted_after=submitted_after)  # Fetch data from KoBoToolbox
        df = pd.DataFrame(new_data['results'])
        return df
    elif option == "LTA - PHM":
        asset_uid = "aHDFcWo745yEdv6bJvdJQt"  # Replace with the actual PHM Form ID
        new_data = kobo.get_data(asset_uid, submitted_after=submitted_after)  # Fetch data from KoBoToolbox
        df = pd.DataFrame(new_data['results'])
        return df
    return None
