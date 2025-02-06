from fastapi import HTTPException, status, Depends, Response
from app.services.complaint_service import ComplaintService
from app.models.schemas.complaint_schema import ComplaintCreate


class ComplaintUseCase():
    def __init__(self, complaint_service: ComplaintService = Depends(ComplaintService)):
        self.complaint_service = complaint_service

    
    async def create_complaint(self, complaint: ComplaintCreate):
        return await self.complaint_service.create_complaint(complaint)

    
    