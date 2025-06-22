from mrfixit.domains.entities.tech_request import (
    TechRequest,
    TechRequestCategory,
    TechRequestStatus,
)
from mrfixit.presenters.bot.content.emojies import common as common_emj


def format_tech_request_line(req: TechRequest) -> str:
    emoji = (
        common_emj.RED_BALL
        if req.category == TechRequestCategory.URGENT
        else common_emj.BLUE_BALL
    )
    line = f"{emoji} {req.title}"
    if req.status == TechRequestStatus.DONE:
        return f"<s>{line}</s>"
    return line
