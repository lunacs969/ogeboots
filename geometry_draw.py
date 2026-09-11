import matplotlib.pyplot as plt
import os



def parse_geometry_data(data):

    points = []
    lines = []
    values = []

    section = None


    for raw in data.split("\n"):

        line = raw.strip()

        if not line:
            continue


        if line.endswith(":"):

            section = line.replace(":", "")
            continue



        if section == "POINTS":

            points.append(
                line.split()[0]
            )


        elif section == "LINES":

            lines.append(line)


        elif section == "VALUES":

            values.append(line)



    return points, lines, values





def create_coordinates(points):


    # треугольник с высотой

    if (
        "A" in points
        and "B" in points
        and "C" in points
        and "H" in points
    ):

        return {

            "A": (0,5),

            "B": (-3,0),

            "C": (3,0),

            "H": (0,0)

        }



    coords = {}

    count = len(points)


    for i, name in enumerate(points):

        angle = (
            2 * 3.14159 * i / count
        )

        import math

        coords[name] = (

            3 * math.cos(angle),

            3 * math.sin(angle)

        )


    return coords





def draw_right_angle(x,y):


    size = 0.35


    plt.plot(

        [
            x,
            x + size,
            x + size,
            x
        ],

        [
            y,
            y,
            y + size,
            y + size
        ],

        color="black",

        linewidth=1.5

    )





def draw_value(value, coords):


    if "=" not in value:
        return


    name, number = value.split("=")


    name = name.strip()


    if name == "AH":

        plt.text(

            0.2,
            2.5,

            number,

            fontsize=12

        )


    elif name == "BC":

        plt.text(

            -0.5,
            -0.45,

            number,

            fontsize=12

        )





def draw_geometry(data):


    points, lines, values = parse_geometry_data(data)


    coords = create_coordinates(points)



    plt.figure(

        figsize=(6,6)

    )



    plt.xlim(-5,5)

    plt.ylim(-2,6)



    # линии фигуры


    for line in lines:


        if len(line) >= 2:


            a = line[0]

            b = line[1]


            if (
                a in coords
                and b in coords
            ):


                plt.plot(

                    [
                        coords[a][0],
                        coords[b][0]
                    ],

                    [
                        coords[a][1],
                        coords[b][1]
                    ],

                    color="black",

                    linewidth=2

                )



    # точки и буквы


    for name, point in coords.items():


        plt.scatter(

            point[0],

            point[1],

            color="black",

            s=25

        )


        offset = 0.25


        if name == "H":

            offset = -0.45



        plt.text(

            point[0],

            point[1] + offset,

            name,

            fontsize=14

        )



    # прямой угол


    if "H" in coords:


        draw_right_angle(

            coords["H"][0],

            coords["H"][1]

        )



    # значения


    for value in values:

        draw_value(

            value,

            coords

        )



    plt.axis(
        "equal"
    )


    plt.axis(
        "off"
    )


    filename = "geometry.png"



    plt.savefig(

        filename,

        dpi=300,

        bbox_inches="tight",

        pad_inches=0.5

    )


    plt.close()



    print(

        "Создан чертёж:",

        os.path.getsize(filename),

        "байт"

    )


    return filename