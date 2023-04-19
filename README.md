# Neovim GPT Plugin

nvim-gpt Plugin is a powerful and intuitive plugin designed to enhance your coding experience. It provides code explanations and general chat with OpenAI's GPT-3.5-turbo within Neovim using the OpenAI API.

## Features

- Explain selected code snippets in simple terms using OpenAI API
- Chat directly with OpenAI GPT-3.5-turbo using the `:GPT` command
- Maintain a continuous conversation with GPT, summarizing the conversation when necessary
- Automatically clean up conversation history when closing the split window

## Requirements

- Neovim 0.5 or later
- Python 3.6 or later
- pynvim 0.43 or later
- OpenAI API key

## Installation

### Using vim-plug

Add the following to your `init.vim` or `init.lua` file:

```vim
Plug 'lzhgus/neovim-gpt'
```
Then run `:PlugInstall`.

### Using Vundle

Add the following to your `init.vim` or `init.lua file:

```lua
Plugin 'lzhgus/nvim-gpt'
```

Then run `:PluginInstall`.

### Using Packer
```
local status, packer = pcall(require, "packer")
packer.startup(function(use)

  use {
    'lzhgus/nvim-gpt',
    config = function() vim.g.nvim_gpt_openai_api_key = "YOUR OPENAI API KEY" end,
  }
end)
```

## Configuration

Add the following line to your Neovim configuration (init.vim or init.lua) to configure your OpenAI API key:

```lua
vim.g.nvim_gpt_openai_api_key = '<YOUR_API_KEY>'
```

To set up the keybinding for the :ExplainCode command in Lua, add the following line to your init.lua:

```lua
vim.api.nvim_set_keymap('n', '<leader>ec', ':ExplainCode<CR>', {noremap = true, silent = true})
```

## Usage

### COde Explanation 

1. Select a piece of code in Neovim.
2. Run the `:ExplainCode` command or use the keybinding (`<leader>ec` by default) to get an explanation of the selected code. The explanation will be displayed in a new split window below the current buffer.

### Chat With GPT

1. Run the `:GPT` command followed by your message (e.g., `:GPT How do I reverse a string in Python?`). The response from GPT will be displayed in the same split window as code explanations.
2. Continue chatting with GPT by running the `:GPT` command with new messages. The plugin will maintain a conversation history and summarize it when necessary.
When you close the split window, the conversation history will be automatically cleaned up.