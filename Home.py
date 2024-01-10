import streamlit as st
from streamlit_ace import st_ace
import requests
import re

# page config
st.set_page_config(page_title='Endpoint Explorer',
                   page_icon='👩‍🚀', layout='wide', initial_sidebar_state='collapsed')

# title
st.title('Endpoint Explorer 👩‍🚀')

import re

def validate_url(url):
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    match = pattern.match(url)
    return match is not None

# declare columns
rq_col, rs_col = st.columns(2)
payload_type = None
payload = None

# input column
with rq_col:
    cols = st.columns((0.35,2))
    
    with cols[0]:
        method = st.selectbox('Method',['GET','POST','DELETE'], placeholder='Method', label_visibility='collapsed')
        # show payload type if method is not GET
        if method != 'GET':
            payload_type = st.selectbox('Payload type',['json','xml'], placeholder='Method', label_visibility='collapsed')
            
    with cols[1]:
        url = cols[1].text_input('URL', placeholder='URL', label_visibility='collapsed')
            # show payload content if method is not GET
        if method != 'GET':
            payload= st_ace(language = payload_type, show_gutter=True, auto_update=True)


# send request
if st.button('Send', type='primary'):
    # validate URL
    if not validate_url(url):
        #show error for invalid url
        st.error('URL can not be empty')
    else:
        with st.spinner(text='Sending...'):
            if payload_type and payload_type == 'json':
                headers = {'Content-Type': 'application/json'}
            elif payload_type and payload_type == 'xml':
                headers = {'Content-Type': 'application/xml'}
            else:
                headers=None
            response = requests.request(method= method, url= url, headers=headers, data=payload)
            with rs_col:
                response_content=str(response.content).lstrip('b\'').rstrip('\'')
                
                st_ace(value= response_content, language=payload_type,  show_gutter=True, auto_update=True, readonly= True)
    
