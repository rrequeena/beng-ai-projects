# PONG Game - Flow Diagrams

## 1. Main Game Loop Flow

```mermaid
graph TD
    A["Start Application"] --> B["Initialize Game"]
    B --> C{"Game State?"}
    C -->|MENU| D["Display Main Menu"]
    C -->|IN_GAME| E["Update Game Logic"]
    C -->|GAME_OVER| F["Display Game Over Screen"]
    
    D -->|Start Game| G["Set Points Target"]
    G -->|Confirm| H["Transition to IN_GAME"]
    
    E --> I["Process Player Input"]
    I --> J["Update Physics"]
    J --> K["Check Collisions"]
    K --> L["Update AI"]
    L --> M["Update Score"]
    M --> N["Render Frame"]
    N --> O{Winner?}
    O -->|No| C
    O -->|Yes| F
    
    F -->|Play Again| D
    F -->|Quit| P["Exit Application"]
```

## 2. Game Initialization Flow

```mermaid
graph TD
    A["Start Game"] --> B["Load Configuration"]
    B --> C["Initialize Pygame"]
    C --> D["Create Game Window"]
    D --> E["Create Player Paddle<br/>Left Side"]
    E --> F["Create CPU Paddle<br/>Right Side"]
    F --> G["Create Ball<br/>Center Position"]
    G --> H["Initialize Physics System"]
    H --> I["Initialize Collision System"]
    I --> J["Initialize AI System"]
    J --> K["Setup Input Handler"]
    K --> L["Initialize UI Manager"]
    L --> M["Game Ready<br/>Show Menu"]
```

## 3. Physics & Movement System

```mermaid
graph TD
    A["Physics Update<br/>Called at 60 FPS"] --> B["Get Current State"]
    B --> C["Calculate Delta Time"]
    C --> D{"Entity Type?"}
    
    D -->|Paddle| E["Clamp Y Position<br/>Within Bounds"]
    E --> F["Update Paddle Position"]
    
    D -->|Ball| G["Apply Velocity<br/>to Position"]
    G --> H["Check Boundary Collision"]
    H --> I{"Out of Bounds?"}
    I -->|Top/Bottom| J["Reflect Ball Velocity Y"]
    I -->|Left/Right| K["Reset Ball & Score"]
    
    J --> L["Update Ball Position"]
    K --> L
    L --> M["Return Updated State"]
```

## 4. Collision Detection & Response

```mermaid
graph TD
    A["Collision Check<br/>Every Frame"] --> B["Get Ball Rectangle"]
    B --> C["Get Paddle Rectangles"]
    
    C --> D{"Ball Collides<br/>with Paddle?"}
    
    D -->|Yes| E{"Which Paddle?"}
    E -->|Left Paddle| F["Calculate Paddle Section"]
    E -->|Right Paddle| G["Calculate Paddle Section"]
    
    F --> H["Reflect Ball Velocity X"]
    G --> H
    
    H --> I["Calculate Speed Increase<br/>Based on Hit Location"]
    I --> J["Increase Ball Velocity<br/>5-10%"]
    J --> K["Update Ball Direction"]
    
    D -->|No| L["No Collision<br/>Continue"]
    K --> L
    L --> M["Return Collision Result"]
```

## 5. AI Decision Making Flow

```mermaid
graph TD
    A["AI Update<br/>Called at 60 FPS"] --> B["Get Ball Position"]
    B --> C["Get CPU Paddle Position"]
    C --> D{"Difficulty Level?"}
    
    D -->|Easy| E["Move Toward Ball<br/>60% Speed"]
    D -->|Medium| F["Move Toward Ball<br/>80% Speed<br/>+ Small Random Error"]
    D -->|Hard| G["Predict Ball Trajectory<br/>Move to Intercept<br/>90% Speed"]
    
    E --> H["Apply Movement Constraints"]
    F --> H
    G --> H
    
    H --> I["Clamp Position to Bounds"]
    I --> J["Update AI Paddle Position"]
    J --> K["Return Updated State"]
```

## 6. Main Menu Flow

```mermaid
graph TD
    A["Display Main Menu"] --> B["Show Menu Options"]
    B --> C["Display Title & Instructions"]
    C --> D{"Player Input?"}
    
    D -->|Start Game| E["Transition to Settings"]
    D -->|Quit| F["Exit Application"]
    
    E --> G["Show Point Target Selection"]
    G --> H{"Select Points?"}
    
    H -->|5 Points| I["Set Win Condition = 5"]
    H -->|10 Points| J["Set Win Condition = 10"]
    H -->|15 Points| K["Set Win Condition = 15"]
    H -->|Custom| L["Input Custom Value"]
    
    I --> M["Show Difficulty Selection"]
    J --> M
    K --> M
    L --> M
    
    M --> N{"Select Difficulty?"}
    
    N -->|Easy| O["Set AI Difficulty = Easy"]
    N -->|Medium| P["Set AI Difficulty = Medium"]
    N -->|Hard| Q["Set AI Difficulty = Hard"]
    
    O --> R["Reset Game State"]
    P --> R
    Q --> R
    
    R --> S["Transition to IN_GAME"]
```

## 7. Score & Win Condition Flow

```mermaid
graph TD
    A["Ball Out of Bounds"] --> B{"Which Side?"}
    
    B -->|Player Side<br/>Left| C["CPU Scores Point"]
    B -->|CPU Side<br/>Right| D["Player Scores Point"]
    
    C --> E["CPU Score += 1"]
    D --> F["Player Score += 1"]
    
    E --> G["Reset Ball Position"]
    F --> G
    
    G --> H["Render Updated Scores"]
    H --> I{Check Win Condition}
    
    I -->|Player Score = Target| J["Set Game State<br/>= GAME_OVER"]
    I -->|CPU Score = Target| K["Set Game State<br/>= GAME_OVER"]
    I -->|Neither| L["Continue Game"]
    
    J --> M["Display Winner Message<br/>= PLAYER"]
    K --> N["Display Winner Message<br/>= CPU"]
    
    M --> O["Show Game Over Menu"]
    N --> O
```

## 8. Input Handling Flow

```mermaid
graph TD
    A["Input Event Detected"] --> B{"Event Type?"}
    
    B -->|Key Down| C{"Which Key?"}
    B -->|Key Up| D["Release Movement"]
    B -->|Window Close| E["Set Running = False"]
    
    C -->|W Key| F["Player Move Up"]
    C -->|S Key| G["Player Move Down"]
    C -->|SPACE| H["Pause/Resume Game"]
    C -->|ESC| I["Return to Menu"]
    
    F --> J["Set Player Velocity = -MAX_SPEED"]
    G --> K["Set Player Velocity = +MAX_SPEED"]
    H --> L["Toggle Pause State"]
    I --> M["Reset Game to Menu"]
    
    D --> N["Set Velocity = 0"]
    
    J --> O["Queue Movement Update"]
    K --> O
    N --> O
    L --> O
    M --> O
```

## 9. Frame Rendering Flow

```mermaid
graph TD
    A["Render Frame<br/>60 FPS"] --> B["Clear Screen<br/>Black Background"]
    
    B --> C["Draw Game Elements"]
    C --> D["Draw Center Dashed Line"]
    D --> E["Draw Left Paddle"]
    E --> F["Draw Right Paddle"]
    F --> G["Draw Ball"]
    
    G --> H["Draw Score Display"]
    H --> I["Draw Player Score<br/>Left Side"]
    I --> J["Draw CPU Score<br/>Right Side"]
    
    J --> K["Draw Status Info"]
    K --> L{"Game State?"}
    
    L -->|IN_GAME| M["Draw Frame Counter"]
    L -->|PAUSED| N["Draw PAUSED Text"]
    
    M --> O["Update Display"]
    N --> O
    
    O --> P["Cap FPS at 60"]
```

## 10. Game States Diagram

```mermaid
stateDiagram-v2
    [*] --> MENU
    
    MENU --> SETTINGS: Start Button
    SETTINGS --> IN_GAME: Confirm Settings
    
    IN_GAME --> PAUSED: Space Key
    PAUSED --> IN_GAME: Resume
    PAUSED --> MENU: Escape Key
    
    IN_GAME --> GAME_OVER: Win Condition Met
    IN_GAME --> MENU: Escape Key
    
    GAME_OVER --> MENU: Menu Button
    GAME_OVER --> IN_GAME: Play Again
    
    MENU --> [*]: Quit
```
