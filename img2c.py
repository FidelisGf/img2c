import cv2 as cv

def convert_rgb565(pixel):
    b, g, r = pixel[0:3]
    rgb = ((r & 0b11111000) << 8) | ((g & 0b11111100) << 3) | (b >> 3)

    return hex(rgb)

def create_matrix(img):
    altura, largura, _ = img.shape

    colors = set()
    matrix_str = f"static unsigned int sprite[{largura}][{altura}] = " + "{\n"
    for i in range(largura):
        matrix_str += "    { "
        for j in range(altura):
            current_color = convert_rgb565(img[j,i])

            colors.add(current_color)
            matrix_str += f"{current_color}, "
        matrix_str += "}\n"
    matrix_str += "}\n"

    colors_str = ""
    for idx, color in enumerate(list(colors)):
        color_n = f"C{idx}"
        colors_str += f"int {color_n} = {color};\n"
        matrix_str = matrix_str.replace(color, color_n)

    colors_str += "\n"
    dimensions_str = f"int W = {largura};\n"
    dimensions_str += f"int H = {altura};\n"

    return colors_str + dimensions_str + matrix_str

def write_file(file_name, info):
    with open(file_name, "w") as f:
        f.write(info)

def warn_bytes(img):
    altura, largura, _ = img.shape
    byte_count = altura * largura

    print(f"Quantidade de Bytes utilizados: {byte_count}")

    if byte_count > 2048:
        print("CUIDADO! IMAGEM PASSA DE 2KB!")
    print("Tome isto como uma guia, pois a quantidade exata de bytes usado pode variar dependendo das otimizacoes do compilador")

def main():
    img = cv.imread('input.bmp')
    info = create_matrix(img)

    warn_bytes(img)
    write_file('output.txt', info)

if __name__ == '__main__':
    main()
