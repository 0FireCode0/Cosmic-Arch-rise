require "nvchad.mappings"

-- add yours here

local map = vim.keymap.set

map("n", ";", ":", { desc = "CMD enter command mode" })
map("i", "jk", "<ESC>")

-- map({ "n", "i", "v" }, "<C-s>", "<cmd> w <cr>")
--
map("n", "<C-b>", "<cmd>NvimTreeToggle<CR>", { desc = "Toggle nvim-tree" })
require "nvchad.mappings"

-- add yours here

local map = vim.keymap.set

map("n", ";", ":", { desc = "CMD enter command mode" })
map("i", "jk", "<ESC>")

-- map({ "n", "i", "v" }, "<C-s>", "<cmd> w <cr>")
--
map("n", "<leader>e", "<cmd>NvimTreeFocus<CR>", { desc = "Focus nvim-tree" })
map("n", "<leader>nf", "<cmd>NvimTreeFindFile<CR>", { desc = "Find file in tree" })

-- Команды для смены корня
map("n", "<leader>nc", function()
  require("nvim-tree.api").tree.change_root_to_node()
end, { desc = "Change root to node" })

map("n", "<leader>nu", function()
  require("nvim-tree.api").tree.change_root_to_parent()
end, { desc = "Change root to parent" })

map("n", "<leader>nh", function()
  local api = require("nvim-tree.api")
  api.tree.change_root(vim.fn.expand("~"))
end, { desc = "Change root to home" })

map("n", "<leader>n/", function()
  local api = require("nvim-tree.api")
  api.tree.change_root("/")
end, { desc = "Change root to /" })

-- Навигация между окнами
map("n", "<C-h>", "<C-w>h", { desc = "Window left" })
map("n", "<C-l>", "<C-w>l", { desc = "Window right" })
map("n", "<C-j>", "<C-w>j", { desc = "Window down" })
map("n", "<C-k>", "<C-w>k", { desc = "Window up" })

-- Быстрое сохранение
map("n", "<C-s>", "<cmd>w<CR>", { desc = "Save file" })
map("i", "<C-s>", "<ESC><cmd>w<CR>", { desc = "Save file" })

map("n" ,"<leader>dv", "<cmd>DataViewer<CR>", {desc = "Открыть Data Viewer" })

