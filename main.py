import os
import time

import pyperclip
import pyautogui
import time
from PIL import ImageGrab
import streamlit as st

# Create a Streamlit page for input
st.title('GptsEasyConfig')
user_input = st.text_area("Describe the agent you wish to create:")

# Submit button
if st.button('Submit'):
    # Get the input into clipboard
    pyperclip.copy(user_input)

    os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "gpts_step1_create"'""")
    # os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "950B64F0-1163-48C4-BFA0-D8585245054B"'""")
    # or: os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "gpts_creation[1]"'""")
    # or: os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "950B64F0-1163-48C4-BFA0-D8585245054B" with parameter "Whatever"'""")

    time.sleep(25)

    os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "gpts_step2_confirm"'""")
    # os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "656700D6-AFB7-44B4-BC1D-D23AB837EC36"'""")
    # or: os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "gpts_confirm[2]"'""")
    # or: os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "656700D6-AFB7-44B4-BC1D-D23AB837EC36" with parameter "Whatever"'""")

    time.sleep(25)

    os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "gpts_step3_publish"'""")
    # os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "83BC847D-9ADD-473F-8EEE-B1E72DECA6D7"'""")
    # or: os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "gpts_click[3]"'""")
    # or: os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "83BC847D-9ADD-473F-8EEE-B1E72DECA6D7" with parameter "Whatever"'""")

    time.sleep(15)

    # Take a screenshot
    screenshot = ImageGrab.grab()
    screenshot.save("screenshot.png")

    st.image("screenshot.png", caption="Screenshot of GPTs")

    os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "gpts_step4_switchTab"'""")
    # import os
    # os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "3F40FC8D-7071-4060-B910-92321975BDE2"'""")
    # or: os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "gpts_last_tab"'""")
    # or: os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "3F40FC8D-7071-4060-B910-92321975BDE2" with parameter "Whatever"'""")

    st.success("Your GPTs has been successfully created!")