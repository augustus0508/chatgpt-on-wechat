import re

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from channel.chat_message import ChatMessage
from plugins import *
from plugins.trpg import dice


@plugins.register(
    name="trpg",
    desire_priority=100,
    desc="Being locked in a black room",
    version="0.1",
    author="augustus0508",
)
class Trpg(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context

    def on_handle_context(self, e_context: EventContext):
        if e_context['context'].type != ContextType.TEXT:
            return
        rd_regex=r'^\.r\d*d\d*$'
        context=e_context["context"].content
        if re.match(rd_regex, context):
            numbers = re.findall(r'\d+', context)
            para = [100, 1]
            for i, j in enumerate(reversed(numbers)):
                para[i] = int(j)

            msg: ChatMessage = e_context['context']['msg']
            reply = Reply()
            reply.type = ReplyType.TEXT
            if msg.is_group:
                reply.content = f'执行{para[1]}d{para[0]},{msg.actual_user_nickname}的投掷结果为：{str(dice.generate_random_integers(para[1], para[0]))}'
            else:
                reply.content = f'执行{para[1]}d{para[0]},{msg.from_user_nickname}的投掷结果为：{str(dice.generate_random_integers(para[1], para[0]))}'
            e_context['reply'] = reply
            e_context.action = EventAction.BREAK_PASS
            return
        return
