from cmu_graphics import *
import math
import random
from random import uniform, randint 
from random import gauss
from PIL import Image

def onAppStart(app):
    # Define general app properties
    app.currentScreen = "home"
    app.instructions = [
        "You have 20 years to make moolah. The bar will go down over the course of one year.",
        "Every 6 months, your pocket cash will refill with $5,000 you can invest.",
        "There are 3 different investment opportunities you can unlock through the game: Savings, CDS, & Stocks",
        "The Savings Account plays the role of a secure place where players can deposit or withdraw money to manage their financial resources strategically. Players also gain an interest of 1% each year",
        "Certificates of Deposit (CDs) serve as a low-risk investment option where players can lock their money for a fixed term to earn guaranteed returns.",
        "Lastly, stocks represent a higher-risk, higher-reward investment option where players can buy shares in companies to potentially earn returns through price increases or dividends.",
        "However, their value fluctuates based on market conditions, which means there are risks and rewards of equity investments.",
        "There also other features that will allow you to keep track of your stocks, helping you make your investment choices (Click on 'm' when you click on stock chart for a surprise).",
        "This is a single-player game against the computer!",
        "If you beat the computer by the end of 20 years, good for you!",
        "END OF TUTORIAL"
    ]
    app.currentInstructionIndex = 0
    app.textWrapWidth = 300  # Maximum width for the text before wrapping
    startColor = rgb(52, 119, 105)
    instructionColor = rgb(112, 167, 244)
    # Define button positions and sizes
    app.startButton = {'x': 325, 'y': 225, 'width': 200, 'height': 50, 'color': startColor, 'border': 'black'}
    app.instructionsButton = {'x': 325, 'y': 325, 'width': 200, 'height': 50, 'color': instructionColor, 'border': 'black'}
    app.exitButton = {'x': 67, 'y': 560, 'width': 100, 'height': 30, 'color': 'lightcoral', 'border': 'darkred'}
    app.nextButton = {'x': 350, 'y': 400, 'width': 200, 'height': 50, 'color': 'gold', 'border': 'orange'}
    app.instructionsExitButton = {'x': 350, 'y': 480, 'width': 200, 'height': 50, 'color': 'lightcoral', 'border': 'darkred'}
    app.pause = {'x': 150, 'y': 700, 'width': 100, 'height': 40, 'color': 'lightcoral', 'border': 'darkred'}

    # Game-specific properties
    app.pocketCash = 5000.00
    app.netWorth = 5000.00
    app.savings = 0.00
    app.currentYear = 0
    app.totalYears = 20
    app.savingsInterestRate = 0.001  # 0.1% interest per step

    # CD
    app.cds = []
    app.cd_price = 0.00
    app.cdHoldings = 0
    app.CDButton = {'x': 650, 'y': 190, 'width': 100, 'height': 50, 'color': 'lightgreen', 'border': 'darkgreen'}
    app.CDScreen = False
    app.CDactiveInput = None
    app.CDInputField = {'x': 630, 'y': 240, 'width': 150, 'height': 30, 'border': 'black'}
    app.CDInputValue = ""
    app.buyCDButton = {'x': 780, 'y': 240, 'width': 50, 'height': 30, 'color': 'white', 'border': 'black'}
    app.exitCDButton = {'x': 590, 'y': 240, 'width': 40, 'height': 30, 'color': 'white', 'border': 'black'}
    app.CDbutton1 = {'x': 620, 'y': 160, 'radius': 35,'color': 'cyan', 'border': 'black'}
    app.CDbutton2 = {'x': 720, 'y': 160, 'radius': 35,'color': 'cyan', 'border': 'black'}
    app.CDbutton3 = {'x': 820, 'y': 160, 'radius': 35,'color': 'cyan', 'border': 'black'}
    app.CDtime = None
    app.CDAPY = random.uniform(1.05, 1.1)

    #STOCKS
    app.buyButtons = [
        {'x': 293, 'y': 540, 'width': 50, 'height': 30, 'color': 'white', 'border': 'black'},
        {'x': 443, 'y': 540, 'width': 50, 'height': 30, 'color': 'white', 'border': 'black'},
        {'x': 593, 'y': 540, 'width': 50, 'height': 30, 'color': 'white', 'border': 'black'},
        {'x': 743, 'y': 540, 'width': 50, 'height': 30, 'color': 'white', 'border': 'black'}
    ]
    app.sellButtons = [
        {'x': 353, 'y': 540, 'width': 50, 'height': 30, 'color': 'white', 'border': 'black'},
        {'x': 503, 'y': 540, 'width': 50, 'height': 30, 'color': 'white', 'border': 'black'},
        {'x': 653, 'y': 540, 'width': 50, 'height': 30, 'color': 'white', 'border': 'black'},
        {'x': 803, 'y': 540, 'width': 50, 'height': 30, 'color': 'white', 'border': 'black'}
    ]
    app.stocks = [
        Stock("15112", 50),
        Stock("RevNoodle", 80),
        Stock("Exchange", 120),
        Stock("Millie's", 200)
    ]
    app.stockShares = [0, 0, 0, 0]  # Number of shares owned for each stock\
    app.stockAmount = [None, None, None, None]

    #Choices for Stock
    app.stockChoices = []
    x_positions = [290, 320, 350, 380, 440, 470, 500, 530, 590, 620, 650, 680, 740, 770, 800, 830]
    app.labels = ["1", "10", "25", "Max"] * 4  # Repeat the labels for all choices

    # Create the stock choices
    for x in x_positions:
        stockChoice = {'x': x, 'y': 510, 'width': 25, 'height': 25, 'color': 'white', 'border': 'black'}
        app.stockChoices.append(stockChoice)


    # Input field for typing amount
    app.activeInput = None
    app.inputValue = ""
    app.inputField = {'x': 265, 'y': 150, 'width': 150, 'height': 30, 'border': 'black'}

    # Progress bar
    app.progressBarWidth = 0
    app.progressBarIncrement = 60 / (120)  # Increment width every step (2 mins = 120 secs)

    # Leaderboard
    app.leaderboardButton = {'x': 25, 'y': 220, 'width': 200, 'height': 30, 'color': 'lightblue', 'border': 'darkblue'}
    app.showLeaderboard = False
    app.computerNetWorth = 5000
    app.cpocketCash = 5000.00
    app.csavings = 0.00
    app.cstockShares = [0, 0, 0, 0]  # Number of shares owned for each stock\
    app.cstockAmount = [None, None, None, None]
    app.ccds = []
    app.ccd_price = 0.00
    app.ccdHoldings = 0
    #Pop Up
    app.showPopup = False  # Flag to toggle the pop-up
    app.popupContent = ""  # Message displayed in the pop-up
    app.popupTimer = 0  # Timer to track the duration of the pop-up
    #Stock Chart
    app.stockChartButton = {'x': 25, 'y': 260, 'width': 200, 'height': 30, 'color': 'lightblue', 'border': 'darkblue'}
    app.showStockChart = False
    app.currentChartType = 1 

    #Pie Chart
    app.pieChartButton = {'x': 25, 'y': 300, 'width': 200, 'height': 30, 'color': 'lightblue', 'border': 'darkblue'}
    app.showPieChart = False
    app.pie = [app.pocketCash, app.savings, getCDSPrice(app), getStockPrices(app)]
    color1 = rgb(96, 80, 220)
    color2 = rgb(213, 45, 183)
    color3 = rgb(255, 46, 126)
    color4 = rgb(255, 107, 69)
    app.pieColor = [color1, color2, color3, color4]
    app.pieCenter = (495, 300)
    app.pieRadius = 75
    app.hoveredIndex = None  # Index of the hovered pie slice

    app.economicEvents = [
        {"description": "Less students are enrolling in 15112, course too hard", "effect": {"15112": -0.1}},
        {"description": "CMU students heard 15112 was giving away free As", "effect": {"15112": 0.15}},
        {"description": "Millie’s is receiving more customers", "effect": {"Millie's": 0.2}},
        {"description": "The Exchange stopped selling the Leonardo", "effect": {"Exchange": -0.15}},
        {"description": "Stories has it that the Exchange has a new menu", "effect": {"Exchange": 0.1}},
        {"description": "Millie’s hired more workers", "effect": {"Millie's": 0.05}},
        {"description": "RevNoodle unleashed a new type of noodles", "effect": {"RevNoodle": 0.1}},
        {"description": "Economic Recession", "effect": {"15112": -0.2, "Millie's": -0.2, "Exchange": -0.3, "RevNoodle": -0.1}},
        {"description": "Economic Boom", "effect": {"15112": 0.3, "Millie's": 0.3, "Exchange": 0.2, "RevNoodle": 0.2}}
    ]

    app.currentEvent = ""  # To track the current event
    app.predictedEvent = []  # Predicted economic event
    # News button
    app.newsButton = {'x': 25, 'y': 340, 'width': 200, 'height': 30, 'color': 'lightblue', 'border': 'darkblue'}
    app.showNews = False  # Toggle for showing news prediction

def wrapText(text, maxWidth, lineHeight, start):
    """Splits the given text into lines, ensuring no line exceeds the maxWidth."""
    words = text.split()
    lines = []
    line = ""
    for word in words:
        if len(line + word) * 7 <= maxWidth:  # Approximate width calculation
            line += (word + " ")
        else:
            lines.append(line.strip())
            line = word + " "
    lines.append(line.strip())  # Add the last line

    return [(lines[i], start + i * lineHeight) for i in range(len(lines))]  # Start at y=250

def computerStrategy(app):
    """
    Simulates the computer player's investment strategy for one step (e.g., 6 months).
    The computer randomly allocates its investments across stocks, CDs, and savings.
    """
    # Randomly generate allocations that sum to 1
    allocations = [random.uniform(0, 1) for _ in range(4)]
    total_allocation = sum(allocations)
    allocations = [alloc / total_allocation for alloc in allocations]  # Normalize to sum to 1

    stockAllocation, cdAllocation, savingsAllocation, keepCashAllocation = allocations

    # Calculate investable cash
    totalCash = app.computerNetWorth
    investableCash = app.cpocketCash

    # Calculate allocations
    toStocks = investableCash * stockAllocation
    toCDs = investableCash * cdAllocation
    toSavings = investableCash * savingsAllocation
    keepCash = investableCash * keepCashAllocation

    # Update savings
    app.csavings += toSavings

    # Buy CDs
    if toCDs >= 500:  # Minimum requirement to invest in CDs
        app.ccdHoldings += 1
        app.ccds.append(CD("CD", base_price=toCDs, APY=app.CDAPY, maturity_time=12))
        app.ccd_price += toCDs

    # Buy stocks
    for stock in app.stocks:
        numShares = toStocks // stock.current_price
        if numShares > 0:
            stock.bought_price = stock.current_price
            app.cstockShares[app.stocks.index(stock)] += numShares
            toStocks -= numShares * stock.current_price

    app.cpocketCash = keepCash
    # Update computer net worth
    app.computerNetWorth = (
        app.cpocketCash +
        app.csavings +
        sum(cd.current_price for cd in app.ccds) +
        sum(stock.bought_price * app.cstockShares[app.stocks.index(stock)] for stock in app.stocks)
    )
def drawHomeScreen(app):
    # Draw background
    picture = "money5.jpg"
    drawImage(picture, 0, 0)
    # Title
    titleColor = rgb (36, 76, 60)
    drawLabel("WealthFrontier", 450, 125, size=75, bold=True, fill=titleColor, font = 'impact',  border = 'black')
    
    # Buttons
    drawButton(app.startButton, "Start Game", 'black')
    drawButton(app.instructionsButton, "Instructions", 'black')
    drawButton(app.pause, "pause", 'darkred')


def drawInstructionsScreen(app):
    # Draw background
    background = "pink.webp"
    drawImage(background, 0, 0)
    # Draw instruction text
    instruction = app.instructions[app.currentInstructionIndex]
    wrappedText = wrapText(instruction, app.textWrapWidth, 40, 200)  # Wrap text to fit within the screen

    drawLabel("Instructions", 450, 100, size=80, bold=True, fill='red', border = 'black', font = 'impact' )
    drawButton(app.nextButton, "Next", 'orange')
    drawButton(app.instructionsExitButton, "Exit", 'darkred')

    for line, y in wrappedText:
        drawLabel(line, 450, y, size=30, fill='black', align='center')

def drawGameScreen(app):
    # Sidebar background
    drawRect(0, 0, 250, app.height, fill='darkgreen')

    # Year and progress bar
    drawLabel(f"Year {app.currentYear} of {app.totalYears}", 125, 30, size=20, fill='white', bold=True)
    drawRect(65, 50, 120, 20, fill='lightgray', border='white')

    # Ensure progressWidth is always at least 1 for visibility
    progressWidth = max(app.progressBarWidth, 1)
    drawRect(65, 50, progressWidth, 20, fill='limegreen')

    # Pocket cash and net worth
    drawLabel("Pocket Cash", 125, 100, size=15, fill='white')
    drawLabel(f"${app.pocketCash:,.2f}", 125, 120, size=20, fill='white', bold=True)
    drawLabel("Overall Net Worth", 125, 160, size=15, fill='white')
    drawLabel(f"${app.netWorth:,.2f}", 125, 180, size=20, fill='white', bold=True)
    drawButton(app.leaderboardButton, "Leaderboard", 'darkblue')
    drawButton(app.exitButton, "Exit", 'darkred')

    # Main game area
    drawRect(250, 0, 650, app.height, fill='lightyellow')
    drawLabel("SAVINGS ACCOUNT", 390, 50, size=25, bold=True, fill='darkgreen')
    drawLabel(f"${app.savings:,.2f}", 390, 125, size=25, bold=True, fill='black')
    drawLabel("BALANCE", 390, 90, size=15, fill='black', bold=True)
    drawLine(540, 0, 540, 285, lineWidth = 4)

    drawInputField(app, app.inputField, app.inputValue)

    # Buttons for withdraw and deposit
    drawRect(265, 200, 100, 40, fill='lightgray', border='black', borderWidth=2)
    drawLabel("Deposit", 315, 220, size=15, fill='black')
    drawRect(415, 200, 100, 40, fill='lightgray', border='black', borderWidth=2)
    drawLabel("Withdraw", 465, 220, size=15, fill='black')

    if app.currentYear >= 1 and not app.CDScreen:
        drawLabel("CERTIFICATE OF DEPOSIT", 715, 50, size=25, bold=True, fill='darkgreen')
        drawLabel("Current CD Price", 640, 100, size=20, fill='black', bold=True)
        drawLabel(f"${getCDSPrice(app):.2f}", 800, 100, size=20, fill='black', bold=True)
        drawButton(app.CDButton, "Buy CD", 'darkgreen')
        drawLabel(f"CD Holdings: {app.cdHoldings}", 625, 150, size=20, fill='black')
    
    if app.CDScreen:
        drawRect(600, 0, 400, 600, fill = "lightyellow")
        drawLabel("CERTIFICATE OF DEPOSIT", 715, 50, size=25, bold=True, fill='darkgreen')
        drawLabel("Current CD Price", 640, 100, size=20, fill='black', bold=True)
        drawLabel(f"${getCDSPrice(app):.2f}", 800, 100, size=20, fill='black', bold=True)
        drawButtonCircle(app.CDbutton1, "6 Months", 'black')
        drawButtonCircle(app.CDbutton2, "1 Years", 'black')
        drawButtonCircle(app.CDbutton3, "3 Years", 'black')
        drawLabel(f"{((app.CDAPY-1) * 100):.2f}% APY", 635, 215, size=15, fill='black')
        drawLabel("Min Deposit $500.00", 760, 215, size=15, fill='black')
        drawButton(app.buyCDButton, "buy", "black")
        drawButton(app.exitCDButton, "X", 'black')
        drawInputField(app, app.CDInputField, app.CDInputValue)

    if app.currentYear >= 3:
        # Draw each stock and its details
        drawLine (250, 285, 900, 285, lineWidth = 4)
        drawLabel ("STOCKS", 545, 320, size = 25, bold = True, fill = 'darkgreen')
        xStart = 285
        for i, stock in enumerate(app.stocks):
            drawRect(xStart, 350, 125, 225, fill='lightgreen', border='black')
            drawLabel(stock.name, xStart + 62, 370, size=20, bold=True, align='center', fill='black')

            # Display current price
            price = f"${stock.current_price:.2f}"
            drawLabel(price, xStart + 62, 400, size=20, bold=True, align='center', fill='black')

            # Display delta
            delta = stock.getDelta()
            deltaText = f"{delta:+.2f}%"  # Show '+' for positive deltas
            deltaColor = 'green' if delta > 0 else 'red'
            drawLabel(deltaText, xStart + 62, 420, size=15, align='center', fill=deltaColor)

            # Display number of shares owned
            drawLabel(f"Shares: {app.stockShares[i]}", xStart + 62, 440, size=15, align='center', fill='black')

            # Buy and sell buttons
            drawButton(app.buyButtons[i], "Buy", 'black')
            drawButton(app.sellButtons[i], "Sell", 'black')
            xStart += 150

        for i in range(len(app.stockChoices)):
            drawButton(app.stockChoices[i], app.labels[i], 'black', 10)
    # Display leaderboard if toggled
    if app.showLeaderboard:
        drawRect(300, 200, 400, 200, fill='white', border='black', borderWidth=2)
        drawLabel("Leaderboard", 500, 220, size=20, bold=True, fill='black')
        drawLabel(f"You: ${app.netWorth:,.2f}", 500, 260, size=18, fill='black')
        drawLabel(f"Computer: ${app.computerNetWorth:,.2f}", 500, 300, size=18, fill='black')
    
    #Stock Chart
    drawButton(app.stockChartButton, "Stock Chart", 'darkblue') 
    if app.showStockChart:
        if app.currentChartType ==1:
            drawStockChart(app)
        else:
            drawStockChart2(app)

    drawButton(app.pieChartButton, "Portfolio Pie Chart", 'darkblue') 
    if app.showPieChart:
        drawRect(400, 150, 400, 300, fill='white', border='black', borderWidth=2)
        draw_pie_chart(app)
        draw_hover_info(app)
    #News Button
    drawButton(app.newsButton, "NewsCentral", 'darkblue') 
    drawNewsPrediction(app) 

def drawEndScreen(app):
    endScreen = "image6.jpg"
    drawImage(endScreen, 0, 0)
    if app.computerNetWorth > app.netWorth:
        drawLabel(f"GAME OVER", 450, 100, size=70, fill='red', bold=True, border = 'black')
    else:
        drawLabel(f"YIPEEE! YOU WIN!", 450, 100, size = 70, fill = 'yellow', bold = True, border = 'white')
    drawRect(250, 150, 400, 300, fill = 'white')
    drawLabel("Leaderboard", 450, 170, size = 35, fill = 'black', bold = True)
    drawLabel(f"You: ${app.netWorth:,.2f}", 450, 230, size=25, fill='black')
    drawLabel(f"Computer: ${app.computerNetWorth:,.2f}", 450, 290, size=25, fill='black')


def drawNewsPrediction(app):
    """Draws the predicted economic event if the news button is clicked."""
    if app.showNews:
        drawRect(25, 370, 200, 180, fill='white', border='black', borderWidth=2)
        drawLabel(f"Predicted News:", 120, 384, size=18, fill='black', bold=True)
        start = 420
        for predict in app.predictedEvent:
                drawLabel(predict["description"], 123, start, size=8, fill='black', align='center')
                start += 20
        drawLabel(f"Actual News:", 120, 490, size=18, fill='black', bold=True)
        wrapCurrent = wrapText(app.currentEvent, 200, 20, 515)
        for line, y in wrapCurrent:
            drawLabel(line, 123, y, size=13, fill='black', align='center')
def drawButton(button, text, textColor, size=20):
    drawRect(button['x'], button['y'], button['width'], button['height'],
             fill=button['color'], border=button['border'], borderWidth=3)
    drawLabel(text, button['x'] + button['width'] / 2, button['y'] + button['height'] / 2, size=size, fill=textColor)

def drawButtonSpecial(button, text, textColor):
    drawRect(button['x'], button['y'], button['width'], button['height'],
             fill=button['color'], border=button['border'], borderWidth=3)
    drawLabel(text, button['x'] + button['width'] / 2, button['y'] + button['height'] / 2, size=10, fill=textColor)

def drawButtonCircle(button, text, textColor):
    drawCircle(button['x'], button['y'], button['radius'], fill=button['color'], border=button['border'], borderWidth=3)
    drawLabel(text, button['x'], button['y'], size=15, fill=textColor)

def drawInputField(app, inputField, inputValue):
    """Draws the input field for typing amounts."""
    drawRect(inputField['x'], inputField['y'], inputField['width'], inputField['height'],
             fill='white', border=app.inputField['border'], borderWidth=2)
    drawLabel(inputValue, inputField['x'] + inputField['width'] / 2,
              inputField['y'] + inputField['height'] / 2, size=15, fill='black', align='center')

def isMouseInButton(button, mouseX, mouseY):
    return (button['x'] <= mouseX <= button['x'] + button['width'] and
            button['y'] <= mouseY <= button['y'] + button['height'])

def isMouseInButtonCircle(button, mouseX, mouseY):
    return (button['x'] - button['radius'] <= mouseX <= button['x'] + button['radius'] and
            button['y'] - button['radius'] <= mouseY <= button['y'] + button['radius'])

def drawPopup(app):
    """Draw the pop-up screen."""
    # Draw the pop-up background
    drawRect(725, 125, 125, 50, fill='white', border='black', borderWidth=3)

    # Display the pop-up content
    drawLabel(app.popupContent, 785, 150, size=20, fill='black', align='center')
def draw_pie_chart(app):
    drawLabel("Portfolio", 600, 170, size = 25, bold = True, fill = 'black')
    drawLabel("PocketCash", 640, 240, size=15, bold=True, fill=app.pieColor[0], font = 'orbitron')
    drawLabel("Savings", 640, 265, size=15, fill=app.pieColor[1], bold=True, font = 'orbitron')
    drawLabel("CDs", 640, 290, size=15, fill=app.pieColor[2], bold=True, font = 'orbitron')
    drawLabel("Stocks", 640, 315, size=15, fill=app.pieColor[3], bold=True, font = 'orbitron')
    total = sum(app.pie)
    if total == 0:
        return None
    startAngle = 0

    for value, color in zip(app.pie, app.pieColor):
        if value <= 0:
            continue
        sweepAngle = 360 * (value / total)
        drawArc(app.pieCenter[0], app.pieCenter[1], 2 * app.pieRadius, 2 * app.pieRadius, startAngle, sweepAngle, fill=color, border = "black")
        startAngle += sweepAngle 

def draw_hover_info(app):
    if app.hoveredIndex is not None:
        total = sum(app.pie)
        percentage = (app.pie[app.hoveredIndex] / total) * 100

        # Calculate the position for the percentage
        angle_rad = angleToRadian(app.hoveredAngle)
        x = app.pieCenter[0] + app.pieRadius / 2 * math.cos(angle_rad)
        y = app.pieCenter[1] - app.pieRadius / 2 * math.sin(angle_rad)

        drawLabel(f"{percentage:.2f}%", x, y, size=12, fill='black', bold=True)
def angleToRadian(angle):
    return angle * math.pi / 180


def drawStockChart(app):
    # Background for the chart
    chartX, chartY, chartWidth, chartHeight = 300, 100, 500, 300
    drawRect(chartX, chartY, chartWidth, chartHeight, fill='white', border='black', borderWidth=2)

    # Draw axes
    drawLine(chartX, chartY + chartHeight, chartX + chartWidth, chartY + chartHeight, fill='black')  # X-axis
    drawLine(chartX, chartY, chartX, chartY + chartHeight, fill='black')  # Y-axis

    # Labels for axes
    drawLabel("Time", chartX + chartWidth / 2, chartY + chartHeight - 20, size=12, fill='black', bold=True)
    drawLabel("Price", chartX + 20, chartY + chartHeight / 2, size=12, fill='black', align='center', bold=True)

    # Plot stock price lines for each stock
    maxHistoryLength = max(len(stock.price_history) for stock in app.stocks)
    minPrice = min(min(stock.price_history) for stock in app.stocks)
    maxPrice = max(max(stock.price_history) for stock in app.stocks)

    for i, stock in enumerate(app.stocks):
        # Map stock prices to chart coordinates
        color = ['red', 'blue', 'green', 'orange'][i % 4]  # Distinct colors for each stock
        xStep = chartWidth / maxHistoryLength
        yScale = chartHeight / (maxPrice - minPrice)  # Normalize to fit the graph

        for j in range(1, len(stock.price_history)):
            x1 = chartX + (j - 1) * xStep
            y1 = chartY + chartHeight - (stock.price_history[j - 1] - minPrice) * yScale
            x2 = chartX + j * xStep
            y2 = chartY + chartHeight - (stock.price_history[j] - minPrice) * yScale
            drawLine(x1, y1, x2, y2, fill=color)

        # Add stock labels
        drawLabel(stock.name, chartX + chartWidth - 40, chartY + 20 + i * 20, size=12, fill=color, bold=True)
def drawStockChart2(app):
    chartX, chartY, chartWidth, chartHeight = 300, 100, 500, 300
    drawRect(chartX, chartY, chartWidth, chartHeight, fill='white', border='black', borderWidth=2)

    # Draw axes
    drawLine(chartX, chartY + chartHeight, chartX + chartWidth, chartY + chartHeight, fill='black')  # X-axis
    drawLine(chartX, chartY, chartX, chartY + chartHeight, fill='black')  # Y-axis

    # Labels for axes
    drawLabel("Time", chartX + chartWidth / 2, chartY + chartHeight - 20, size=12, fill='black', bold=True)
    drawLabel("Price", chartX + 20, chartY + chartHeight / 2, size=12, fill='black', align='center', bold=True)

    # Determine the range of prices for normalization
    maxHistoryLength = max(len(stock.price_history) for stock in app.stocks)
    minPrice = min(min(stock.price_history) for stock in app.stocks)
    maxPrice = max(max(stock.price_history) for stock in app.stocks)

    # Calculate dimensions for candlesticks
    xStep = chartWidth / maxHistoryLength
    yScale = chartHeight / (maxPrice - minPrice)

    for i, stock in enumerate(app.stocks):
        color = ['red', 'blue', 'green', 'orange'][i % 4]  # Distinct colors for each stock
        for j in range(1, len(stock.price_history)):
            # Compute high, low, open, and close values for the candlestick
            openPrice = stock.price_history[j - 1]
            closePrice = stock.price_history[j]
            highPrice = max(openPrice, closePrice)
            lowPrice = min(openPrice, closePrice)

            # Map prices to chart coordinates
            x = chartX + j * xStep - xStep / 2
            yOpen = chartY + chartHeight - (openPrice - minPrice) * yScale
            yClose = chartY + chartHeight - (closePrice - minPrice) * yScale
            yHigh = chartY + chartHeight - (highPrice - minPrice) * yScale
            yLow = chartY + chartHeight - (lowPrice - minPrice) * yScale

            # Draw the vertical line for high-low range
            drawLine(x, yHigh, x, yLow, fill='black')

            # Draw the rectangle for open-close range (candlestick body)
            bodyColor = 'green' if closePrice > openPrice else 'red'
            drawRect(x - xStep / 4, min(yOpen, yClose), xStep / 2, abs(yClose - yOpen), fill=bodyColor)

        # Add a legend for each stock
        drawLabel(stock.name, chartX + chartWidth - 40, chartY + 20 + i * 20, size=12, fill=color, bold=True)
def predictEconomicEvent(app):
    while len(app.predictedEvent) != 3:
        event = random.choice(app.economicEvents)
        if event not in app.predictedEvent:
            app.predictedEvent.append(event) # Predicted economic event
def applyEconomicEvent(app):
    """Applies a random economic event every 5 years."""
    current = random.choice(app.predictedEvent)
    app.currentEvent = current["description"]
        # Apply the effects of the event to the stock prices
    for stock in app.stocks:
        if stock.name in current["effect"]:
            adjustment = current["effect"][stock.name]
            stock.current_price *= (1 + adjustment)
            stock.current_price = max(stock.current_price, 0.01)

def onMousePress(app, mouseX, mouseY):
    if app.currentScreen == "home":
        if isMouseInButton(app.startButton, mouseX, mouseY):
            app.currentScreen = "game"  # Switch to game screen
        elif isMouseInButton(app.instructionsButton, mouseX, mouseY):
            app.currentScreen = "instructions"
            app.currentInstructionIndex = 0  # Reset to the first instruction
    elif app.currentScreen == "instructions":
        if isMouseInButton(app.nextButton, mouseX, mouseY):
            app.currentInstructionIndex += 1
            if app.currentInstructionIndex >= len(app.instructions):
                app.currentInstructionIndex = 0  # Restart from the first instruction
        elif isMouseInButton(app.instructionsExitButton, mouseX, mouseY):
            app.currentScreen = "home"  # Return to home screen
    elif app.currentScreen == "game":
        if isMouseInButton(app.exitButton, mouseX, mouseY):
            app.currentScreen = "home"
        # Check input field
        elif (app.inputField['x'] <= mouseX <= app.inputField['x'] + app.inputField['width'] and
                app.inputField['y'] <= mouseY <= app.inputField['y'] + app.inputField['height']):
            app.activeInput = "amount"
        # Withdraw button
        elif 265 <= mouseX <= 365 and 200 <= mouseY <= 240:
            if app.inputValue:
                amount = float(app.inputValue)
                if 0 < amount <= app.pocketCash:
                    app.pocketCash -= amount
                    app.savings += amount
                    app.inputValue = ""
        # Deposit button
        elif 415 <= mouseX <= 515 and 200 <= mouseY <= 240:
            if app.inputValue:
                amount = float(app.inputValue)
                if 0 < amount <= app.savings:
                    app.savings -= amount
                    app.pocketCash += amount
                    app.inputValue = ""
        # CD button
        elif 650 <= mouseX <= 750 and 190 <= mouseY <= 265:  
            app.CDScreen = True
        if app.CDScreen:
            if (app.CDInputField['x'] <= mouseX <= app.CDInputField['x'] + app.CDInputField['width']  and
                    app.CDInputField['y'] <= mouseY <= app.CDInputField['y'] + app.CDInputField['height']):
                app.CDactiveInput = "amount"
        
        if isMouseInButton(app.buyCDButton, mouseX, mouseY) and app.CDtime:
            if app.CDInputValue:
                amount = float(app.CDInputValue)
                if 500 <= amount <= app.pocketCash and app.cdHoldings < 3:
                    app.cdHoldings += 1
                    app.pocketCash -= amount
                    app.cd_price += amount
                    app.cds.append(CD("IDC", base_price=amount,APY = app.CDAPY, maturity_time= app.CDtime))
                    app.CDInputValue = ""
                    app.CDScreen = False
                    app.CDtime = None
                    app.CDbutton1["color"] = "cyan"
                    app.CDbutton2["color"] = "cyan"
                    app.CDbutton3["color"] = "cyan"
        
        if isMouseInButtonCircle(app.CDbutton1, mouseX, mouseY):
            app.CDbutton1["color"] = "lightblue"
            app.CDbutton2["color"] = "cyan"
            app.CDbutton3["color"] = "cyan"
            app.CDtime = 6
        if isMouseInButtonCircle(app.CDbutton2, mouseX, mouseY):
            app.CDbutton2["color"] = "lightblue"
            app.CDbutton1["color"] = "cyan"
            app.CDbutton3["color"] = "cyan"
            app.CDtime = 12
        if isMouseInButtonCircle(app.CDbutton3, mouseX, mouseY):
            app.CDbutton3["color"] = "lightblue"
            app.CDbutton2["color"] = "cyan"
            app.CDbutton1["color"] = "cyan"
            app.CDtime = 36

        if isMouseInButton(app.exitCDButton, mouseX, mouseY):
            app.CDScreen = False
            
        if isMouseInButton(app.leaderboardButton, mouseX, mouseY):
            app.showLeaderboard = not app.showLeaderboard 
        
        #STOCKS
        stockAmounts = [1, 10, 25, "max"]

# Loop through all buttons in groups of 4
        for group_index in range(4):
            group_start = group_index * 4

            for i in range(4):
                if isMouseInButton(app.stockChoices[group_start + i], mouseX, mouseY):
                    app.stockChoices[group_start + i]["color"] = "lightblue"

                    for j in range(4):
                        if j != i:
                            app.stockChoices[group_start + j]["color"] = "white"

                    app.stockAmount[group_index] = stockAmounts[i]
                    break

        #Buy Buttons
        for idx, button in enumerate(app.buyButtons):
            if isMouseInButton(button, mouseX, mouseY) and app.stockAmount[idx]:
                SelectMax = False
                if app.stockAmount[idx] == "max":
                    SelectMax = True
                    app.stockAmount[idx] = app.pocketCash // app.stocks[idx].current_price
                price = app.stocks[idx].current_price * app.stockAmount[idx]
                app.stocks[idx].bought_price = app.stocks[idx].current_price
                if app.pocketCash > price:
                    app.stockShares[idx] += app.stockAmount[idx]
                    app.pocketCash -= price
                if SelectMax:
                    app.stockAmount[idx] = "max"
        #Sell Buttons
        for idx, button in enumerate(app.sellButtons):
            if isMouseInButton(button, mouseX, mouseY) and app.stockAmount[idx]:
                SelectMax = False
                if app.stockAmount[idx] == "max":
                    SelectMax = True
                    app.stockAmount[idx] = app.stockShares[idx]
                price = app.stocks[idx].current_price * app.stockAmount[idx]
                if app.stockShares[idx] >= app.stockAmount[idx]:
                    app.pocketCash += price
                    app.stockShares[idx] -= app.stockAmount[idx]
                if SelectMax:
                    app.stockAmount[idx] = "max"

        #Toggle to show Stock Chart
        if isMouseInButton(app.stockChartButton, mouseX, mouseY):
            app.showStockChart = not app.showStockChart

        if isMouseInButton(app.pieChartButton, mouseX, mouseY):
            app.showPieChart = not app.showPieChart

        if isMouseInButton(app.newsButton, mouseX, mouseY):
            app.showNews = not app.showNews

def onMouseMove(app, mouseX, mouseY):
    if app.currentScreen == "game":
        if app.showPieChart == True:
            dx = mouseX - app.pieCenter[0]
            dy = mouseY - app.pieCenter[1]
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance <= app.pieRadius:
                # Mouse is inside the pie radius
                angle = (math.atan2(-dy, dx) * 180 / math.pi) % 360  # Angle in degrees
                total = sum(app.pie)
                startAngle = 0
                for i, value in enumerate(app.pie):
                    sweepAngle = 360 * (value / total)
                    if startAngle <= angle < startAngle + sweepAngle:
                        app.hoveredIndex = i
                        app.hoveredAngle = startAngle + sweepAngle / 2
                        return
                    startAngle += sweepAngle
            app.hoveredIndex = None

def onKeyPress(app, key):
    if app.activeInput == "amount":
        if key.isdigit() or key == ".":
            app.inputValue += key
        elif key == "backspace":
            app.inputValue = app.inputValue[:-1]
        else:
            app.activeInput = None
            app.inputValue = "" 
    elif app.CDactiveInput == "amount":
        if key.isdigit() or key == ".":
            app.CDInputValue += key
        elif key == "backspace":
            app.CDInputValue = app.CDInputValue[:-1]
        else:
            app.CDactiveInput = None
            app.CDInputValue = ""
    if key == 'm':
        # Toggle the chart type
        app.currentChartType = 1 if app.currentChartType == 2 else 2

def onStep(app):
    if app.currentScreen == "game":
        # Increment the progress bar width
        app.progressBarWidth += app.progressBarIncrement

        # If the bar is full, reset and increment the year
        if app.progressBarWidth >= 120:
            app.progressBarWidth = 0
            app.currentYear += 1
            app.savings += app.savings * app.savingsInterestRate
            app.netWorth = app.pocketCash + app.savings + (app.cdHoldings * getCDSPrice(app)) + (getStockPrices(app))
            # Stop the game when years reach the total limit
            if app.currentYear > app.totalYears:
                app.currentScreen = "end"
        if app.progressBarWidth % 120 == 0:
            app.pocketCash += 5000
            app.netWorth += 5000
            app.computerNetWorth += 4500
            app.cpocketCash += 5000

        if app.progressBarWidth % 10 == 0:
            updateCDSPrice(app)
            checkCDTime(app)
            if app.currentYear >= 3:
                updateStocks(app)
            app.netWorth = app.pocketCash + app.savings + (app.cdHoldings * getCDSPrice(app)) + (getStockPrices(app))

    if app.currentYear % 5 == 4 and app.progressBarWidth == 0 and app.currentYear > 0:
        app.predictedEvent = []
        predictEconomicEvent(app)

    if app.currentYear % 5 == 0 and app.progressBarWidth == 0 and app.currentYear > 0:
        applyEconomicEvent(app)
    if app.showPopup:
        app.popupTimer += 1
        # Close the pop-up after 2 seconds (2 seconds * 10 steps per second)
        if app.popupTimer >= 20:
            app.showPopup = False
    app.pie = [app.pocketCash, app.savings, getCDSPrice(app), getStockPrices(app)]

    if app.progressBarWidth % 60 == 0:
        computerStrategy(app)

def redrawAll(app):
    if app.currentScreen == "home":
        drawHomeScreen(app)
    elif app.currentScreen == "instructions":
        drawInstructionsScreen(app)
    elif app.currentScreen == "game":
        drawGameScreen(app)
    elif app.currentScreen == "end":
        drawEndScreen(app)
    if app.showPopup:
        drawPopup(app)
    draw_hover_info(app)

class CD:
    def __init__(self, name, APY, base_price, maturity_time):
        self.name = name
        self.base_price = base_price  # Initial price of the CD
        self.current_price = base_price
        self.age = 0  # Age of the CD in months
        self.maturity_time = maturity_time  # Maturity time in months
        self.APY = APY

    def updatePrice(self):
        """Simulates price fluctuations in the stock market."""

        percentIncrease = pythonRound(pow((self.APY), (1/12)), 8) #1/12 because we're increasing the cd price every month
        self.current_price = pythonRound(self.base_price * pow(percentIncrease ,self.age),2)  # Ensure price is never negative
        self.age += 1
    
    def isMature(self):
        """Checks if the CD has reached maturity."""
        return self.age >= self.maturity_time
def updateCDSPrice(app):
    for cd in app.cds:
        cd.updatePrice()

def getCDSPrice(app):
    sum = 0
    for cd in app.cds:
        sum += cd.current_price
    return sum

def checkCDTime(app):
    temp = []
    for cd in app.cds:
        if not cd.isMature():
            temp.append(cd)
        else:
            app.popupContent = f"${cd.current_price}$"
            app.showPopup = True
            app.popupTimer = 0 
            app.pocketCash += cd.current_price
            app.cdHoldings -= 1
    app.cds = temp

class Stock:
    def __init__(self, name, base_price):
        self.name = name
        self.base_price = base_price
        self.current_price = base_price
        self.previous_price = base_price  # Track the previous price
        self.price_history = [base_price]
        self.bought_price = 0

    def updatePrice(self):
        """Simulate stock price changes using a Monte Carlo model (Gaussian random walk)."""
        self.previous_price = self.current_price  # Update the previous price
        daily_return = gauss(0, 0.02)  # Mean return is 0, with a standard deviation of 2%
        self.current_price *= (1 + daily_return)
        self.current_price = max(self.current_price, 0.01)  # Ensure prices are never negative
        self.price_history.append(self.current_price)

    def getDelta(self):
        """Returns the price change (delta)."""
        return self.current_price - self.previous_price

def updateStocks(app):
    """Update the price of each stock."""
    for stock in app.stocks:
        stock.updatePrice()

def getStockPrices(app):
    sum = 0
    for idx, stock in enumerate(app.stocks):
        sum += (stock.bought_price * app.stockShares[idx]) - (stock.getDelta() * app.stockShares[idx])
    return sum

def getCDSPrice(app):
    sum = 0
    for cd in app.cds:
        sum += cd.current_price
    return sum


runApp(height = 600, width = 900)

# References:
# Trevor Santiago. "Simulating Stock Prices With Monte Carlo Methods - Trevor Santiago." Youtube, uploaded by Trevor Santiago, Dec 9, 2020, https://www.youtube.com/watch?v=dYiZAgsUY8U. Accessed 1 Dec. 2024
# for lines 831 -  841

# OpenAI. *ChatGPT*. Version Nov. 2024, OpenAI, https://chat.openai.com. Accessed 2 Dec. 2024.
# for lines 780-798, 822-837, 449-522 (debug purposes), also used in attended to webscrape and code genetic algorithm

# Beazley, D. (2009). A Python Book: Beginning Python, Advanced Python, and Python Exercises, https://www.dabeaz.com/action/stockclass.html. Accessed 25 Nov. 2024
# for lines 831-841
 
 # GeeksforGeeks. "Enumerate() in Python." GeeksforGeeks, GeeksforGeeks, 23 Sept. 2023, https://www.geeksforgeeks.org/enumerate-in-python/. Accessed 30 Nov. 2024
 # for lines 306, 467, 503, 645, 659, 694, 850

# Coinbase. "How to Read a Candlestick Chart." Coinbase, https://www.coinbase.com/learn/tips-and-tutorials/how-to-read-candlestick-chart. Accessed 6 Dec. 2024.
# for lines 482 - 527

 # Homepage Image from "https://www.ibackdrop.com/products/sports-green-grass-football-field-background-football-frame-light-backdrop-ibd-19756?variant=31262967988337"
 # Instructionpage Image from "https://www.dbackdrop.com/products/solid-color-portrait-photography-backdrop-baby-pink-photo-background-sc6"
 # Endpage Image from "https://chapinc.org/blog-news/new-compliance-program/"

# Zhejie Jiang from the University of Chicago
# Lines 169 - 198 (help with Computer AI attempt)