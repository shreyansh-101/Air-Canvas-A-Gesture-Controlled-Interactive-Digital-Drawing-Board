from handTracker import HandTracker, ColorRect
import numpy as np
import random
import math
import cv2

# Initialize the hand detector
detector = HandTracker(detectionCon=0.8)

try:
    # Initialize the camera
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    # Creating canvas to draw on it
    canvas = np.zeros((720, 1280, 3), np.uint8)

    # Define a previous point to be used with drawing a line
    px, py = 0, 0
    # Initial brush color
    color = (255, 0, 0)
    # Brush and eraser sizes
    brushSize = 5
    eraserSize = 20

    # Creating colors
    colorsBtn = ColorRect(200, 0, 100, 100, (120, 255, 0), 'Colors')

    colors = []
    # Random color
    b = int(random.random() * 255)
    g = int(random.random() * 255)
    r = int(random.random() * 255)
    colors.append(ColorRect(300, 0, 100, 100, (b, g, r)))
    # Red
    colors.append(ColorRect(400, 0, 100, 100, (0, 0, 255)))
    # Blue
    colors.append(ColorRect(500, 0, 100, 100, (255, 0, 0)))
    # Green
    colors.append(ColorRect(600, 0, 100, 100, (0, 255, 0)))
    # Yellow
    colors.append(ColorRect(700, 0, 100, 100, (0, 255, 255)))
    # Eraser (black)
    colors.append(ColorRect(800, 0, 100, 100, (0, 0, 0), "Eraser"))

    # Clear button
    clear = ColorRect(900, 0, 100, 100, (100, 100, 100), "Clear")

    # Pen sizes
    pens = []
    for i, penSize in enumerate(range(5, 25, 5)):
        pens.append(ColorRect(1100, 50 + 100 * i, 100, 100, (50, 50, 50), str(penSize)))

    penBtn = ColorRect(1100, 0, 100, 50, color, 'Pen')

    # Whiteboard button
    boardBtn = ColorRect(50, 0, 100, 100, (255, 255, 0), 'Board')

    # Shape buttons
    shapesBtn = ColorRect(1000, 0, 100, 50, (200, 200, 200), 'Shapes')
    squareBtn = ColorRect(1000, 50, 100, 100, (200, 200, 200), 'Square')
    circleBtn = ColorRect(1000, 150, 100, 100, (200, 200, 200), 'Circle')
    triangleBtn = ColorRect(1000, 250, 100, 100, (200, 200, 200), 'Triangle')
    brushBtn = ColorRect(1000, 350, 100, 100, (200, 200, 200), 'Brush')

    # Define a whiteboard to draw on
    whiteBoard = ColorRect(50, 120, 1020, 580, (255, 255, 255), alpha=0.6)

    coolingCounter = 20
    shapeCooldownCounter = 0
    hideBoard = True
    hideColors = True
    hidePenSizes = True
    hideShapes = True
    selectedTool = 'None'  # Default tool

    while True:
        if coolingCounter:
            coolingCounter -= 1
        if shapeCooldownCounter:
            shapeCooldownCounter -= 1

        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (1280, 720))
        frame = cv2.flip(frame, 1)

        detector.findHands(frame)
        positions = detector.getPostion(frame, draw=False)  # Corrected method name
        upFingers = detector.getUpFingers(frame)

        if upFingers:
            x, y = positions[8][0], positions[8][1]
            if upFingers[1] and not whiteBoard.isOver(x, y):
                px, py = 0, 0

                ##### Pen sizes ######
                if not hidePenSizes:
                    for pen in pens:
                        if pen.isOver(x, y):
                            brushSize = int(pen.text)
                            pen.alpha = 0
                        else:
                            pen.alpha = 0.5

                ####### Choose a color for drawing #######
                if not hideColors:
                    for cb in colors:
                        if cb.isOver(x, y):
                            color = cb.color
                            cb.alpha = 0
                        else:
                            cb.alpha = 0.5

                    # Clear
                    if clear.isOver(x, y):
                        clear.alpha = 0
                        canvas = np.zeros((720, 1280, 3), np.uint8)
                    else:
                        clear.alpha = 0.5

                # Color button
                if colorsBtn.isOver(x, y) and not coolingCounter:
                    coolingCounter = 10
                    colorsBtn.alpha = 0
                    hideColors = False if hideColors else True
                    colorsBtn.text = 'Colors' if hideColors else 'Hide'
                else:
                    colorsBtn.alpha = 0.5

                # Pen size button
                if penBtn.isOver(x, y) and not coolingCounter:
                    coolingCounter = 10
                    penBtn.alpha = 0
                    hidePenSizes = False if hidePenSizes else True
                    penBtn.text = 'Pen' if hidePenSizes else 'Hide'
                else:
                    penBtn.alpha = 0.5

                # Whiteboard button
                if boardBtn.isOver(x, y) and not coolingCounter:
                    coolingCounter = 10
                    boardBtn.alpha = 0
                    hideBoard = False if hideBoard else True
                    boardBtn.text = 'Board' if hideBoard else 'Hide'
                else:
                    boardBtn.alpha = 0.5

                # Shapes button
                if shapesBtn.isOver(x, y) and not coolingCounter:
                    coolingCounter = 10
                    shapesBtn.alpha = 0
                    hideShapes = False if hideShapes else True
                    shapesBtn.text = 'Shapes' if hideShapes else 'Hide'
                else:
                    shapesBtn.alpha = 0.5

                if not hideShapes:
                    if squareBtn.isOver(x, y) and not coolingCounter:
                        coolingCounter = 10
                        selectedTool = 'Square'
                        squareBtn.alpha = 0
                    else:
                        squareBtn.alpha = 0.5

                    if circleBtn.isOver(x, y) and not coolingCounter:
                        coolingCounter = 10
                        selectedTool = 'Circle'
                        circleBtn.alpha = 0
                    else:
                        circleBtn.alpha = 0.5

                    if triangleBtn.isOver(x, y) and not coolingCounter:
                        coolingCounter = 10
                        selectedTool = 'Triangle'
                        triangleBtn.alpha = 0
                    else:
                        triangleBtn.alpha = 0.5

                    if brushBtn.isOver(x, y) and not coolingCounter:
                        coolingCounter = 10
                        selectedTool = 'Brush'
                        brushBtn.alpha = 0
                    else:
                        brushBtn.alpha = 0.5

            elif upFingers[1] and not upFingers[2] and not shapeCooldownCounter:
                if whiteBoard.isOver(x, y) and not hideBoard:
                    if selectedTool == 'Brush':
                        cv2.circle(frame, positions[8], brushSize, color, -1)
                        # Drawing on the canvas
                        if px == 0 and py == 0:
                            px, py = positions[8]
                        if color == (0, 0, 0):
                            cv2.line(canvas, (px, py), positions[8], color, eraserSize)
                        else:
                            cv2.line(canvas, (px, py), positions[8], color, brushSize)
                        px, py = 0,0
                    elif selectedTool == 'Square':
                        if px == 0 and py == 0:
                            px, py = positions[8]
                        else:
                            length = math.dist(positions[4], positions[8])  # Distance between thumb and index
                            start_point = (int(px - length / 2), int(py - length / 2))
                            end_point = (int(px + length / 2), int(py + length / 2))
                            cv2.rectangle(canvas, start_point, end_point, color, brushSize)
                            px, py = 0, 0
                            shapeCooldownCounter = 20  # Add cooldown for shapes
                    elif selectedTool == 'Circle':
                        if px == 0 and py == 0:
                            px, py = positions[8]
                        else:
                            radius = int(math.dist(positions[4], positions[8]))  # Distance between thumb and index
                            cv2.circle(canvas, (px, py), radius, color, brushSize)
                            px, py = 0, 0
                            shapeCooldownCounter = 20  # Add cooldown for shapes
                    elif selectedTool == 'Triangle':
                        if px == 0 and py == 0:
                                px, py = positions[8]
                        else:
                                length = math.dist(positions[4], positions[8])  # Distance between thumb and index
                                pts = np.array([[px, py - length / 2], [px - length / 2, py + length / 2],
                                                [px + length / 2, py + length / 2]], np.int32)
                                pts = pts.reshape((-1, 1, 2))
                                cv2.polylines(canvas, [pts], isClosed=True, color=color, thickness=brushSize)
                                px, py = 0, 0
                                shapeCooldownCounter = 20  # Add cooldown for shapes

            # Put colors button
            colorsBtn.drawRect(frame)
            cv2.rectangle(frame, (colorsBtn.x, colorsBtn.y), (colorsBtn.x + colorsBtn.w, colorsBtn.y + colorsBtn.h),
                          (255, 255, 255), 2)

            # Put whiteboard button
            boardBtn.drawRect(frame)
            cv2.rectangle(frame, (boardBtn.x, boardBtn.y), (boardBtn.x + boardBtn.w, boardBtn.y + boardBtn.h),
                          (255, 255, 255), 2)

            # Put the whiteboard on the frame
            if not hideBoard:
                whiteBoard.drawRect(frame)
                # Moving the draw to the main image
                canvasGray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
                _, imgInv = cv2.threshold(canvasGray, 20, 255, cv2.THRESH_BINARY_INV)
                imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
                frame = cv2.bitwise_and(frame, imgInv)
                frame = cv2.bitwise_or(frame, canvas)

            # Draw colors' boxes
            if not hideColors:
                for c in colors:
                    c.drawRect(frame)
                    cv2.rectangle(frame, (c.x, c.y), (c.x + c.w, c.y + c.h), (255, 255, 255), 2)

                clear.drawRect(frame)
                cv2.rectangle(frame, (clear.x, clear.y), (clear.x + clear.w, clear.y + clear.h), (255, 255, 255), 2)

            # Draw pen size boxes
            penBtn.color = color
            penBtn.drawRect(frame)
            cv2.rectangle(frame, (penBtn.x, penBtn.y), (penBtn.x + penBtn.w, penBtn.y + penBtn.h), (255, 255, 255), 2)
            if not hidePenSizes:
                for pen in pens:
                    pen.drawRect(frame)
                    cv2.rectangle(frame, (pen.x, pen.y), (pen.x + pen.w, pen.y + pen.h), (255, 255, 255), 2)

            # Draw shape buttons
            shapesBtn.drawRect(frame)
            cv2.rectangle(frame, (shapesBtn.x, shapesBtn.y), (shapesBtn.x + shapesBtn.w, shapesBtn.y + shapesBtn.h),
                          (255, 255, 255), 2)
            if not hideShapes:
                squareBtn.drawRect(frame)
                cv2.rectangle(frame, (squareBtn.x, squareBtn.y), (squareBtn.x + squareBtn.w, squareBtn.y + squareBtn.h),
                              (255, 255, 255), 2)

                circleBtn.drawRect(frame)
                cv2.rectangle(frame, (circleBtn.x, circleBtn.y), (circleBtn.x + circleBtn.w, circleBtn.y + circleBtn.h),
                              (255, 255, 255), 2)

                triangleBtn.drawRect(frame)
                cv2.rectangle(frame, (triangleBtn.x, triangleBtn.y), (triangleBtn.x + triangleBtn.w, triangleBtn.y + triangleBtn.h),
                              (255, 255, 255), 2)

                brushBtn.drawRect(frame)
                cv2.rectangle(frame, (brushBtn.x, brushBtn.y), (brushBtn.x + brushBtn.w, brushBtn.y + brushBtn.h),
                              (255, 255, 255), 2)

        cv2.imshow('video', frame)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
