local Timer = require "libraries.hump.timer"
-- Representations
local guard = nil
local obstacles = {}
local travelHistory = {}

-- Grid size and cell size for display
local cellSize = 32  -- Size of each cell in pixels
local gridWidth, gridHeight = 10, 10  -- Map dimensions
local mapData = {
    "....#.....",
    ".........#",
    "..........",
    "..#.......",
    ".......#..",
    "..........",
    ".#..^.....",
    "........#.",
    "#.........",
    "......#..."
}

-- Grid size and cell size for display
local cellSize = 48  -- Size of each cell in pixels
local mapData = {}  -- Will be loaded from an external file
local gridWidth, gridHeight = 0, 0  -- Map dimensions (updated dynamically)

-- Function to load the map from an external file
local function loadMapFromFile(filename)
    mapData = {}
    for line in love.filesystem.lines(filename) do
        table.insert(mapData, line)
    end
    gridWidth = #mapData[1]  -- Assuming all rows are of equal length
    gridHeight = #mapData
end

-- Parse the map into the new representation
local function parseMap()
    guard = nil
    obstacles = {}
    travelHistory = {}

    for r, line in ipairs(mapData) do
        for c = 1, #line do
            local cell = line:sub(c, c)
            if cell == "^" then
                guard = {x = c, y = r, direction = "^"} -- Store guard position and direction
            elseif cell == "#" then
                table.insert(obstacles, {x = c, y = r}) -- Store obstacle position
            end
        end
    end
end

-- Parse the map into the new representation
local function parseMap()
    for r, line in ipairs(mapData) do
        for c = 1, #line do
            local cell = line:sub(c, c)
            if cell == "^" then
                guard = {x = c, y = r, direction = "^"} -- Store guard position and direction
            elseif cell == "#" then
                table.insert(obstacles, {x = c, y = r}) -- Store obstacle position
            end
        end
    end
end

-- Directions and their corresponding movements
local directions = {
    ["^"] = {dx = 0, dy = -1},
    [">"] = {dx = 1, dy = 0},
    ["v"] = {dx = 0, dy = 1},
    ["<"] = {dx = -1, dy = 0}
}

-- Turn right (clockwise)
local function turn_right(direction)
    if direction == "^" then return ">" end
    if direction == ">" then return "v" end
    if direction == "v" then return "<" end
    if direction == "<" then return "^" end
end

-- Check if a position is an obstacle
local function is_obstacle(x, y)
    for _, obs in ipairs(obstacles) do
        if obs.x == x and obs.y == y then
            return true
        end
    end
    return false
end

-- Simulate one step of the guard's movement
local function simulateGuard()
    local entry = {x = guard.x, y = guard.y, size = 0}  -- Start with a size of 0
    table.insert(travelHistory, entry)

    -- Animate the size growth for this entry
    Timer.tween(0.8, entry, {size = cellSize / 3}, "in-out-quad")

    -- Calculate the next position
    local dir = directions[guard.direction]
    local nextX, nextY = guard.x + dir.dx, guard.y + dir.dy

    -- Check if the guard encounters an obstacle or boundary
    if nextX < 1 or nextY < 1 or nextY > gridHeight or nextX > gridWidth then
        guard.x, guard.y = nextX, nextY
        else
        if is_obstacle(nextX, nextY) then
            -- Turn right if blocked
            guard.direction = turn_right(guard.direction)
        else
            guard.x, guard.y = nextX, nextY
        end
    end
end

-- Love2D functions
function love.load()
    print("Save directory:", love.filesystem.getSaveDirectory())
    recording=true
    frameCounter = 0
    -- Load the map from an external file
    loadMapFromFile("sample.txt")  -- Replace "map.txt" with the name of your map file
    parseMap()  -- Parse the map and initialize the representations
end

-- Save the current frame
local function saveFrame()
    frameCounter = frameCounter + 1
    local filename = string.format("frames/frame_%04d.png", frameCounter)
    love.filesystem.createDirectory("frames")  -- Ensure the directory exists
    love.graphics.captureScreenshot(function(imageData)
        imageData:encode("png", filename)
    end)
end

function love.update(dt)
    Timer.update(dt)
    if recording then
        simulateGuard()
        if frameCounter < 200 then  -- Limit recording to 200 frames
            saveFrame()
        else
            recording = false
        end
    end
    -- Simulate the guard's movement periodically (e.g., every 0.2 seconds)
    if not(guard.x < 1 or guard.y < 1 or guard.y > gridHeight or guard.x > gridWidth) then
        if love.timer.getTime() % 0.1 < dt then
            simulateGuard()
        end
    end
end

function love.draw()
    -- Draw the grid
    for r = 1, gridHeight do
        for c = 1, gridWidth do
            love.graphics.setColor(0.8, 0.8, 0.8) -- Light gray for empty cells
            love.graphics.rectangle("line", (c - 1) * cellSize, (r - 1) * cellSize, cellSize, cellSize)
        end
    end

    -- Draw obstacles
    love.graphics.setColor(1, 0, 0) -- Red for obstacles
    for _, obs in ipairs(obstacles) do
        love.graphics.rectangle("fill", (obs.x - 1) * cellSize, (obs.y - 1) * cellSize, cellSize, cellSize)
    end

    -- Draw the guard
    love.graphics.setColor(0, 0, 1) -- Blue for the guard
    love.graphics.circle("fill", (guard.x - 1) * cellSize + cellSize / 2, (guard.y - 1) * cellSize + cellSize / 2, cellSize / 3)

    -- Draw the travel history
    love.graphics.setColor(0, 1, 0) -- Green for the travel path
    -- Draw the travel history with animation
    for _, entry in ipairs(travelHistory) do
        love.graphics.setColor(1, 1-1/entry.size, 0) -- Green for the travel path
        love.graphics.circle("fill", (entry.x - 1) * cellSize + cellSize / 2, (entry.y - 1) * cellSize + cellSize / 2, entry.size)
    end
end
