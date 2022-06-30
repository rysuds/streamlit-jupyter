#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st


# In[ ]:


st.markdown('''# Testing Jupyter Notebook -> Streamlit as markdown

## Markdown stuff

- blah
- blah

`blah`

jnedjnbejdnbje
hello


jjjj




jjsjs

kkkk
ksjksjks
sjjsjs

**blah**

huhuhuhuhu
yadadad

spiro


jdj

jsjs----jsj
jsj




''')


# In[ ]:


st.title('Test')
written = st.text_area('type stuff')
st.select_slider('', options=['1','2'])


# In[ ]:


st.write(written)
st.write(written)

