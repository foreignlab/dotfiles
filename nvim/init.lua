vim.o.number = true
vim.o.relativenumber = true
vim.o.cursorline = true

vim.api.nvim_create_autocmd('InsertEnter', {
  pattern = '*',
  callback = function()
    vim.opt.relativenumber = false
  end
})

vim.api.nvim_create_autocmd('InsertLeave', {
  pattern = '*',
  callback = function()
    vim.opt.relativenumber = true
  end
})
  
vim.o.ignorecase = true
vim.o.smarttab = true
vim.o.smartcase = true
vim.o.incsearch = true

vim.o.swapfile = false
vim.o.undofile = true

vim.o.tabstop = 2
vim.o.shiftwidth = 2
vim.o.softtabstop = 2
vim.o.expandtab = true
vim.o.smartindent = true

vim.g.mapleader = ' '
vim.g.maplocalleader = ' '

-- WSL のときだけ Windows クリップボード(win32yank)と連携
if vim.fn.has("wsl") == 1 then
  vim.g.clipboard = {
    name = "win32yank-wsl",
    copy = {
      ["+"] = "win32yank.exe -i --crlf",
      ["*"] = "win32yank.exe -i --crlf",
    },
    paste = {
      ["+"] = "win32yank.exe -o --lf",
      ["*"] = "win32yank.exe -o --lf",
    },
    cache_enabled = 0,
  }
end

-- OS クリップボードをデフォルトレジスタと連携
vim.opt.clipboard = 'unnamedplus'

require('config.lazy')

vim.o.termguicolors = true
vim.cmd('colorscheme dracula')
