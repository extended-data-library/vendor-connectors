"""Pydantic schemas for Google connector tools."""
from __future__ import annotations

from pydantic import BaseModel, Field


class GoogleListFoldersArgs(BaseModel):
    """Arguments for the google_list_folders tool."""

    parent: str = Field(..., description="Parent resource (organizations/ORG_ID or folders/FOLDER_ID).")
    unhump_folders: bool = Field(False, description="Convert keys to snake_case.")
