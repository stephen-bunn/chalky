from chalky import bg, fg, hex, rgb, sty

# compose some styles together
print(fg.red & sty.bold | "Bold and red text")
print(bg.blue & fg.white & sty.italic | "White italic text on a blue background")

# store a style for later use
success_style = fg.green
print(success_style | "Success message")
print(success_style & sty.underline | "Underlined success message")

# build some true colors as well
print(rgb(255, 9, 255) | "Purply text")
print(hex("#ffdd00") & sty.bold | "Bold yellowy text")
