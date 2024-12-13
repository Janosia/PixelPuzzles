import random
import json
from django.shortcuts import render
from django.http import JsonResponse

# Define cell types with their characteristics
CELL_TYPES = [
    {
        "type": "trap",
        "damage": (-10, -1),
        "image": "flame.png",
        "description": "Dangerous trap that reduces health"
    },
    {
        "type": "monster",
        "damage": (-5, -2),
        "image": "poison.png",
        "description": "Monsters that cause damage"
    },
    {
        "type": "healing",
        "damage": (1, 5),
        "image": "fairy.png",
        "description": "Healing spot that restores health"
    },
    {
        "type": "treasure",
        "damage": (0, 2),
        "image": "magic-wand.png",
        "description": "Treasure with minimal risk"
    },
    {
        "type": "empty",
        "damage": (0, 0),
        "image": "cat.png",
        "description": "Safe empty space"
    }
]

def generate_dungeon(request):
    """Generate a sophisticated dungeon with varied cell types"""
    rows = random.randint(4, 6)
    cols = random.randint(4, 6)
    
    # Create dungeon with cell types and damage values
    dungeon = []
    dungeon_details = []
    
    for _ in range(rows):
        row = []
        row_details = []
        for _ in range(cols):
            # Randomly select cell type
            cell_type = random.choice(CELL_TYPES)
            
            # Generate damage value within cell type's range
            damage = random.randint(cell_type['damage'][0], cell_type['damage'][1])
            
            row.append(damage)
            row_details.append({
                "type": cell_type['type'],
                "damage": damage,
                "image": cell_type['image']
            })
        
        dungeon.append(row)
        dungeon_details.append(row_details)
    
    return JsonResponse({
        'dungeon': dungeon,
        'dungeon_details': dungeon_details,
        'rows': rows,
        'cols': cols
    })

def game_view(request):
    """Render the main game page"""
    cell_types = CELL_TYPES
    return render(request, 'game/index.html', {'cell_types': cell_types})

# def game_view(request):
#     """Render the main game page"""
#     return render(request, 'game/index.html')

def calculate_minimum_health(request):
    """
    Calculate minimum health
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        dungeon = data.get('dungeon', [])
        
        def max_func(a, b):
            return a if a > b else b
        
        def calculate_min_hp(dungeon):
            r, c = len(dungeon), len(dungeon[0])
            I = 237627
            
            # Initialize DP array
            dp = [[I for _ in range(c)] for _ in range(r)]
            
            # Base case for bottom-right cell
            dp[r-1][c-1] = 0 if dungeon[r-1][c-1] > 0 else dungeon[r-1][c-1]
            
            # Fill last row
            for i in range(c-2, -1, -1):
                dp[r-1][i] = dungeon[r-1][i] + dp[r-1][i+1]
                dp[r-1][i] = 0 if dp[r-1][i] > 0 else dp[r-1][i]
            
            # Fill last column
            for j in range(r-2, -1, -1):
                dp[j][c-1] = dungeon[j][c-1] + dp[j+1][c-1]
                dp[j][c-1] = 0 if dp[j][c-1] > 0 else dp[j][c-1]
            
            def recurse(dp, dungeon, r, c):
                if dp[r][c] != I:
                    return dp[r][c]
                
                dp[r][c] = max_func(
                    dungeon[r][c] + (recurse(dp, dungeon, r+1, c) if r+1 < len(dungeon) else 0),
                    dungeon[r][c] + (recurse(dp, dungeon, r, c+1) if c+1 < len(dungeon[0]) else 0)
                )
                
                dp[r][c] = 0 if dp[r][c] > 0 else dp[r][c]
                return dp[r][c]
            
            h = recurse(dp, dungeon, 0, 0)
            
            if h > 1:
                return 1
            if h == 0:
                return 1
            if h < 0:
                h = abs(h) + 1
            
            return h
        
        min_health = calculate_min_hp(dungeon)
        
        return JsonResponse({
            'minimum_health': min_health
            })
