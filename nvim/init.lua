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

require('config.lazy')

vim.o.termguicolors = true
vim.cmd('colorscheme dracula')