from PIL import Image, ImageDraw, ImageFont

def parse_zpl(zpl_code):
    commands = []
    lines = zpl_code.split('^')
    for line in lines:
        if line:
            command = line[:2]
            params = line[2:].split(',')
            commands.append((command, params))
    return commands

def draw_zpl(commands, image):
    draw = ImageDraw.Draw(image)
    font_large = ImageFont.truetype("arial.ttf", 60)
    font_medium = ImageFont.truetype("arial.ttf", 30)
    font_small = ImageFont.truetype("arial.ttf", 15)
    font_barcode = ImageFont.truetype("arial.ttf", 40)
    
    x, y = 0, 0
    reverse = False
    for command, params in commands:
        if command == 'FO':  # Field Origin
            x, y = int(params[0]), int(params[1])
        elif command == 'FD':  # Field Data
            text = ','.join(params)
            draw.text((x, y), text, fill="black", font=font_medium)
        elif command == 'GB':  # Graphic Box
            width, height, border_thickness = int(params[0]), int(params[1]), int(params[2])
            draw.rectangle([x, y, x + width, y + height], outline="black", width=border_thickness)
        elif command == 'CF':  # Change Font
            if params[0] == '0':
                font_large = ImageFont.truetype("arial.ttf", int(params[1]))
            elif params[0] == 'A':
                font_medium = ImageFont.truetype("arial.ttf", int(params[1]))
        elif command == 'BY':  # Barcode Field Default
            barcode_orientation = params[0]
            barcode_height = int(params[1])
            barcode_width = int(params[2])
            barcode_font = ImageFont.truetype("arial.ttf", barcode_height)

        elif command == 'BC':  # Barcode Code 128
            text = params[0]
            module_width = int(params[1])
            barcode_height = int(params[2])
            barcode_font = ImageFont.truetype("arial.ttf", barcode_height)

            # Calculate x-coordinate adjustment for centered barcode
            x_adjustment = (barcode_width - len(text) * module_width) // 2

            draw.text((x + x_adjustment, y), text, fill="black", font=barcode_font)
                
        elif command == 'FR':  # Field Reverse Print
            reverse = True
        elif command == 'FS':  # Field Separator
            reverse = False
        elif command == 'FX':  # Comment
            pass  # Comments are ignored
        # Add more ZPL commands as needed
    return image

def generate_image_from_zpl(zpl_code, output_file):
    # Create a blank canvas
    image = Image.new('RGB', (800, 1200), 'white')  # Adjust size as needed

    # Parse ZPL code
    commands = parse_zpl(zpl_code)

    print(commands)
    # Draw elements based on ZPL commands
    image = draw_zpl(commands, image)

    # Save the image
    image.save(output_file)

# Example ZPL code
zpl_code = """
^XA
^FX Top section with logo, name and address.
^CF0,60
^FO50,50^GB100,100,100^FS
^FO75,75^FR^GB100,100,100^FS
^FO93,93^GB40,40,40^FS
^FO220,50^FDIntershipping, Inc.^FS
^CF0,30
^FO220,115^FD1000 Shipping Lane^FS
^FO220,155^FDShelbyville TN 38102^FS
^FO220,195^FDUnited States (USA)^FS
^FO50,250^GB700,3,3^FS
^FX Second section with recipient address and permit information.
^CFA,30
^FO50,300^FDJohn Doe^FS
^FO50,340^FD100 Main Street^FS
^FO50,380^FDSpringfield TN 39021^FS
^FO50,420^FDUnited States (USA)^FS
^CFA,15
^FO600,300^GB150,150,3^FS
^FO638,340^FDPermit^FS
^FO638,390^FD123456^FS
^FO50,500^GB700,3,3^FS
^FX Third section with bar code.
^BY5,2,270
^FO100,550^BC^FD12345678^FS
^FX Fourth section (the two boxes on the bottom).
^FO50,900^GB700,250,3^FS
^FO400,900^GB3,250,3^FS
^CF0,40
^FO100,960^FDCtr. X34B-1^FS
^FO100,1010^FDREF1 F00B47^FS
^FO100,1060^FDREF2 BL4H8^FS
^CF0,190
^FO470,955^FDCA^FS
^XZ
"""

# Generate image from ZPL code
generate_image_from_zpl(zpl_code, 'output.png')