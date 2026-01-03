from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *

class MyWebBrowser(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MyWebBrowser, self).__init__(*args, **kwargs)
        self.tabs = QTabWidget()

        self.browser = QWebEngineView()

        self.tabs.setDocumentMode(True)

        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

        self.tabs.currentChanged.connect(self.current_tab_changed)

        self.tabs.setTabsClosable(True)

        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.setCentralWidget(self.tabs)

        self.status = QStatusBar()

        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation")

        self.addToolBar(navtb)

        self.back_button = QAction("<", self)

        self.forward_button = QAction(">", self)


        self.back_button.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(self.back_button)
        self.forward_button.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(self.forward_button)

        reload_button = QAction("Reload", self)
        reload_button.setStatusTip("Reload Page")
        reload_button.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_button)

        navtb.addSeparator()
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        self.add_new_tab(QUrl("http://www.duckduckgo.com"), "Homepage")

        self.show()
        self.setWindowTitle("Jake's Browser")
    
    def add_new_tab(self, qurl = None, label = "Blank"):
        if qurl is None:
            qurl = QUrl("http://www.duckduckgo.com")
        browser = QWebEngineView()
        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser = browser: self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i = i, browser = browser: self.tabs.setTabText(i, browser.page().title()))
    
    def tab_open_doubleclick(self, i):
       if i == -1:
           self.add_new_tab()
    
    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())
    
    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)
    
    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return
        
        title = self.tabs.currentWidget().page().title()

        self.setWindowTitle("% s - Jake's web browser" % title)
    
    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.duckduckgo.com"))
    
    def navigate_to_url(self):
        q = QUrl(f"https://duckduckgo.com/?origin=funnel_home_website&t=h_&q={self.urlbar.text()}&ia=web")

        if q.scheme() == "":
            q.setScheme("http")
        
        self.tabs.currentWidget().setUrl(q)
    
    def update_urlbar(self, q, browser = None):
        if browser != self.tabs.currentWidget():
            return
        
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

app = QApplication([])
app.setApplicationName("Jake's Web Browser")
window = MyWebBrowser()
app.exec_()