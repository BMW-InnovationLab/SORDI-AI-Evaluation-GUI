from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from api.controllers import inference_services_controller, evaluation_jobs_controller, web_graphs_controller, \
    datasets_controller, health_controller

app = FastAPI()

app.mount("/results", StaticFiles(directory="../servable"), name="results")
app.mount("/images", StaticFiles(directory="../servable_images"), name="images")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    inference_services_controller.router,
    prefix="/services/inference",
    tags=["Inference Services"]
)

app.include_router(
    datasets_controller.router,
    prefix="/datasets",
    tags=["Datasets"]
)

app.include_router(
    evaluation_jobs_controller.router,
    prefix="/evaluation/jobs",
    tags=["Evaluation Jobs"]
)

app.include_router(
    web_graphs_controller.router,
    prefix="/graphs/web",
    tags=["Web Graphs"]
)

app.include_router(
    health_controller.router,
    prefix="/health",
    tags=["Health"]
)