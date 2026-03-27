import streamlit.components.v1 as components
import os

_component_func = components.declare_component(
    "realtime_stt",
    path=os.path.dirname(os.path.abspath(__file__))
)

def realtime_stt(lang='en-US', key=None):
    return _component_func(lang=lang, key=key)
