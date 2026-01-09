from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
IP = env.str("ip")  # Xosting ip manzili

# Chess analysis settings
GEMINI_API_KEY = env.str("GEMINI_API_KEY")  # Gemini API key
STOCKFISH_DEPTH = env.int("STOCKFISH_DEPTH", 15)  # Stockfish analysis depth
STOCKFISH_TIME_LIMIT = env.float("STOCKFISH_TIME_LIMIT", 2.0)  # Time limit in seconds

# Database
DB_PATH = env.str("DB_PATH", "data/chess_bot.db")  # SQLite database path

# File upload limits
MAX_IMAGE_SIZE_MB = 10  # Maximum image size in MB
