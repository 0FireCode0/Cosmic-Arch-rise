return {
  -- Catppuccin тема
  {
    "catppuccin/nvim",
    name = "catppuccin",
    priority = 1000,
    config = function()
      require("catppuccin").setup({
        flavour = "mocha",
        transparent_background = true,
        integrations = {
          nvimtree = true,
          treesitter = true,
          cmp = true,
          gitsigns = true,
          telescope = true,
          which_key = true,
          mason = true,
          native_lsp = {
            enabled = true,
          },
        },
      })
    end,
  },

  -- Настройка nvim-tree
  {
    "nvim-tree/nvim-tree.lua",
    cmd = { "NvimTreeToggle", "NvimTreeFocus" },
    config = function()
      local nvtree = require("nvim-tree")
      
      nvtree.setup({
        disable_netrw = true,
        hijack_netrw = true,
        hijack_cursor = true,
        hijack_unnamed_buffer_when_opening = true,
        
        -- КЛЮЧЕВЫЕ НАСТРОЙКИ
        sync_root_with_cwd = true,
        respect_buf_cwd = false,
        update_cwd = true,
        prefer_startup_root = false,  -- НЕ предпочитать стартовый корень
        
        view = {
          width = 35,
          side = "left",
          preserve_window_proportions = true,
        },
        
        renderer = {
          root_folder_label = function(path)
            return "  " .. vim.fn.fnamemodify(path, ":~")
          end,
          highlight_git = true,
          indent_markers = {
            enable = true,
          },
          icons = {
            show = {
              file = true,
              folder = true,
              folder_arrow = true,
              git = true,
            },
          },
        },
        
        update_focused_file = {
          enable = true,
          update_root = false,
        },
        
        filters = {
          dotfiles = false,
        },
        
        git = {
          enable = true,
          ignore = false,
        },
        
        actions = {
          change_dir = {
            enable = true,
            global = true,
          },
          open_file = {
            quit_on_open = false,
            window_picker = {
              enable = true,
            },
          },
        },
        
        -- Важно: не фиксировать корень
        filesystem_watchers = {
          enable = true,
        },
      })
    end,
  },
  {
    "VidocqH/data-viewer.nvim",
    dependencies = {
      "nvim-lua/plenary.nvim",
      "kkharji/sqlite.lua", -- чтобы смотреть SQLite файлы
    },
    cmd = { "DataViewer", "DataViewerNextTable", "DataViewerPrevTable", "DataViewerClose" },
    opts = {
      -- пример настроек (можешь оставить пустым, если хочешь)
      width = 0.8,  -- ширина окна (80% экрана)
      height = 0.8, -- высота окна
      border = "rounded",
      filetypes = { "csv", "tsv", "json", "sqlite", "db", "sqlite3" },
    },
    keys = {
      { "<leader>dv", "<cmd>DataViewer<CR>", desc = "Открыть Data Viewer" },
    },
  },
}
