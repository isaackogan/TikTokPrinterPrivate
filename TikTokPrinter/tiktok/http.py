import logging
import random
import string
import traceback
from typing import Optional, List, Dict

import aiohttp
from TikTokLive.types import User, Gift


class ProfileImage:
    """
    ProfileImage HTTP Scraping Object
    
    """

    DEFAULT_REQUEST_HEADERS: Dict[str, str] = {
        "authority": "m.tiktok.com", "scheme": "https", "sec-gcp": "1",
        "accept-encoding": "gzip", "accept-language": "en-US,en;q=0.9", "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors", "sec-fetch-site": "none", "accept": "application/json, content/plain, */*",
        "Connection": 'keep-alive', "'Cache-Control'": 'max-age=0', "Accept": 'content/html,application/json,application/protobuf',
        "'User-Agent'": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        "Referer": 'https://www.tiktok.com/', "Origin": 'https://www.tiktok.com', "Accept-Language": 'en-US,en;q=0.9', "Accept-Encoding": 'gzip, deflate',
    }
    """Default headers for making TikTok Requests"""

    def __init__(self, user: Optional[User], index: int = 0):
        """
        Initialize a ProfileImage object
        
        :param user: The user the profile image belongs to
        :param index: The index to pull the image from
        
        """

        self.index: int = index
        self.user: User = user

    @staticmethod
    def generate_device_id() -> str:
        """
        Generates a valid device_id for requests
        
        """

        return "".join([random.choice(string.digits) for _ in range(19)])

    @property
    def url(self) -> str:
        """
        Get their profile picture URL
        
        :return: The URL
        
        """

        return self.user.profilePicture.urls[self.index]

    async def to_download(self, path: str, custom_headers: dict = {}, proxies: Optional[List] = []) -> bool:
        """
        Download an image to a given file path
        
        :param proxies: List of proxies (picks a random one)
        :param path: Path to download to
        :param custom_headers: Custom headers if necessary
        :return: Whether it downloaded successfully
        
        """
        b: Optional[bytes] = await self.to_bytes(custom_headers, proxies)

        try:
            with open(path, 'wb') as file:
                file.write(b)

            return True
        except:
            logging.error(traceback.format_exc() + "\nFailed to save the image to disk")
            return False

    async def to_bytes(self, custom_headers: dict = {}, proxies: Optional[List] = []) -> Optional[bytes]:
        """
        Turn a profile image object to bytes
        
        :param proxies: List of proxies (picks a random one)
        :param custom_headers: Custom headers if necessary
        :return: Image in bytes
        
        """

        return await self.__to_bytes(self.url, headers=custom_headers, proxies=proxies)

    async def __to_bytes(self, url: str, headers: dict, proxies: Optional[List[str]]) -> Optional[bytes]:
        """
        Image to bytes
        
        :param url: URL of image
        :param headers: Headers to request with
        :return: Optional data (if successful)\
        
        """

        device_id = self.generate_device_id()
        headers: dict = {**self.DEFAULT_REQUEST_HEADERS, **headers, **{"tt_webid": device_id, "tt_webid_v2": device_id}}
        proxy: Optional[str] = random.choice(proxies) if proxies and len(proxies) > 0 else None

        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
                async with session.get(url=url, headers=headers, proxy=proxy) as request:
                    return await request.read()
        except:
            logging.error(traceback.format_exc() + "\nFailed to download the profile picture image!")
            return None


class GiftImage(ProfileImage):
    """
    GiftImage HTTP Scraping Object
    
    """

    def __init__(self, gift: Gift):
        """
        Initialize the GiftImage class
        
        :param gift: The gift to get the image for
        
        """

        super().__init__(None)
        self.gift: Gift = gift

    @property
    def url(self) -> str:
        """
        Get their profile picture URL

        :return: The URL

        """

        return self.gift.extended_gift.image.url_list[-1]
