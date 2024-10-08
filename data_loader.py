import pandas as pd
from koboextractor import KoboExtractor
import streamlit as st

KOBO_TOKEN = "0e7a75b50290d146396d6a3efef6d6de287683c6"
kobo = KoboExtractor(KOBO_TOKEN, 'https://eu.kobotoolbox.org/api/v2')

@st.cache_data(ttl=600)
def load_dataset(option, submitted_after):
    if option == "LTA - Baseline 1":
        asset_uid = "asv4Gt5Ar98UxRy4Kisf7Q"  # Baseline Form ID 1
        new_data = kobo.get_data(asset_uid, submitted_after=submitted_after)
        df = pd.DataFrame(new_data['results'])
        return df
    elif option == "LTA - Baseline 2":
        asset_uid = "aJN9n5MPJHarfTh279eVGg"  # Baseline Form ID 2
        new_data = kobo.get_data(asset_uid, submitted_after=submitted_after)
        df = pd.DataFrame(new_data['results'])
        return df
    elif option == "LTA - Baseline 3":
        asset_uid = "aDf3pqeP6u9vuaoxjiaEAQ"  # Baseline Form ID 3
        new_data = kobo.get_data(asset_uid, submitted_after=submitted_after)
        df = pd.DataFrame(new_data['results'])
        return df
    elif option == "LTA - PDM":
        asset_uid = "aMSpJ7vpGUdDYfBakatSff"
        new_data = kobo.get_data(asset_uid, submitted_after=submitted_after)
        df = pd.DataFrame(new_data['results'])
        return df
    elif option == "LTA - PHM":
        asset_uid = "aHDFcWo745yEdv6bJvdJQt"
        new_data = kobo.get_data(asset_uid, submitted_after=submitted_after)
        df = pd.DataFrame(new_data['results'])
        return df
    return None
