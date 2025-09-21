local lazypath = vim.fn.stdpath('data') .. '/lazy/lazy.nvim'
if not (vim.uv or vim.loop).fs_stat(lazypath) then
  vim.fn.system({
    'git',
    'clone',
    '--filter=blob:none',
    'https://github.com/folke/lazy.nvim.git',
    '--branch=stable', -- latest stable release
    lazypath,
  })
end

vim.opt.rtp:prepend(lazypath)

require('lazy').setup({
  { 'folke/lazy.nvim', version = false },
  { 'dracula/vim', name = 'dracula' },
  {
    'MeanderingProgrammer/render-markdown.nvim',
    dependencies = { 'nvim-treesitter/nvim-treesitter', 'echasnovski/mini.nvim' },
    opts = {
      -- render_modes = { 'n', 'c', 'v' },
      render_modes = true,
      anti_conceal = { enabled = true },
      heading = {
        position = "inline",
        style = "bold",
        icons = {},
      },
    },
  },
})