"""Pydantic schemas for GitHub connector tools."""
from __future__ import annotations

from pydantic import BaseModel, Field


class GitHubListRepositoriesArgs(BaseModel):
    """Arguments for the github_list_repositories tool."""

    type_filter: str = Field("all", description="Filter type ('all', 'public', 'private', 'forks', 'sources', 'member').")
    include_branches: bool = Field(False, description="Include branch information.")
