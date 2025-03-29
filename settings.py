"""사용자 설정 페이지"""

from module.settings import CustomSettingPage

setting_page = CustomSettingPage()
setting_page.lift()
setting_page.focus_force()
setting_page.mainloop()
