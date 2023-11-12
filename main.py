import flet as ft
import aiohttp
import asyncio
pokemon = 0

#Asyncronous functions, this way will prepare the information prior to refresh the page
async def main(page: ft.Page):
    page.window_width = 720
    page.window_height = 1280
    page.window_resizable = False
    page.padding = 0
    page.fonts = { #using the zpix font (kind of videogame)
        "zpix": "https://github.com/SolidZORO/zpix-pixel-font/releases/download/v3.1.8/zpix.ttf",
    }
    page.theme = ft.Theme(font_family="zpix")
    
    
    #this function generates a request using http
    async def request(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json() #output format will be json format to make it handy.
    
    #if we press the top arrow button will increase the count and pokemon number, if press the botton arrow will decrease it. 
    async def get_pokemon(e: ft.ContainerTapEvent):
        global pokemon
        if e.control == top_arrow:
            pokemon +=1
        else:
            pokemon -=1
        
        number = (pokemon%150) + 1 #bring the pokemons from 1 to 150 instead of 0 to 149
        result = await request(f"https://pokeapi.co/api/v2/pokemon/{number}")
        
        #formatting the data to be shown on the green screen
        data = f"Name: {result['name']}\n\nAbilities:"
        for element in result['abilities']:
            skill = element['ability']['name']
            data += f"\n{skill}"
        data += f"\n\nHeight: {result['height']}"
        text.value = data
        #update the image
        sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{number}.png"
        image.src = sprite_url
        #refresh the page
        await page.update_async()
    
    #make the blue light blink
    async def blink():
        while True:
            await asyncio.sleep(1)
            blue_light.bgcolor = ft.colors.BLUE_100
            await page.update_async()
            await asyncio.sleep(0.1)
            blue_light.bgcolor = ft.colors.BLUE
            await page.update_async()
    #lights container
    blue_light = ft.Container(width=70, height=70, left=5, top=5, bgcolor=ft.colors.BLUE, border_radius=50)
    light = ft.Stack([
        ft.Container(width=80,height=80,bgcolor=ft.colors.WHITE,border_radius=50),
        blue_light,
        
    ])
    #top items container
    top_items = [
        ft.Container(content=light,width=80,height=80),
        ft.Container(width=40,height=40,bgcolor=ft.colors.RED_200,border_radius=50),
        ft.Container(width=40,height=40,bgcolor=ft.colors.YELLOW,border_radius=50),
        ft.Container(width=40,height=40,bgcolor=ft.colors.GREEN,border_radius=50),
    ]
    #image container 
    sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png"
    image = ft.Image(
        src= sprite_url,
        scale=10,
        width=30,
        height=30,
        top=350/2,
        left=550/2
    )
    #screen container
    center_stack = ft.Stack([
        ft.Container(width=600, height=400, bgcolor= ft.colors.WHITE,border_radius=10),
        ft.Container(width=550, height=350, bgcolor= ft.colors.BLACK, top=25, left=25),
        image,
    ])
    #using canvas to draw a triangle 
    triangle = ft.canvas.Canvas([
        ft.canvas.Path([
            ft.canvas.Path.MoveTo(40,0),
            ft.canvas.Path.LineTo(0,50),
            ft.canvas.Path.LineTo(80,50),
        ],
                       paint=ft.Paint(
                           style=ft.PaintingStyle.FILL,
                       ),
                    ),
    ],
        width=80,
        height=50
                              )
    #arrows for the buttons
    top_arrow = ft.Container(triangle, width=80, height=50, on_click = get_pokemon)
    arrows = ft.Column([
        top_arrow,
        ft.Container(triangle, rotate=ft.Rotate(angle = 3.14159),width=80, height=50, on_click = get_pokemon)
    ])
    #Text to be displayed (by default shows three points because it is loading the information)
    text = ft.Text(
        value="...",
        color=ft.colors.BLACK,
        size=22
        )
    #in this container will be display the data related to the pokemon
    inferior_items = [
        ft.Container(width=50,),#Left Margin
        ft.Container(text, padding=10, width=400, height=300, bgcolor=ft.colors.GREEN, border_radius=20),
        ft.Container(width=30,), #Right Margin
        ft.Container(arrows, width=80, height=120),
    ]
    
    #declaration of the main container or background
    top = ft.Container(content=ft.Row(top_items), width=600,height=80, margin=ft.margin.only(top=40))
    center = ft.Container(content = center_stack, width=600,height=400, margin=ft.margin.only(top=40), alignment=ft.alignment.center)
    inferior = ft.Container(content=ft.Row(inferior_items), width=600,height=400, margin=ft.margin.only(top=40), )
    
    col = ft.Column(spacing=0,controls=[
        top,
        center,
        inferior,
    ])
    container = ft.Container(col,width=720,height=1280,bgcolor=ft.colors.RED,alignment=ft.alignment.top_center)
    
    #load the page and start blinking after the loading of the page.
    await page.add_async(container)
    await blink()
    
    #point the execution point to the main.
ft.app(target=main)