import streamlit as st
from streamlit_monaco import st_monaco
from utils import utils
import requests
import json
from streamlit_ace import st_ace
from bs4 import BeautifulSoup
from xml.dom import minidom
# page config
st.set_page_config(page_title='Endpoint Explorer', page_icon='👨‍🚀', layout='wide', initial_sidebar_state='collapsed')

# title
st.title('Endpoint Explorer 👨‍🚀')

# declare columns & init optional variables
rq_col, rs_col = st.columns(2)
payload_type = None
payload = None
# input column
with rq_col:
    cols = st.columns((0.5, 2))

    method = cols[0].selectbox('Method', ['OPTIONS', 'HEAD', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE'], placeholder='Method', label_visibility='collapsed')
    url = cols[1].text_input('URL', placeholder='URL',label_visibility='collapsed')
     # show payload type & content if method is not GET, DELETE or HEAD
    if method not in ['GET', 'HEAD', 'DELETE', 'OPTIONS']:
        payload_type = cols[0].selectbox('Payload type', ['json', 'xml'], placeholder='Method', label_visibility='collapsed')
        with cols[1]:
            #payload = st_monaco(value='', height="300px", language=payload_type, lineNumbers=True, minimap=True, theme='streamlit')
            payload = st_ace(language = payload_type, show_gutter=True, auto_update=True, height=300, theme='dracula')
   

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
        headers = utils.prepare_headers(payload_type, hdrs_input)
        try:
            # send request
            response = requests.request(method=method, url=url, headers=headers, data=payload)
            # display response, status code and response headers
            with rs_col:
                with st.status(label=str(response.status_code)+' '+response.reason, expanded=True):
                    st.write('Response headers')
                    formatted_hdrs=json.dumps(dict(response.headers), indent=2, sort_keys=True)
                    st.code(body=formatted_hdrs, language='json', line_numbers=True)
                    st.write('Response body')
                    # check the Content-Type of response to decide how to display it
                    if 'json' in response.headers['Content-Type']:
                        formatted_code = utils.format_json(response.json())
                        st.code(body=formatted_code, language='json', line_numbers=True)
                    elif 'xml' in response.headers['Content-Type']:
                        formatted_code = utils.format_xml(response.text)
                        st.code(body=formatted_code,language='xml', line_numbers=True)
                    elif 'html'in response.headers['Content-Type']:
                        formatted_code = utils.format_html(response.text)
                        st.code(body=formatted_code,language='html', line_numbers=True)
                    else:
                        st.warning('Response type not supported')
        except Exception as e:
            st.error(e)
        