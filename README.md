# nvim-speech

Neovim plugin to record and convert speech to text.

Currently only supports [VASR][0], Google ASR support will be added soon.

<p align="center">
    <img src="https://i.imgur.com/K4kYnkL.gif" style="width:100%"/>
</p>


# Installation

| Plugin Manager | Install with... |
| ------------- | ------------- |
| [Pathogen][1] | `git clone https://github.com/vipul-sharma20/nvim-speech ~/.vim/bundle/nvim-speech`<br/>Remember to run `:Helptags` to generate help tags |
| [NeoBundle][2] | `NeoBundle 'vipul-sharma20/nvim-speech'` |
| [Vundle][3] | `Plugin 'vipul-sharma20/nvim-speech'` |
| [Plug][4] | `Plug 'vipul-sharma20/nvim-speech'` |
| [VAM][5] | `call vam#ActivateAddons([ 'nvim-speech' ])` |
| [Dein][6] | `call dein#add('vipul-sharma20/nvim-speech')` |
| [minpac][7] | `call minpac#add('vipul-sharma20/nvim-speech')` |
| manual | copy all of the files into your `~/.vim` directory |

This plugin works only on Python version 3 or above

### VASR Support

For VASR support, you'll also need to install Vernacular speech SDK:

  `pip install vernacular-ai-speech`

more doc [here][8]

### Google Support

🚧  *Coming Soon*


# Configuration

* Set ASR provider for the plugin. Can be 'vernacular' or 'google'

  `let g:asr_provider='vernacular'`

* Set ASR language code. Check language code for the providers below.

  `let g:asr_language_code=en-IN`

### Vernacular ASR

* Store API access token in `VERNACULAR_ACCESS_TOKEN` environment variable.

`export VERNACULAR_ACCESS_TOKEN="xxxxxxxxxxxxxxxxxxxxxxx"`

#### Language code

Vernacular ASR only supports indian languages for now. Use these language codes for following languages.

| Language | Code |
|--|--|
| Hindi | hi-IN |
| English | en-IN |
| Kannada | kn-IN |
| Malayalam| ml-IN |
| Bengali | bn-IN |
| Marathi | mr-IN |
| Gujarati | gu-IN |
| Punjabi | pa-IN |
| Telugu | te-IN |
| Tamil | ta-IN |

Set these code as:

`let g:asr_language_code="en-IN"`


### Google ASR

🚧  *Coming Soon*


# Documentation

`:h nvim-speech`


# Commands

| Command              | List |
| ---                  | --- |
| `Speech`             | Record speech and store transcription in `g:asr_transcription` |
| `SpeechEcho`         | Record speech and write transcription on current line |

Check some key bindings in the documentation `:h nvim-speech`


[0]: https://github.com/Vernacular-ai/speech-recognition
[1]: https://github.com/tpope/vim-pathogen
[2]: https://github.com/Shougo/neobundle.vim
[3]: https://github.com/VundleVim/Vundle.vim
[4]: https://github.com/junegunn/vim-plug
[5]: https://github.com/MarcWeber/vim-addon-manager
[6]: https://github.com/Shougo/dein.vim
[7]: https://github.com/k-takata/minpac/
[8]: https://github.com/Vernacular-ai/speech-recognition
