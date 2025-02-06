from fastapi import Response, Depends
from app.usecases.complaint_usecase import ComplaintUseCase
from app.models.schemas.complaint_schema import ComplaintCreate


class ComplaintController:
    def __init__(self, complaint_usecase: ComplaintUseCase = Depends(ComplaintUseCase)):
        self.complaint_usecase = complaint_usecase

    async def create_complaint(self, complaint: ComplaintCreate):
        return await self.complaint_usecase.create_complaint(complaint)