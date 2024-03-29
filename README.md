# GPTs-EasyConfig
![Static Badge](https://img.shields.io/badge/license-MIT-blue)

![image](https://github.com/Ruijian-Zha/GPTs-EasyConfig/assets/55631456/c0b6c513-5d8b-456b-83b9-ee877fefb29f)

https://github.com/Ruijian-Zha/GPTs-EasyConfig/assets/55631456/5760e02e-87be-48ff-9000-f45b4100e083


`GPTs-EasyConfig` is a streamlined open-source tool designed to simplify and automate the setup and configuration of databases for GPT-based applications. Leveraging the user-friendly Streamlit interface, it provides a seamless experience for both beginners and experienced developers to manage and interact with their GPT instances effectively.

Currently, `GPTs-EasyConfig` supports the most basic version of GPTs generation (only in mac os). Other features, such as the tool server, are still under development.

## Prerequisites

Before you begin, ensure you have the following installed:
- `Conda`
- `Google Chrome`
- `Keyboard Maestro`

## Environment Setup

1. **Prepare Scripts:**
   Place all scripts from the `keyboard_maestro` folder into the Keyboard Maestro app on your local computer.

2. **Enable Chrome for Apple Events:**
   Make sure to enable Google Chrome to be triggered by Apple Events. (google chrome setting >> view >> developer >> allow javascript form apple events)

3. **Run Streamlit:**
   You can run the application using Streamlit with the following command:

```bash
streamlit run main.py
```
