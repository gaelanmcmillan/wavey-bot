import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
TS_GUILD_ID = os.getenv("TS_GUILD_ID")
PUBLIC_KEY = os.getenv("PUBLIC_KEY")

if __name__ == "__main__":
    print(TOKEN)
