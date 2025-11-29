local autocmd = vim.api.nvim_create_autocmd

-- Автооткрытие nvim-tree при запуске
autocmd("VimEnter", {
  callback = function(data)
    -- Определяем, что было передано при запуске
    local is_directory = vim.fn.isdirectory(data.file) == 1
    local is_no_name = data.file == "" or data.file == nil
    
    if is_directory then
      -- Если это директория - перейти в неё и открыть дерево
      vim.cmd.cd(data.file)
      vim.schedule(function()
        require("nvim-tree.api").tree.open()
      end)
    elseif is_no_name then
      -- Если ничего не указано - открыть в текущей рабочей директории
      vim.schedule(function()
        require("nvim-tree.api").tree.open()
      end)
    else
      -- Если это файл - открыть дерево в директории файла
      local dir = vim.fn.fnamemodify(data.file, ":p:h")
      vim.cmd.cd(dir)
      vim.schedule(function()
        require("nvim-tree.api").tree.open()
      end)
    end
  end,
})

-- Закрыть Neovim если остался только nvim-tree
autocmd("BufEnter", {
  nested = true,
  callback = function()
    if #vim.api.nvim_list_wins() == 1 and
       vim.api.nvim_buf_get_name(0):match("NvimTree_") ~= nil then
      vim.cmd("quit")
    end
  end,
})


