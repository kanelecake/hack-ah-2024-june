from PIL import Image, ImageDraw, ImageFont


# Функция для нахождения координат вершин четырехугольника
def find_vertices(Mx, My, a, b):
    a += 2
    b += 2

    # Предположим, что (Mx, My) - это вершина A четырехугольника
    Ax, Ay = Mx, My

    # Вершина B находится на расстоянии a от A
    Bx = Ax + a
    By = Ay

    # Вершина C находится на расстоянии b от B
    Cx = Bx
    Cy = By + b

    # Вершина D находится на расстоянии c от C (предполагая, что D находится слева от C)
    Dx = Cx - a
    Dy = Cy

    # Вернуть координаты вершин
    return [(Ax, Ay), (Bx, By), (Cx, Cy), (Dx, Dy)]


# Отрисовка основного квадрата с дефектом
def draw_bbox(image, labels):
    draw = ImageDraw.Draw(image)

    for label in labels:
        Mx, My = label.x, label.y  # середина
        a, b = label.width, label.height  # длины сторон

        vertices = find_vertices(Mx, My, a, b)
        draw.polygon(vertices, outline="lightgreen", width=2, fill=None)

        text = "Class: " + label.classifier
        font = ImageFont.load_default(size=14)

        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        text_position = (Mx, My - text_height)
        rectangle_position = [text_position, (text_position[0] + text_width, text_position[1] + text_height)]

        draw.rectangle(rectangle_position, fill="white")
        draw.text(text_position, text, fill="black", font=font)

    # Возвращаем полученное изображение
    return image
