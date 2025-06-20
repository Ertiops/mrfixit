from mrfixit.domains.entities.tech_request import (
    TechRequest,
    TechRequestCategory,
    TechRequestStatus,
)


def format_tech_request_line(req: TechRequest) -> str:
    emoji = "🔴" if req.category == TechRequestCategory.URGENT else "🔵"
    line = f"{emoji} {req.title}"
    if req.status == TechRequestStatus.DONE:
        return f"<s>{line}</s>"
    return line
