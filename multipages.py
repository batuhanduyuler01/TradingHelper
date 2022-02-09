##############################################################################
# Bu sınıf birden fazla işlevin                                              #
# farklı sayfalarda çalışmasını                                              #
# handle etmek için kullanılacaktır.                                         #
#                                                                            #
# kaynak:                                                                    #
# https://github.com/prakharrathi25/data-storyteller/blob/main/multipage.py  #
#                                                                            #
##############################################################################

import streamlit as st

class MultiPage:

    def __init__(self):
        # diğer işlevlerini içerisinde tutacak app (sayfa) sözlüğü
        self.pages = {"title": [], "func": []}

    def add_page(self, title, func) -> None: 
        """ Sayfaları eklemek için kullanılan method
        Args:
            title : sayfanın navigator'da yer alacak ismi 
            
            func: sayfayı streamlit app olarak çalıştıracak py fonksiyonu
        """

        self.pages["title"].append(title)
        self.pages["func"].append(func)

    def run(self):
        # Selectbox içerisinde yer alan fonksiyonlar ile sayfalara geçiş yapılacak. 
        page = st.sidebar.selectbox(
            'App Navigation', 
            self.pages["title"], 
        )

        # run the app function 
        appIndexNo = self.pages["title"].index(page)
        self.pages["func"][appIndexNo]()

