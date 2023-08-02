from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api import init_router
from app.core.config import get_app_settings
from app.models import beanie_client


class App:
    def create_app(self) -> FastAPI:
        settings = get_app_settings()
        settings.configure_logging()

        self.app = FastAPI(**settings.fastapi_kwargs)
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.ALLOWED_HOSTS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @self.app.get("/")
        async def root():
            return {"message": "Hello world"}

        # @app.middleware("http")
        # async def add_process_time_header(request: Request, call_next):
        #     start_time = time.time()
        #     response = await call_next(request)
        #     process_time = time.time() - start_time
        #     response.headers["X-Process-Time"] = str(process_time)
        #     return response

        @self.app.on_event("startup")
        async def init_app():
            await init_router(self.app, settings)
            await beanie_client.init_beanie(settings)

        return self.app


fastapi_app = App()
