### 项目简介

欢迎来到 **Easy_RWKV_Webui** 项目！本项目是一个基于 PyWebIO 和 RWKV 模型的在线聊天室，用户可以与 RWKV 模型进行互动和对话。

![Language](https://img.shields.io/badge/language-python-brightgreen) ![Documentation](https://img.shields.io/badge/documentation-yes-brightgreen)
### 项目结构

```
Easy_RWKV_Webui/
├── main.py
├── chat_room/
│   ├── __init__.py
│   └── chat_room.py
├── rwkv_model/
│   ├── __init__.py
│   └── rwkv_model.py
└── model（放置rwkv模型和词表）
```

### 功能介绍

- **实时聊天** 🗨️：用户可以在聊天室中实时发送和接收消息。
- **智能回复** 🤖：通过 RWKV 模型生成智能回复。
- **多语言支持** 🌐：支持英文和中文界面。

### 安装指南

1. 克隆仓库到本地：

   ```sh
   git clone https://github.com/No-22-Github/Easy_RWKV_webui.git
   cd Easy_RWKV_webui
   ```

2. 创建并激活虚拟环境：

   ```sh
   python -m venv venv
   source venv/bin/activate   # 对于 Windows 系统使用 `venv\Scripts\activate`
   ```

3. 安装依赖：

   ```sh
   pip install -r requirements.txt
   pip install torch==2.2.1+cu118 torchvision==0.17.1+cu118 -f https://mirror.sjtu.edu.cn/pytorch-wheels/torch_stable.html
   (torch如果是cpu版需要修改rwkv_model/rwkv_model.py)

   ```

### 配置RWKV模型

在 `rwkv_model/rwkv_model.py` 中配置你的 RWKV 模型路径和其他参数：

```python
args.MODEL_NAME = "model/RWKV-x060-World-1B6-v2.1-20240328-ctx4096"
```

请确保你已经下载并解压了对应的 RWKV 模型，并将其路径填写到上述代码中。
[RWKV-x060-World-1B6-v2-20240208-ctx4096.pth](https://huggingface.co/BlinkDL/rwkv-6-world/blob/main/RWKV-x060-World-1B6-v2.1-20240328-ctx4096.pth)

### 运行项目

在项目根目录下运行以下命令启动服务器：

```sh
python main.py
```

服务器启动后，你可以在浏览器中访问 `http://localhost:8080` 来使用 RWKV Chat Room。

### 问题反馈

如果在使用过程中遇到问题，请通过 GitHub Issues 提交，我们会尽快解决。

### 致谢

感谢 PyWebIO 和 RWKV 模型的开发者们，你们的工作让这个项目成为可能。🎉

---

> **注意**：此 README 中的路径和配置需要根据你的实际情况进行调整。

如果有任何疑问或建议，请随时联系！感谢你的支持！💖
