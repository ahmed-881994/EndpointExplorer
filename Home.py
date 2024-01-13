import streamlit as st
from streamlit_monaco import st_monaco
import pprint
import pandas as pd
import requests
import re

# page config
st.set_page_config(page_title='Endpoint Explorer', page_icon='👩‍🚀', layout='wide', initial_sidebar_state='collapsed')

# title
st.title('Endpoint Explorer 👩‍🚀')

def prepare_headers(payload_type, headers_dict):
    """Prepares the request headers dict

    Args:
        payload_type (str): the payload type ['xml', 'json']
        headers_dict (dict): the list of key and values generated from the data editor 'hdrs_input' in the format of {'key':[''],'value':['']}

    Returns:
        dict: Request headers
    """
    headers = {}
    if payload_type and payload_type == 'json':
        content_type = 'application/' + payload_type
        headers = {'Content-Type': content_type}
    for i in range(len(headers_dict['key'])):
        if headers_dict['key'][i]=='':
            continue
        else:
            headers.update({headers_dict['key'][i]:headers_dict['key'][i]})
    return headers

# declare columns & init optional variables
rq_col, rs_col = st.columns(2)
payload_type = None
payload = None
# input column
with rq_col:
    cols = st.columns((0.35, 2))

    method = cols[0].selectbox('Method', ['GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE'], placeholder='Method', label_visibility='collapsed')
    url = cols[1].text_input('URL', placeholder='URL',label_visibility='collapsed')
     # show payload type & content if method is not GET, DELETE or HEAD
    if method not in ['GET', 'HEAD', 'DELETE']:
        payload_type = cols[0].selectbox('Payload type', ['json', 'xml'], placeholder='Method', label_visibility='collapsed')
        with cols[1]:
            payload = st_monaco(value='', height="300px", language=payload_type, lineNumbers=True, minimap=True, theme='streamlit')
   

    if 'data' not in st.session_state:
        data = {'key':[''],'value':['']}
        st.session_state.data = data

    # Show current data
    st.write('Headers')
    hdrs_input=st.data_editor(data=st.session_state.data, use_container_width=True, hide_index=True, num_rows='dynamic', column_config={
        "key": st.column_config.TextColumn(
            "Key",
            help="Header key",
            width="medium",
            required=True,
            validate="\\S"
        ),
        "value": st.column_config.TextColumn(
            "Value",
            help="Header value",
            width="medium",
            required=True,
            validate="\\S"
        )
    }, key='hdrs_input')

    


# send request
if cols[1].button('Send', type='primary'):
    with st.spinner(text='Sending...'):
        # prepare headers
        headers = prepare_headers(payload_type, hdrs_input)
        try:
            # send request
            response = requests.request(method=method, url=url, headers=headers, data=payload)
            # display response, status code and response headers
            with rs_col:
                with st.status(label=str(response.status_code)+' '+response.reason, expanded=True):
                    st.write('Response headers')
                    st.code(body=pprint.pformat(response.headers, sort_dicts=False), language='json', line_numbers=True)
                    # check the Content-Type of response to decide how to display it
                    if response.headers['Content-Type'] == 'application/json':
                        response_content = str(response.content).lstrip('b\'').rstrip('\'')
                        st.code(body=pprint.pformat(response_content, sort_dicts=False), language='json', line_numbers=True)
                    elif response.headers['Content-Type'] == 'application/xml':
                        response_content = str(response.content).lstrip('b\'').rstrip('\'')
                        st.code(body=response_content,language='xml-doc', line_numbers=True)
                    else:
                        st.warning('Response type not supported')
        except Exception as e:
            st.error(e)
        