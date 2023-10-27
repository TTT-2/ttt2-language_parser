-- English language strings

local L = LANG.CreateLanguage("en")

-- Compatibility language name that might be removed soon.
-- the alias name is based on the original TTT language name:
-- https://github.com/Facepunch/garrysmod/blob/master/garrysmod/gamemodes/terrortown/gamemode/lang/english.lua
L.__alias = "english"

L.lang_name = "English (English)"

-- General text used in various places
L.traitor = "Traitor"
L.detective = "Detective"
L.innocent = "Innocent"
L.last_words = "Last Words"

-- 2023-10-25
L.help_keyhelp = [[
Key bind helpers are part of a UI element that always shows relevant keybindings to the player, which is especially helpful for new players. There are three different types of key bindings:

Core: These contain the most important bindings found in TTT2. Without them the game is hard to play to its full potential.
Extra: Similar to core, but you don't always need them. They contain stuff like chat, voice or flashlight. It might be helpful for new players to enable this.
Equipment: Some equipment items have their own bindings, these are shown in this category.

Disabled categories are still shown when the scoreboard is visible]]

L.label_keyhelp_show_core = "Enable always showing the core bindings"
L.label_keyhelp_show_extra = "Enable always showing the extra bindings"
L.label_keyhelp_show_equipment = "Enable always showing the equipment bindings"
