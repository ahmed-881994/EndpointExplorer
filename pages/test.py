import requests
import streamlit as st

st.title('Test 👩‍🚀')

# declare columns
from code_editor import code_editor

response_dict = code_editor(None, lang='json')

from streamlit_ace import st_ace

# Spawn a new Ace editor
content = st_ace(language='xml',show_gutter=True,auto_update=True)
content