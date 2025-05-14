local Players = game:GetService("Players")
local player = Players.LocalPlayer

-- this does stuff
if not player.Character then
    player.CharacterAdded:Wait()
end

wait(1) -- anti stun fr
player.Character:Destroy
()
