from fastapi import APIRouter, Request

router = APIRouter()

@router.get('/health')
async def health():
    return {'status' : 'Up'}