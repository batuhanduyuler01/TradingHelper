import os
import streamlit as st
from multipages import MultiPage
from PIL import Image
import numpy as np
from web_pages import coin_predictions, borsa_predictions, old_web_page


app = MultiPage()

display = Image.open('fly_trader_logo.png')
display  = np.array(display)

col1, col2 = st.columns(2)
col1.image(display, width = 300)
col2.title("FLY Trading App")

app.add_page("COIN İŞLEMLERİ", coin_predictions.app)
app.add_page("BORSA İŞLEMLERİ", borsa_predictions.app)
app.add_page("ESKI SÜRÜME DÖN", old_web_page.app)


app.run()
