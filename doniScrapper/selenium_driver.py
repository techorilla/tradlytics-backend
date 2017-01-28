from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver

class SeleniumDriver(object):
    def get_user_agent_for_headless_browser(self):
        return (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
        )

    def get_selenium_driver(self,url):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = self.get_user_agent_for_headless_browser()
        driver = webdriver.PhantomJS()
        driver.set_window_size(1024, 768)
        driver.get(url)
        return driver