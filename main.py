from TikTokLive.types.events import ShareEvent

from TikTokPrinter import TikTokPrinterClient, EscposEngineGenerator

client: TikTokPrinterClient = TikTokPrinterClient(
    unique_id="USERNAME_HERE",
    engine=EscposEngineGenerator.create_usb(
        vendor_id=0x1,  # Vendor ID goes here
        product_id=0x1,  # Product ID goes here
        align="center"
    )
)


@client.on("share")
async def on_share(event: ShareEvent):
    client.text(f"Thank you, @{event.user.uniqueId}, for sharing the LIVE!")


if __name__ == '__main__':
    """
    
    Just getting started? Check out the README and LICENSE files.
    
    The README includes all pertinent information to get started. The LICENSE file
    lets you know what you can and can't do with this project, legally speaking.
    
    Thanks for purchasing Isaac Kogan's Printer Script.
    
    Best of luck,
    Isaac
    
    """

    client.run()
