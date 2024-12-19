from PyInstaller.utils.hooks import copy_metadata

datas = (
    copy_metadata("streamlit") +
    copy_metadata("langchain") + # 添加 langchain 的元数据
    copy_metadata("langchain-openai")+
    copy_metadata("langchain-community")
) 
