import pandas as pd
from koboextractor import KoboExtractor
import streamlit as st
import io  # Import io for in-memory image storage

KOBO_TOKEN = "0e7a75b50290d146396d6a3efef6d6de287683c6"
kobo = KoboExtractor(KOBO_TOKEN, 'https://eu.kobotoolbox.org/api/v2')

@st.cache_data(ttl=600)
def load_dataset(option, submitted_after):
    asset_uids = {
        "LTA - Baseline 1": "asv4Gt5Ar98UxRy4Kisf7Q",  # Baseline Form ID 1
        "LTA - Baseline 2": "aJN9n5MPJHarfTh279eVGg",  # Baseline Form ID 2
        "LTA - Baseline 3": "aDf3pqeP6u9vuaoxjiaEAQ",  # Baseline Form ID 3
        "LTA - PDM": "aMSpJ7vpGUdDYfBakatSff",        # PDM Form ID
        "LTA - PHM": "aHDFcWo745yEdv6bJvdJQt"         # PHM Form ID
    }

    asset_uid = asset_uids.get(option)
    if asset_uid is None:
        return None

    # Load data from KoBoToolbox
    new_data = kobo.get_data(asset_uid, submitted_after=submitted_after)
    df = pd.DataFrame(new_data['results'])

    return df