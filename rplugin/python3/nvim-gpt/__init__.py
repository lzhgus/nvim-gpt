import os
import pynvim
from .openai_api import OpenAI_API


@pynvim.plugin
class Nvim_GPT(object):
    def __init__(self, vim):
        self.vim = vim
        api_key = vim.vars.get('nvim_gpt_openai_api_key', None)
        if api_key is None:
            api_key = os.environ.get('OPENAI_API_KEY', None)
            if api_key is None:
                raise Exception(
                    "No OpenAI API key provided. Please set it in your Neovim configuration or as an environment variable.")
        self.openai_api = OpenAI_API(api_key)
        self.buffer_number = None
        self.current_buffer = None
        self.conversation_history = []

    def send_message(self, message, is_gpt=False):
        conversation_history_str = '\n'.join(self.conversation_history)
        response = self.openai_api.send_message(
            message, conversation_history_str)
        self.conversation_history.append(f"User: {message}")
        self.conversation_history.append(f"GPT: {response}")

        if not response:
            self.vim.command('echo "No explanation found."')
        elif response.startswith("Error"):
            self.vim.command(f'echoerr "{response}"')
        else:
            selected_code_title = "User: \n-------------" if is_gpt else "Selected Code: \n-------------"
            explanation_title = "\nGPT: \n------------ " if is_gpt else "\nExplanation\n------------"

            if self.buffer_number is not None:
                selected_code_title = "\n-------------\n" + selected_code_title
                self.current_buffer = self.vim.current.buffer.number
                self.vim.command(f"buffer {self.buffer_number}")
            else:
                self.vim.command('vnew')
                self.buffer_number = self.vim.current.buffer.number

            # Format selected code
            formatted_code = f"{selected_code_title} \n{message}\n"

            # Format explanation``
            formatted_explanation = response.replace('. ', '.\n')
            formatted_explanation = f"{explanation_title}\n{formatted_explanation}\n"

            # Combine formatted code and explanation
            formatted_content = f"{formatted_code}{formatted_explanation}"

            self.vim.current.buffer.append(formatted_content.splitlines())
            self.vim.command(
                'setlocal buftype=nofile bufhidden=hide noswapfile')
            self.vim.command('setlocal wrap')

            # switch back to the original buffer
            if self.current_buffer is not None:
                self.vim.command(f"buffer {self.current_buffer}")

    @pynvim.command('Explain', range="")
    def explain_code_command(self, range):
        code_text = self.vim.funcs.getline(range[0], range[1])
        code_text = "\n".join(map(str, code_text))
        self.conversation_history = []
        message = f"Explain the following code in simple terms:\n\n{code_text}\n"
        self.send_message(code_text)

    @pynvim.command('GPT', nargs='*')  # type: ignore
    def gpt_command(self, args):
        message = ' '.join(args)
        self.send_message(message, True)
