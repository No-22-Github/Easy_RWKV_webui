import asyncio
from pywebio.input import input, actions, textarea, input_group
from pywebio.output import put_markdown, put_scrollable, put_scope
from pywebio.session import info as session_info
from rwkv_model.rwkv_model import generate_response

MAX_MESSAGES_CNT = 10 ** 4

chat_msgs = []  # The chat message history. The item is (name, message content)
online_users = set()

def t(eng, chinese):
    """Return English or Chinese text according to the user's browser language"""
    return chinese if 'zh' in session_info.user_language else eng

async def refresh_msg(my_name):
    """Send new message to current session"""
    global chat_msgs
    last_idx = len(chat_msgs)
    while True:
        await asyncio.sleep(0.5)
        for m in chat_msgs[last_idx:]:
            if m[0] != my_name:  # only refresh message that not sent by current user
                put_markdown('`%s`: %s' % m, sanitize=True, scope='msg-box')

        # remove expired message
        if len(chat_msgs) > MAX_MESSAGES_CNT:
            chat_msgs = chat_msgs[len(chat_msgs) // 2:]

        last_idx = len(chat_msgs)

async def main():
    """PyWebIO chat room

    You can chat with everyone currently online.
    """
    global chat_msgs

    put_markdown(t("## RWKV chat room\nWelcome to the RWKV room, you can chat with RWKV", "## RWKV聊天室\n欢迎来到RWKV聊天室，你可以和RWKV聊天"))

    put_scrollable(put_scope('msg-box'), height=300, keep_bottom=True)
    nickname = "You"
    online_users.add(nickname)

    while True:
        data = await input_group(t('Send message', '发送消息'), [
            input(name='msg', help_text=t('Message content supports inline Markdown syntax', '消息内容支持行内Markdown语法')),
            actions(name='cmd', buttons=[t('Send', '发送'), t('Multiline Input', '多行输入'), {'label': t('Exit', '退出'), 'type': 'cancel'}])
        ], validate=lambda d: ('msg', 'Message content cannot be empty') if d['cmd'] == t('Send', '发送') and not d['msg'] else None)
        if data is None:
            break
        if data['cmd'] == t('Multiline Input', '多行输入'):
            data['msg'] = '\n' + await textarea('Message content', help_text=t('Message content supports Markdown syntax', '消息内容支持Markdown语法'))
        put_markdown('`%s`: %s' % (nickname, data['msg']), sanitize=True, scope='msg-box')
        chat_msgs.append((nickname, data['msg']))

        # 调用RWKV模型生成回复
        response = generate_response(data['msg'])
        put_markdown('`Assistant`: %s' % response, sanitize=True, scope='msg-box')
        chat_msgs.append(('Assistant', response))
