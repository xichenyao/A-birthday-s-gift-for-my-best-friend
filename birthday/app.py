import streamlit as st
from langchain.memory import ConversationBufferMemory
from chain import generate_response
from PIL import Image
import os
import base64


def start_page():
    

    
    # 自定义CSS样式
    custom_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap'); 
    body {
        font-family: 'Roboto', sans-serif;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # 使用st.markdown来创建一个居中的大号字体标题
    st.markdown(
        '<div style="text-align: center; font-size: 44px; margin-top: 50px;"><h1>鸡哥情感小屋~</h1></div>',
        unsafe_allow_html=True
    )

    # 创建五列布局
    col1, col2, col3, col4, col5 = st.columns([1, 1, 3, 1, 1])

    # 在中间列使用empty占位符来调整按钮的位置
    with col3:
        st.empty()  # 第一个占位符
        st.empty()  # 第二个占位符
        if st.button("开始使用"):
            st.session_state.page = "login"
            st.rerun()
         # 显示背景图片
    image_path = '1.jpg'  # 确保路径正确
    st.image(image_path, use_column_width=True)


def login_page():
    st.title('鸡哥情感小屋~')

    

  # 确保用户数据初始化
    if "users" not in st.session_state:
        st.session_state.users = {"default_user": "password123"}  # 示例用户数据
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.login_attempted = False  # 用于控制错误消息显示

    # 表单输入
    username = st.text_input("🐔 用户名", placeholder="请输入用户名", key="username")
    password = st.text_input("🐔 密码", type="password", placeholder="请输入密码", key="password")

    # 自定义按钮样式
    button_style = """
    <style>
    .long-button {
        width: 100%;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
        margin-top: 10px;
    }
    .long-button:hover {
        background-color: #0056b3;
    }
    </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)

    # 创建一个包含一列的布局，用于登录按钮
    col = st.columns([1])

    with col[0]:
        # 登录按钮
        if st.markdown('<button class="long-button">登录</button>', unsafe_allow_html=True):
            st.session_state.login_attempted = True  # 设置登录尝试标记
            if username and password:
                if username in st.session_state.users and st.session_state.users[username] == password:
                    st.session_state.logged_in = True  # 设置登录状态
                    st.session_state.current_user = username  # 记录当前登录的用户
                    st.success("登录成功！")
                    st.session_state.page = "main"  # 设置页面为主页面
                    st.rerun()  # 重新运行应用
                else:
                    st.error("用户名或密码错误！")
            elif username or password:
                st.error("用户名或密码不能为空！")
       

    # 第二行：注册和跳过按钮
    button_col = st.columns([1,1,1, 1,1])  # 两列宽度相等

    with button_col[1]:
        if st.button("注册"):
            st.session_state.page = "register"
            st.rerun()

    with button_col[3]:
        if st.button("跳过", key="skip_button"):
            st.session_state.page = "main"
            st.session_state.logged_in = True
            st.rerun()




    # 添加底部标语
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #D3D3D3;
            color: #000000;
            text-align: center;
            padding: 20px;
            font-family: 'Pacifico', cursive;
            font-size: 24px;
        }
        </style>
        <div class="footer">
            "难绷！！难绷！！难绷！！"
        </div>
        """,
        unsafe_allow_html=True
    )

def register_page():

    st.title('鸡哥情感小屋~')

    # 添加注册界面的小标题
    #st.subheader('🙌注册界面')
    # 表单输入
    new_username = st.text_input("🐔新用户名")
    new_password = st.text_input("🐔新密码", type="password")

    # 注册按钮
    if st.button("注册"):
        if new_username in st.session_state.users:
            st.error("用户名已存在！")
        elif new_username and new_password:
            st.session_state.users[new_username] = new_password
            st.success("注册成功，请登录！")
            st.session_state.page = "login"
            st.rerun()
        else:
            st.error("用户名和密码不能为空！")

    # 返回登录页面按钮
    if st.button("返回登录页面"):
        st.session_state.page = "login"
        st.rerun()
        # 添加底部标语
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #D3D3D3;
            color: #000000;
            text-align: center;
            padding: 20px;
            font-family: 'Pacifico', cursive;
            font-size: 24px;
        }
        </style>
        <div class="footer">
           "难绷！！难绷！！难绷！！"
        </div>
        """,
        unsafe_allow_html=True
    )
def main_page():
    st.title('鸡哥情感小屋~')

    # 初始化对话列表
    if "conversations" not in st.session_state:
        st.session_state.conversations = {"鸡哥1": {"messages": [], "memory": ConversationBufferMemory(memory_key='chat_history')}} 
        st.session_state.current_conversation = "鸡哥1"

    # 初始化 selected_model
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "智谱"

    # 选择或创建对话
    with st.sidebar:
        conversation_name = st.selectbox("不同时期的鸡哥", list(st.session_state.conversations.keys()) + ["全新的鸡哥"],index=len(list(st.session_state.conversations.keys()))-1)
        if conversation_name == "全新的鸡哥":
            new_conversation_name = st.text_input("请输入新的鸡哥")
            if st.button("改变鸡哥") and new_conversation_name:
                st.session_state.conversations[new_conversation_name] = {"messages": [], "memory": ConversationBufferMemory(memory_key='chat_history')}
                st.session_state.current_conversation = new_conversation_name
                st.rerun()
        else:
            st.session_state.current_conversation = conversation_name

        # 切换对话
        st.write(f"鸡哥1: {st.session_state.current_conversation}")

        # 删除对话
        delete_conversation_name = st.selectbox("删除", ["选择要删除的时间段（对话）"] + list(st.session_state.conversations.keys()))
        if delete_conversation_name != "选择要删除的时间段（对话）" and st.button("删除"):
            del st.session_state.conversations[delete_conversation_name]
            if st.session_state.current_conversation == delete_conversation_name:
                st.session_state.current_conversation = None
            st.rerun()

        # 初始化 selected_model
        if "selected_model" not in st.session_state:
            st.session_state.selected_model = "智谱"

        # 下拉菜单选择模型
        model = st.selectbox("选择你的鸡哥（默认模型为智谱）", ["智谱", "百川", "你自己的选择"], index=[ "智谱", "百川","你自己的选择"].index(st.session_state.selected_model))
        st.write(f"你选择了 {model}")
        st.session_state.selected_model = model

        # 子页面链接
        if st.button("设置API Key"):
            st.session_state.page = "settings"
            st.rerun()

        current_conversation = st.session_state.conversations.get(st.session_state.current_conversation, None)
        if current_conversation is None:
            st.write("请创建或选择一个对话")
            return   
    
        uploaded_file = st.file_uploader("上传文件", type=["txt"])
        if uploaded_file is not None:
            st.write("已上传文件: ", uploaded_file.name)
            # 处理上传的文件（例如：读取文件内容、传输文件等）

            # 解码文件内容为字符串
            try:
                file_content = uploaded_file.read().decode('utf-8')  # 假设文件内容是以UTF-8编码的
            except UnicodeDecodeError:
                st.error("文件解码失败，请上传一个有效的UTF-8编码文件。")
                return



            current_conversation["messages"].append({'role': 'user', 'content': file_content})

            # 将解码后的文件内容传递给 generate_response 函数
            response = generate_response(current_conversation["memory"], file_content)
                # 展示聊天记录

            response = response['text']
            current_conversation["messages"].append({'role': 'assistant', 'content': response})

        st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)  # 根据侧边栏高度调整值
        if st.button("返回登录界面"):
            st.session_state.page = "login"
            st.rerun()

         # 获取当前对话
    current_conversation = st.session_state.conversations.get(st.session_state.current_conversation, None)
    if current_conversation is None:
        st.write("请创建或选择一个对话")
        return           



    # 展示当前选择的模型
    st.markdown(f"**当前陪伴你的鸡哥: {st.session_state.selected_model}**")



    # 展示聊天记录
    for message in current_conversation["messages"]:
        if message["role"] == "user":
            with st.chat_message(message["role"], avatar='🐔'):
                st.markdown(message["content"])
        else:
            with st.chat_message(message["role"], avatar='🐔'):
                st.markdown(message["content"])

    # 用于用户输入
    if prompt := st.chat_input('请和鸡哥开始交流！'):
        with st.chat_message('user', avatar='🐔'):
            st.markdown(prompt)

        current_conversation["messages"].append({'role': 'user', 'content': prompt})

        answer = generate_response(current_conversation["memory"], prompt,st.session_state.selected_model)

        response = answer['text']

        with st.chat_message('assistant', avatar='🐔'):
            st.markdown(response)
        current_conversation["messages"].append({'role': 'assistant', 'content': response})

            # 添加竖着的条幅
    st.markdown(
        """
        <style>
        .banner {
            position: fixed;
            right: 0;
            top: 20%;
            width: 40px;  /* 设置条幅宽度 */
            height: auto; /* 自动高度 */
            padding: 10px;
            background-color: #f1f1f1;
            
            box-shadow: 0px 0px 5px rgba(0,0,0,0.1);
            text-align: center;
            font-size: 14px;
            color: #333;
            writing-mode: vertical-rl; /* 文字竖排，右到左 */
            text-align: center; /* 居中对齐文字 */
            letter-spacing: 5px; /* 调整字间距 */
        }
        </style>
        <div class="banner">
            鸡哥陪你一起成长！
        </div>
        """,
        unsafe_allow_html=True
    )

def settings_page():
    # 初始化API key session state
    if "model_api_keys" not in st.session_state:
        st.session_state.model_api_keys = {
            "百川": "sk-9ad53b9efa92b004e166f989ce618b35",
            #sk-cfdf885592540e8f76134c1cfd962dd0
            "智谱": "abb6de86a3f2be08362ca8f230bec2ce.5ID144JCkuPEWgHr",
            "你自己的选择": "your_custom_api_key_here"
        }
        st.session_state.model_urls = {
            "百川": "https://api.baichuan-ai.com/v1",
            "智谱": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
            "你自己的选择": ""
        }
        st.session_state.model_names = {
            "百川": "Baichuan3-Turbo",
            "智谱": "glm-4",
            "你自己的选择": ""
        }

    # 获取当前选择的模型
    model = st.session_state.get("selected_model", "百川")

    st.title(f'设置 {model} 的 API Key')

    # 确保 model 存在于 model_api_keys 中
    if "model_api_keys" not in st.session_state:
        st.session_state.model_api_keys = {
            "你自己的选择": ""
        }
        st.session_state.model_urls = {
            "你自己的选择": ""
        }
        st.session_state.model_names = {
            "你自己的选择": ""
        }
    
    # 输入API key
    api_key = st.text_input(f"{model} API Key", value=st.session_state.model_api_keys.get(model, ""), type='password')
    # 输入API URL
    api_url = st.text_input(f"{model} API URL", value=st.session_state.model_urls.get(model, ""))
    # 输入模型名称
    model_name = st.text_input(f"{model} 模型名称", value=st.session_state.model_names.get(model, ""))

    # 保存按钮
    if st.button("保存"):
        st.session_state.model_api_keys[model] = api_key
        st.session_state.model_urls[model] = api_url
        st.session_state.model_names[model] = model_name
        st.success(f"{model} 的设置已保存")
        # st.session_state.page = "main"
        # st.experimental_rerun()

    # 切换到百川模型
    if model == "百川" and st.button("切换到百川"):
        st.success("已经成功切换到百川")
        st.session_state.selected_model = "百川"
        # st.session_state.page = "main"
        # st.experimental_rerun()
    # 切换到智谱模型
    if model == "智谱" and st.button("切换到智谱"):
        st.success("已经成功切换到智谱")
        st.session_state.selected_model = "智谱"
        # st.session_state.page = "main"
        # st.experimental_rerun()

    # 切换到自定义模型
    if model == "你自己的选择" and st.button("切换到自定义"):
        st.success("已经成功切换到自定义")
        st.session_state.selected_model = "你自己的选择"
        # st.session_state.page = "main"
        # st.experimental_rerun()

    # 返回主页面
    if st.button("返回"):
        st.session_state.page = "main"
        st.rerun()

def main():
    if "page" not in st.session_state:
        st.session_state.page = "start"

    if st.session_state.page == "start":
        start_page()
    elif st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "register":
        register_page()
    elif st.session_state.page == "main":
        main_page()
    elif st.session_state.page == "settings":
        settings_page()


if __name__ == "__main__":
    main()
