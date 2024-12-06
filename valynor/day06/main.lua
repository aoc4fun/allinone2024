local current_color = {1, 1, 1, 1}
local seconds=0
local animation=nil
local dices = {}
love.graphics.setDefaultFilter( "nearest","nearest" )
Timer = require 'libraries/hump/timer'
Class = require "libraries/classic/classic"

function PrintTable(_table)
  for key, value in pairs(_table) do
    print(key .. ": " .. tostring(value))
  end
end

local cursorX, cursorY -- Position of the '^'
local direction = {dx = -1, dy = 0} -- initial direction is up
local steps = 0
local done = false
local timeAccumulator = 0
local moveInterval = 0.005 -- move every 1 second

-- Function to turn direction right
local function turnRight(dir)
    -- Up (-1,0), Right(0,1), Down(1,0), Left(0,-1)
    if dir.dx == -1 and dir.dy == 0 then
        -- Up -> Right
        dir.dx, dir.dy = 0, 1
    elseif dir.dx == 0 and dir.dy == 1 then
        -- Right -> Down
        dir.dx, dir.dy = 1, 0
    elseif dir.dx == 1 and dir.dy == 0 then
        -- Down -> Left
        dir.dx, dir.dy = 0, -1
    elseif dir.dx == 0 and dir.dy == -1 then
        -- Left -> Up
        dir.dx, dir.dy = -1, 0
    end
end


function love.load()
    love.window.setVSync( false )
  local name, version, vendor, device = love.graphics.getRendererInfo( )
  print("Renderer : ".. name .. "\nVersion: " .. version .. "\nVendor: " .. vendor .. "\nDevice: ".. device)
  local features = love.graphics.getSupported( )
  print("----------------------- Features")
  PrintTable(features)
  local limits = love.graphics.getSystemLimits( )
  print("----------------------- Limits")
  PrintTable(limits)
  local scale = love.graphics.getDPIScale( )
  print("----------------------- HDPI")
  print("HDPI Scale : " .. scale)
  Gametimer = Timer()
--  local f, error = contents, size = love.filesystem.read("sample.txt")
    mapData = {}
    for line in love.filesystem.lines("06.txt") do
        table.insert(mapData, line)
    end
    cellSize = 10       -- Taille de la cellule
    rectSize = 8        -- Taille du rectangle à l'intérieur de la cellule
    margin = (cellSize - rectSize) / 2  -- Pour centrer le rectangle dans la cellule
    -- Find the '^' in the map
    for r, line in ipairs(mapData) do
        local c = line:find("%^")
        if c then
            cursorY = r
            cursorX = c
            -- Replace '^' with '.' since it's just a marker
            local before = line:sub(1, c-1)
            local after = line:sub(c+1)
            mapData[r] = before .. "." .. after
            break
        end
    end
end

local function isOutsideMap(x, y)
    return y < 1 or y > #mapData or x < 1 or x > #mapData[1]
end

function love.draw()
  local stats = love.graphics.getStats()
  local r, g, b, a = love.graphics.getColor( )
  love.graphics.setColor( 0,0,0 )
--  love.graphics.print(str1, 10, 10)
  --love.graphics.print(str2, 10, 30)
    -- Parcourir les lignes et les colonnes de la carte
    for rowIndex, line in ipairs(mapData) do
        for colIndex = 1, #line do
            local char = line:sub(colIndex, colIndex)

            local x = (colIndex - 1) * cellSize
            local y = (rowIndex - 1) * cellSize

            if char == '.' then
                love.graphics.setColor(0, 0, 1)
                love.graphics.rectangle("fill", x + margin, y + margin, rectSize, rectSize)
            elseif char == '#' then
                love.graphics.setColor(1, 0, 0)
                love.graphics.rectangle("fill", x + margin, y + margin, rectSize, rectSize)
            else
                love.graphics.setColor(1, 1, 1)
                local cell = mapData[rowIndex]:sub(colIndex, colIndex)
                local line = mapData[rowIndex]
                -- nextX est la position de la colonne à modifier
                mapData[cursorY] = line:sub(1, cursorX - 1) .. "5" .. line:sub(cursorX + 1)
                love.graphics.rectangle("fill", x + margin, y + 5, rectSize, rectSize)
            end
        end
    end

    -- Draw the cursor
    if not done then
        local cx = (cursorX - 1) * cellSize
        local cy = (cursorY - 1) * cellSize
        love.graphics.setColor(0, 1, 0)
        love.graphics.rectangle("fill", cx + margin, cy + margin, rectSize, rectSize)
    end

    love.graphics.setColor(1, 1, 1)
    if done then
        love.graphics.print("Number of steps: " .. steps, 10, 10)
    end
end

function love.keypressed(pressed_key)
  if pressed_key == 'escape' then
    love.event.quit()
  end
end

function love.mousereleased(x, y, button)

end

function love.mousepressed(x, y, button)

end

function love.mousemoved(x, y, dx, dy)

end

function love.update(dt)
  Gametimer:update(dt)
    if done then return end

    timeAccumulator = timeAccumulator + dt
    if timeAccumulator >= moveInterval then
        timeAccumulator = timeAccumulator - moveInterval

        -- Check next cell in the current direction
        local nextX = cursorX + direction.dy
        local nextY = cursorY + direction.dx
        -- Note: careful with row/col indexing
        -- Here, rowIndex = y, colIndex = x
        -- We took cursorY as row, cursorX as column.
        -- direction is defined as (dx,dy) with dx in row-direction, dy in col-direction:
        -- dx changes rows (vertical), dy changes columns (horizontal)
        -- So the next cell is (cursorY + dx, cursorX + dy).

        nextY = cursorY + direction.dx
        nextX = cursorX + direction.dy

        if isOutsideMap(nextX, nextY) then
            -- Outside map
            done = true
            print("Number of steps:", steps+1)
        else
            local cell = mapData[nextY]:sub(nextX, nextX)
            local line = mapData[cursorY]
            -- nextX est la position de la colonne à modifier
            mapData[cursorY] = line:sub(1, cursorX - 1) .. "0" .. line:sub(cursorX + 1)
            if cell == '#' then
                -- Turn right, don't move
                turnRight(direction)
            elseif cell == '.' then
                -- Move forward
                cursorX, cursorY = nextX, nextY
                steps = steps + 1
            else
                -- If there are other chars, treat them as '.'
                cursorX, cursorY = nextX, nextY
            end
        end
    end
end

