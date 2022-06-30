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

**blah**''')


# In[ ]:


st.title('Test')
written = st.text_area('type stuff')


# In[ ]:


st.write(written)

